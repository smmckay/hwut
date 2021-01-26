#! /usr/bin/env bash
# Feature f16 -- Oversize Detection
#
# fix&test by: 14y11m14d fschaef
#______________________________________________________________________________
arg=$1
test_id=22
source ./hwut_greet.sh "Feature $test_id" fschaef \
         'Futile make commands;' 

# We do not HAVE to use 'hwut_call.sh' if the output is omitted anyway.
# Here, HWUT is called directly.
export HWUT_TEST_DIR_NAME=$test_id
export HWUT_TERMINAL_WIDTH=40

./hwut_call.sh 22 also.sh

echo "<Test Done>"
