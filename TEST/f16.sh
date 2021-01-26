#! /usr/bin/env bash
# Feature f16 -- Oversize Detection
#
# fix&test by: 14y11m14d fschaef
#______________________________________________________________________________
arg=$1
test_id=f16
source ./hwut_greet.sh "Feature $test_id" fschaef \
         'Oversized Output Detection;' 

# We do not HAVE to use 'hwut_call.sh' if the output is omitted anyway.
# Here, HWUT is called directly.
export HWUT_TEST_DIR_NAME=$test_id
export HWUT_TERMINAL_WIDTH=40

pushd $test_id >& /dev/null
rm -f ADM/cache.fly
rm -f OUT/*

for choice in quicky slow-starter stalker; do
    echo "Run choice $choice"
    $HWUT_EXE oversizer.sh $choice >& /dev/null
done
HWUT_OUTPUT_FILE_MAX_SIZE=1048576
echo "Check on generated files sizes. HWUT's default size limit is 1MB."
echo 
echo "-- No output shall be bigger than 10MB               --> [good] or [bad ]"
echo "-- No process shall be actively working on the file. --> users: []"
echo 
for file in $(ls ./OUT/*); do
    verdict=$(ls $file -s --block-size=1 | awk '{ print ($1 < 10 * 1024 * 1024)  ? "good" : "bad " }')
    echo "[$verdict] $file"
    echo "       users: [$(lsof $file)]"
    echo 
done

# Delete the large files.
rm -rf f16/OUT f16/GOOD

echo "<Test Done>"
