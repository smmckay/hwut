#! /usr/bin/env bash
# Feature 20: EXTRA_FILES
#
# Test the 'EXTRA_FILES' feature where an application can output extra files
# besides the standard output. Those files are compared binarily.
#
# PROCEDURE: Test: with 1 and 2 output files; 
#                  with and without the 'SAME' flag for choices.
#
# (1) Accept Test
# (2) Run Test
# (3) Slightly change GOOD file of extra file; Run Test Again.
#
# AUTHOR: 15y11m23 fschaef
#______________________________________________________________________________
arg=$1
test_id=f20
source ./hwut_greet.sh "Bug $test_id" fschaef \
         'EXTRA_FILES' \
         'CHOICES: 1-file, 2-files;'

# We do not HAVE to use 'hwut_call.sh' if the output is omitted anyway.
# Here, HWUT is called directly.
export HWUT_TEST_DIR_NAME=$test_id
export HWUT_TERMINAL_WIDTH=80

pushd $test_id >& /dev/null
rm -rf ADM OUT GOOD *.py
popd >& /dev/null

case $1 in 
    1-file)
        cp $test_id/tests/1file.py       $test_id/.
        cp $test_id/tests/SAME-1file.py  $test_id/.
        #
        # (1) Accept
        #
        ./hwut_call.sh $test_id a 1file.py --grant
        ./hwut_call.sh $test_id a SAME-1file.py --grant
        echo 
        echo "Files in GOOD/"
        echo "||||"
        wc $(find $test_id/GOOD -type f)
        echo "||||"
        echo 
        #
        # (2) Test (Oll Korrect)
        #
        ./hwut_call.sh $test_id test
        echo 
        #
        # (3) Test (Extra files fail)
        #
        rm -f $test_id/GOOD/1file.py--file--OUTPUT-1.txt
        rm -f $test_id/GOOD/SAME-1file.py--file--OUTPUT-1.txt
        echo "Nonsense" >> $test_id/GOOD/1file.py--file--OUTPUT-1.txt
        echo "Nonsense" >> $test_id/GOOD/SAME-1file.py--file--OUTPUT-1.txt
        ./hwut_call.sh $test_id test
        echo 
    ;;
    2-files)
        cp $test_id/tests/2files.py       $test_id/.
        cp $test_id/tests/SAME-2files.py  $test_id/.
        #
        # (1) Accept
        #
        ./hwut_call.sh $test_id a 2files.py --grant
        ./hwut_call.sh $test_id a SAME-2files.py --grant
        echo 
        echo "Files in GOOD/"
        echo "||||"
        wc $(find $test_id/GOOD -type f)
        echo "||||"
        echo 
        #
        # (2) Test (Oll Korrect)
        #
        ./hwut_call.sh $test_id test
        echo 
        #
        # (3) Test (Extra files fail)
        #
        rm -f $test_id/GOOD/2files.py--file--OUTPUT-1.txt
        rm -f $test_id/GOOD/SAME-2files.py--file--OUTPUT-1.txt
        echo "Nonsense" >> $test_id/GOOD/2files.py--file--OUTPUT-1.txt
        echo "Nonsense" >> $test_id/GOOD/SAME-2files.py--file--OUTPUT-1.txt
        ./hwut_call.sh $test_id test
        echo 
    ;;
esac


echo "<Test Done>"

