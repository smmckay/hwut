import sys

def error(File, LineN, Str):

    for line in Str.split("\n"):
        print "%s:%i:error: %s" % (File, LineN, line)
    sys.exit(-1)




