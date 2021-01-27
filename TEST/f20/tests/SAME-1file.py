#! python
print "Hello World"
import sys
if "--hwut-info" in sys.argv:
    print "CHOICES: A, B;"
    print "SAME;"
    print "EXTRA_FILES: OUTPUT-1.txt;"

open("OUTPUT-1.txt", "wb").write("Hi")
