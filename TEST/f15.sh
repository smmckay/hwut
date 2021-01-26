#! /usr/bin/env bash
# Feature f15 -- Time Out functionality.
#
# fix&test by: 14y10m01 fschaef
#______________________________________________________________________________
arg=$1
test_id=f15
source ./hwut_greet.sh "Feature $test_id" fschaef \
         'Time Out Detection;' 

# We do not HAVE to use 'hwut_call.sh' if the output is omitted anyway.
# Here, HWUT is called directly.
export HWUT_TEST_DIR_NAME=$test_id
export HWUT_TERMINAL_WIDTH=40
export HWUT_DEFAULT_TIMEOUT_MIN_SEC=3

set min_t=5

pushd $test_id >& /dev/null
rm -f ADM/cache.fly

chmod 777 make_waiter.sh

rm -f *ms*.sh
./make_waiter.sh 0.1    0.1   > 10ms_a.sh   # 3x T < $min_t second
./make_waiter.sh 0.1    0.1   > 10ms_b.sh   # 3x T < $min_t second
./make_waiter.sh 1.667  1.667 > 1700ms_a.sh # 3x T > $min_t second
./make_waiter.sh 1.667  1.667 > 1700ms_b.sh # 3x T > $min_t second
chmod 777 *ms*.sh

popd >& /dev/null

./hwut_call.sh $test_id 

pushd $test_id >& /dev/null
./make_waiter.sh 0.1   0.1   > 10ms_a.sh   # t < 3 * T; t < 1 sec -- no time out
./make_waiter.sh 0.31  0.1   > 10ms_b.sh   # t > 3 * T; t < 1 sec -- no time out
./make_waiter.sh 2     1.667 > 1700ms_a.sh # t < 3 * T; t > 1 sec -- no time out
./make_waiter.sh 5.1   1.667 > 1700ms_b.sh # t > 3 * T; t > 1 sec -- time out!
chmod 777 *ms*.sh

popd >& /dev/null

cp -f f15/ADM/good_cache.fly f15/ADM/cache.fly
chmod a+rwx f15/ADM/cache.fly

./hwut_call.sh $test_id 

echo
echo "Make, sure that test times are not secretely adapted ..."
echo
./hwut_call.sh $test_id 1700ms_b.sh 
./hwut_call.sh $test_id 1700ms_b.sh 

echo "<Test Done>"

