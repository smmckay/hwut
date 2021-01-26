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
# SPDX license identifier: LGPL-2.1
#
# Copyright (C) Frank-Rene Schaefer, private.
# Copyright (C) Frank-Rene Schaefer, 
#               Visteon Innovation&Technology GmbH, 
#               Kerpen, Germany.
#
# This file is part of "HWUT -- The hello worldler's unit test".
#
#                  http://hwut.sourceforge.net
#
# This file is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this file; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA
#
#------------------------------------------------------------------------------
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

