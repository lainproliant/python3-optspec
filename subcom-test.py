from optspec import SubcommandMap

subcom = SubcommandMap()

@subcom.define('polite', default = True)
def polite_version(argv, name):
  if len(argv) < 2:
     print("%s: I'm sorry, I don't know who you are." % name)

  else:
     print("%s: Good morning, %s!  What a lovely day!" % (name, argv[1]))

@subcom.define('rude')
def rude_version(argv, name):
  if len(argv) < 2:
     print("%s: Who the hell are you?" % name)

  else:
     print("%s: %s??  What a stupid name!" % (name, argv[1]))

if __name__ == "__main__":
  subcom.invoke('Robot')
