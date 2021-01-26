#! python
print "Hello World"
import sys
if "--hwut-info" in sys.argv:
    print "EXTRA_FILES: OUTPUT-2.txt, OUTPUT-1.txt;"
    print "EXTRA_FILES(A): OUTPUT-A.txt;"
    print "EXTRA_FILES(B): OUTPUT-B.txt;"

open("OUTPUT-1.txt", "wb").write("Hi %s\n" % sys.argv[1])
open("OUTPUT-2.txt", "wb").write("Hallo %s\n" % sys.argv[1])
open("OUTPUT-A.txt", "wb").write("Hi A\n")
open("OUTPUT-B.txt", "wb").write("Hallo B\n")
