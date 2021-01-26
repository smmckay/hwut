# PURPOSE: 
#
# Generate a response to HWUT that tells something about the 
# bug or feature request in a consistent manner.
#
# ARGUMENTS:
# 
#    $1 bug identifier
#    $2 submitter
#    $3 Title
#    $4 More responses to --hwut-info
# 
# AUTHOR: 14y08m01d fschaef
#______________________________________________________________________________
bug=$1
submitter=$2
title=$3
more=$4
if [ "$arg" = "--hwut-info" ]; then
    echo "$submitter: $bug - $title;"
    echo "$more"
    exit
fi
export HWUT_EXE="python $HWUT_PATH/hwut-exe.py --no-color"

