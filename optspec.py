#--------------------------------------------------------------------
# optspec.py: A wrapper around getopt.getopt(), providing option
#             counting, mapping, and parsing capabilities.
#
# Author: Lain Supe (lainproliant)
# Date: Tuesday, April 5 2015
#--------------------------------------------------------------------

import getopt
import sys

#--------------------------------------------------------------------
class OptionSpec:
    def __init__(self, *forms,
            name        = None,
            param       = None,
            required    = False,
            additive    = False,
            multi       = False,
            default     = None,
            parser      = lambda a: a,
            increment   = 1):
        
        self.name = name
        self.param = param or required or multi or default
        self.required = required
        self.additive = additive and not multi
        self.multi = multi
        self.default = default
        self.parser = parser
        self.increment = increment
        self.shortopts = None
        self.longopts = None
        self.reps = []

        shortopts = set()
        longopts = set()

        for form in forms:
            if len(form) > 1:
                opt = form

                if name is None:
                    self.name = form
                if self.param:
                    opt += '='

                longopts.add(opt)
                self.reps.append('--' + form)

            else:
                opt = form

                if self.param:
                    opt += ':'

                shortopts.add(opt)
                self.reps.append('-' + form)

        self.longopts = longopts
        self.shortopts = shortopts

        if self.name is None:
            self.name = forms[0]

#--------------------------------------------------------------------
class Options:
    def __init__(self):
        self.specs = []
    
    def inherit(self, options):
        self.specs.extend(options.specs)

    def opt(self, *args, **kwargs):
        self.specs.append(OptionSpec(*args, **kwargs))
        return self

    def parse(self, argv = sys.argv):
        shortopts = ''.join([s for shortopts in [spec.shortopts for spec in self.specs] for s in shortopts])
        longopts = [l for longopts in [spec.longopts for spec in self.specs] for l in longopts]
        required_set = set([s.name for s in self.specs if s.required])
        
        repmap = {}
        optmap = {}

        for spec in self.specs:
            repmap.update({rep: spec for rep in spec.reps})

        opts, args = getopt.getopt(argv[1:], shortopts, longopts)

        for rep, val in opts:
            if not rep in repmap:
                raise Exception('Encountered unknown option rep: "%s"' % opt)
            
            spec = repmap[rep]

            if spec.param:
                if spec.additive:
                    if not spec.name in optmap:
                        optmap[spec.name] = spec.parser(val)
                    else:
                        optmap[spec.name] += spec.parser(val)

                elif spec.multi:
                    if not spec.name in optmap:
                        optmap[spec.name] = []
                    optmap[spec.name].append(spec.parser(val))

                else:
                    optmap[spec.name] = spec.parser(val)

            elif spec.additive:
                if not spec.name in optmap:
                    optmap[spec.name] = spec.default or 0
                optmap[spec.name] += spec.increment
            else:
                optmap[spec.name] = True

        for required_name in required_set:
            if not required_name in optmap:
                raise Exception('Missing required parameter: "%s"' % required_name)

        for spec in self.specs:
            if not spec.name in optmap:
                if spec.param:
                    if spec.multi:
                        optmap[spec.name] = spec.default or []
                    else:
                        optmap[spec.name] = spec.default
                elif spec.additive:
                    optmap[spec.name] = spec.default or 0
                else:
                    optmap[spec.name] = False

        return optmap, args

#--------------------------------------------------------------------
class SubcommandMap:
    def __init__(self):
        self.fmap = {}
        self.default = None

    def define(self, name, default = False):
        def define_impl(f):
            self.fmap[name] = f
            if default:
                if self.default is None:
                    self.default = name
                else:
                    raise ValueError('Cannot have multiple default subcommands, "%s" is already defined as the default subcommand.' % self.default)
            return f
        return define_impl

    def get(self, name):
        if not name in self.fmap:
            raise ValueError('Subcommand "%s" does not exist in the SubcommandMap.' % name)
        return self.fmap[name]

    def invoke(self, *args, **kwargs):
        argv = sys.argv
        if 'argv' in kwargs:
            argv = kwargs['argv']
            del kwargs['argv']

        argv = argv[:]
        pname = argv.pop(0)
        name = self.default

        if len(argv) > 0 and argv[0] in self.fmap:
            name = argv.pop(0)
        
        if name is None:
            raise ValueError('No default subcommand defined and no subcommand was provided in the argument list.')

        return self.fmap[name]([pname] + argv, *args, **kwargs)

