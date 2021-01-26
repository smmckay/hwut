# PURPOSE: 
#
# This script calls HWUT for a directory given as the first argument. 
#
# -- it cleans the directory upon entry.
# -- executes HWUT
# -- extracts the HWUT output from within the dashed lines
# -- it cleans the directory upon exit.
#
# ARGUMENTS:
#    $1      -- directory contains the use case.
#    $2      -- additional instruction 
#               If it is not a command, it will be left as HWUT argument.
#    ...     -- remaining HWUT arguments
#
# AUTHOR: 14y08m01d Frank-Rene Schaefer
#______________________________________________________________________________
trash=/dev/null
test_dir=$1
shift
clean_f=false
case "$1" in 
    "CMD:clean") clean_f=true; shift; 
    ;;
esac

export HWUT_EXE="python $HWUT_PATH/hwut-exe.py"
temp_file=$(mktemp)

echo 
echo "Test: $test_dir"
echo 
echo "> hwut $@"
echo 

# TRICK: Let HWUT consider the test_dir's directory as THE test directory.
export HWUT_TEST_DIR_NAME=$test_dir
# Make sure that the text width is constant for all  tests.
export HWUT_TERMINAL_WIDTH=80

pushd $test_dir >& $trash

function clean_test_directory {
    rm -f $temp_file >& $trash
    make clean       >& $trash
    rm -f OUT/*      >& $trash
    rm -f ADM/*      >& $trash
}

# -- clean upon entry
if [ "$clean_f" = "true" ]; then
    echo "hwut_call.sh: CLEAN TEST DIRECTORY"
    clean_test_directory
fi

# -- call HWUT and extract output
$HWUT_EXE $@ --no-color >& $temp_file

awk 'BEGIN{ x=0; } /---/ { x=!x; if( !x ) { print $0; } } { if(x) { print $0; } }' $temp_file | awk '! /^ *make/'

# -- clean upon exit
if [ "$clean_f" = "true" ]; then
    clean_test_directory
else
    mv $temp_file tmp.txt
fi

popd >& $trash
