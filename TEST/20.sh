#! /usr/bin/env bash
# Bug 20 "hwut --fail" was not working. 
#
# When called with "hwut --fail" hwut would consider all files not only 
# the failed ones. 
#
# Root cause: The check for interview time was wrong. Hwut always interviewed
# the application and generated a new entry in the test dabases with new 
# 'innocent' content. 
#
# Now: hwut's checks are adapted. it also overtakes the choices for failed 
#      tests.
#
# fix&test by: 14y08m01 fschaef
#______________________________________________________________________________
arg=$1
test_id=20
source ./hwut_greet.sh "Bug $test_id" \
         fschaef \
         'Dysfunctional: hwut --fail' \
         'CHOICES: untouched, touched, normal-info;'

# We do not HAVE to use 'hwut_call.sh' if the output is omitted anyway.
# Here, HWUT is called directly.
export HWUT_TEST_DIR_NAME=$test_id
export HWUT_TERMINAL_WIDTH=80

case $1 in 
    untouched)
        echo "Do not touch 'good.sh', 'bad.sh', and 'both.sh'"
    ;;
    touched)
        echo "Modify (not only touch) 'good.sh', 'bad.sh', and 'both.sh'"
        echo 
        pushd $test_id >& /dev/null
        for file in good.sh bad.sh both.sh; do
            rm -f $file >& /dev/null
            cp original-$file $file >& /dev/null
            chmod 777 $file >& /dev/null
            echo "# $(date +%yy%mm%dd-%Hh%M)" >> $file
        done
        popd >& /dev/null
    ;;
    normal-info)
        ./hwut_call.sh $test_id i
        exit 0
    ;;
esac

# Following is necessary, in order enable parallelism
interview_file_name=$(mktemp)
if -z "$interview_file_name"; then
    echo "'mktemp' is not installed. On windows try package 'msys-mktemp'"
    exit
fi
echo "##  file: $interview_file_name"
echo $interview_file_name > $test_id/interview_file_name.txt

# Applications in the directory fill 'interview.txt' in case
# that hwut interviews them.
rm -f $interview_file_name >& /dev/null

echo "(*) Test"
source ./hwut_call.sh $test_id --fail

echo "(*) Info"
source ./hwut_call.sh $test_id i --fail

echo "(*) HWUT's interviews:"
echo "##  wc:   $(wc $interview_file_name)"
if [ -e $interview_file_name ]; then
    cat $interview_file_name 
    rm -f $interview_file_name
fi

echo "<Test Done>"

