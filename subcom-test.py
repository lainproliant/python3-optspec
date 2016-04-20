from optspec import SubcommandMap

subcom = SubcommandMap()

@subcom.define('polite', default = True)
def polite_version(argv):
  if len(argv) < 2:
     print("I'm sorry, I don't know who you are.")

  else:
     print("Good morning, %s!  What a lovely day!" % argv[1])

@subcom.define('rude')
def rude_version(argv):
  if len(argv) < 2:
     print("Who the hell are you?")

  else:
     print("%s??  What a stupid name!" % argv[1])

if __name__ == "__main__":
  subcom.invoke()
