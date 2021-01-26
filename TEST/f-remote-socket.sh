#! /usr/bin/env bash
# Feature f15 -- Time Out functionality.
#
# fix&test by: 14y10m01 fschaef
#______________________________________________________________________________
arg=$1
test_id=f-remote-socket
source ./hwut_greet.sh "Feature $test_id" fschaef \
         'Remote Execution: Sockets;' 

# We do not HAVE to use 'hwut_call.sh' if the output is omitted anyway.
# Here, HWUT is called directly.
export HWUT_TEST_DIR_NAME=$test_id
export HWUT_TERMINAL_WIDTH=40
export HWUT_DEFAULT_TIMEOUT_MIN_SEC=3

set min_t=5

pushd $test_id >& /dev/null
rm -f ADM/cache.fly

# Use the remote application that is also used in the module's unit test.
pushd $HWUT_PATH/hwut/auxiliary/executer/remote/TEST >& /dev/null
make remotey.exe >& /dev/null
if [ ! -e ./remotey.exe ]; then 
    echo "Error: application 'remotey.exe'" has not been made by 'make'.
    exit
fi

popd >& /dev/null
mkdir -p my-remote-location
mv    $HWUT_PATH/hwut/auxiliary/executer/remote/TEST/remotey.exe ./my-remote-location/

if [ ! -e ./my-remote-location ]; then 
    echo "Error: remote application './my-remote-location/remotey.exe'"
    echo "Error: has not been generated."
    exit
fi

popd >& /dev/null
./hwut_call.sh $test_id

echo "<Test Done>"

