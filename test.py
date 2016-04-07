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
