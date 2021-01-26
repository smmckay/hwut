# This file calls HWUT from within a cygwin environment. It is the third 
# stage in a HWUT dos to cygwin bridge:
#
#      DOS --> hwut2cygwin.bat --> cygwin --> hwut2cygwin.sh --> hwut 
#
# ARGUMENTS:
#
# $1  -- Directory from where the HWUT dos-cygwin bridge has been invoqued.
#
# ... -- remaining argument which are supposed to be passed to HWUT.
# 
# (C) Frank-Rene Schaefer
#______________________________________________________________________________
work_dir=$1
hwut_dir=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)
shift

# (1) HWUT Setup 

# -- setup HWUT_PATH
#    (The place of this script is the HWUT_PATH)
export HWUT_PATH=$(readlink -e $hwut_dir)

pwd_dir=$(readlink -e $work_dir)

# (3) Call hwut with the remaining arguments.
cd $pwd_dir
$HWUT_PATH/hwut-exe.py $*

