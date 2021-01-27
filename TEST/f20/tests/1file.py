#! python
print "Hello World"
import sys
if "--hwut-info" in sys.argv:
    print "EXTRA_FILES: OUTPUT-1.txt;"

open("OUTPUT-1.txt", "wb").write("Hi %s\n" % sys.argv[1])
