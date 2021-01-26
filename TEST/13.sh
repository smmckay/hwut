#! /usr/bin/env bash
# Bug 15 describes a case, where the actual output is empty while
#        the GOOD output is only one line long. This was a special
#        case where the comparison failed. It id not consider the
#        last read GOOD line.
#
# fix&test by: 14y08m01 fschaef
#______________________________________________________________________________
arg=$1
test_id=13
source ./hwut_greet.sh "Bug $test_id" \
         stephanhengefel \
         'Dysfunctional: hwut make clean' \
         'CHOICES: recursive, local;'

export HWUT_EXE="python $HWUT_PATH/hwut-exe.py"
# We do not HAVE to use 'hwut_call.sh' if the output is omitted anyway.
# Here, HWUT is called directly.
export HWUT_TEST_DIR_NAME=$test_id
export HWUT_TERMINAL_WIDTH=80

case $1 in 
    recursive)
        # Walk recursively through directory tree, and try to find test
        # directories, namely the ones called '13'
        echo "Walk recursively from directory: 13"
        cd $HWUT_TEST_DIR_NAME
    ;;
    local)
        # Consider only the local directory.
        echo "Consider only leaf directory: '$HWUT_TEST_DIR_NAME/1/1/1/13'"
        echo 
        cd $HWUT_TEST_DIR_NAME/1/1/1/13
esac

# Make sure, that there is no trailing dirt.
rm -rf $(find -name dirt.txt)

# Execute 'make dirt' in the lowest directory of the tree.
$HWUT_EXE make dirt --no-color >& /dev/null

echo "Have dirt files have been created?"
echo
find -name dirt.txt | sort
echo

# Execute 'make clean' in the lowest directory of the tree.
$HWUT_EXE make clean --no-color >& /dev/null

echo "Have dirt files have been removed (no output is good output)?"
echo
find -name dirt.txt | sort
echo

echo "<Test Done>"


