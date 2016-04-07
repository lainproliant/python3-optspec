optspec - A wrapper around getopt
=================================

optspec is a wrapper around getopt that provides option parsing, mapping, counting,
and enforcement of required parameters.  I wrote this because I enjoy the
simplicity of getopt.getopt(), but dislike the duplication involved in
interpreting its results into variables or settings.

Option Specifications: The `opt()` Function
-------------------------------------------
The `opt()` function accepts a series of option forms, and keyword arguments
identifying the option's behavior.

The option forms are either shortopts or longopts based on their length:
single-char forms are shortopts and multi character forms are longopts
(sorry, no single-char longopts).  Every form in the specification (optspec)
will map to the same key in the resulting option map (optmap).  This key,
aka `name`, is determined by the first longopt specified, or the first shortopt
specified if no longopts are specified, and can also explicitly be specified
with the `name` keyword argument.

- `name`: Explicitly specifies the option map value key, which is normally
  implied from the option forms.  This can also be used to map options with
  different meanings to the same value key, as per the `-v` and `-q` options
  in the example below.
- `param = True`: Indicates that the option takes a parameter.  If the option is
  not specified, the value in the resulting optmap will be determined based on the
  following rules:
  - If `default` was specified, that value is provided.
  - If `multi = True`, the result is an empty list to indicate that no parameters were provided for a multi parameter option.
  - Otherwise, `None` is provided as the value for the optmap key.
- `required = True`: Indicates that the option is required, and implies
  `param = True`.  If the option is not specified in `sys.argv` or the provided
  `argv`, the `parse()` function will raise an exception.
- `additive = True`: Indicates that the option is additive.  If the option takes
  a parameter, then each time the parameter is provided, it is added to the
  previous value instead of replacing it using the `+` operator.  If the option
  takes no parameters, then `increment` is added to `default` (or `0` if `default`
  was not provided).
- `multi = True`: Indicates that the option can take multiple parameters by being
  specified multiple times.  Each time the option is specified the resulting value
  is added to a list and this list is provided as the value for the optmap key.
  Note that an option may not be `additive` and `multi`, if `multi` is specified
  all rules for `additive` are ignored.
- `default`: Specifies a default value to use for an option with parameters, and
  also indicates the starting value for additive options.  If specified for an
  option that is `multi`, this had ought to be a list or collection of some sort.
- `parser`: Provide a function that is used to parse parameters to options from
  strings.  This is the identify function `lambda a: a` by default.  Some common
  useful values for this include `int` and `float`.
- `increment`: Specifies the value to be added to `default` for `additive` options
  where `param = False`.  This defaults to `1`.

Example Usage
-------------

To use optspec, create an Option object, then specify a series of options using
the `opt()` function successively.  Then, you may call the `parse()` function with
no parameters to parse from `sys.argv` implicitly, or provide your own `argv`
as a parameter.::

   from optspec import Options

   optmap, args = ( Options()
        .opt('s', 'safe')
        .opt('i', 'input', required = True)
        .opt('o', 'output', param = True, default = 'a.out')
        .opt('v', 'verbose', additive = True)
        .opt('p', 'ports', multi = True, parser = int)
        .opt('c', 'count', param = True, additive = True, parser = int, default = 0)
        .opt('q', 'quiet', name = 'verbose', additive = True, increment = -1)
        .parse() )

   print('optmap = %s' % repr(optmap))
   print('args = %s' % repr(args))

   $ python test.py --input a -qq -p 1 -p 2 -c -10000 -c 400 Hello Python
	optmap = {'output': 'a.out', 'count': -9600, 'safe': False, 'ports': [1, 2], 'input': 'a', 'verbose': -2}
	args = ['Hello', 'Python']

