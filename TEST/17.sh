#! /usr/bin/env bash
# Bug 17: A test application is built by 'make'. It contains some choices 
#         as reported by 'CHOICES'. 
#
#         As long as the compilation succeeds, the choices are reported
#         correctly. If it fails, it does not use the stored information.
#         It reports the app as a single application without choices.
#
# fix&test by: 14y08m01 fschaef
#______________________________________________________________________________
arg=$1
test_id=17
source ./hwut_greet.sh "Bug $test_id" \
                       fschaef \
                       'Make CHOICES reduction'

# (0) Delete 'hello.py' -- the test application
rm -f $test_dir/hello.py >& /dev/null

# (1) Run the test while 'make' succeeds.
#     => database should have been updated.
cp $test_id/Makefile.good $test_id/Makefile
source ./hwut_call.sh $test_id 

rm -f $test_id/hello.py >& /dev/null

cp $test_id/Makefile.bad $test_id/Makefile
source ./hwut_call.sh $test_id

# Call it trice, to make sure no historic effects
source ./hwut_call.sh $test_id
source ./hwut_call.sh $test_id
