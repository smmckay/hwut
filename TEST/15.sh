#! /usr/bin/env bash
# Bug 15 describes a case, where the actual output is empty while
#        the GOOD output is only one line long. This was a special
#        case where the comparison failed. It id not consider the
#        last read GOOD line.
#
# fix&test by: 14y08m01 fschaef
#______________________________________________________________________________
arg=$1
test_id=15
source ./hwut_greet.sh "Bug $test_id" \
                       stephanhengefel \
                       'False Possitive'
source ./hwut_call.sh $test_id CMD:clean
