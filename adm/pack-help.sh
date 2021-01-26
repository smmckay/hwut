# PURPOSE: Creating a release of HWUT
#   $1  version of the hwut release
#
# (C) 2007 Frank-Rene Schaefer  fschaef@users.sourceforge.net
# 
# ABSOLUTELY NO WARRANTY
#
#------------------------------------------------------------------------------
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
orig_directory=`pwd`
directory=`basename $orig_directory`

# (*) Update the version information inside the application
awk -v version="'$1'" ' ! /^HWUT_VERSION/ { print; } /^HWUT_VERSION/ { print "HWUT_VERSION =",version; }' \
    ./hwut/common.py > tmp-common.txt
mv tmp-common.txt ./hwut/common.py

# (*) Collect the list of files under concern
input=/tmp/file-list-in.txt
output=/tmp/file-list-out.txt

cd ..

find $directory/hwut $directory/demo  -type f  > $input
find $directory/ -maxdepth 1 -type f >> $input

# -- filter out all files that are not directly required for 
#    a working application.
awk ' ! /\/\.svn/ { print; }'  $input > $output; cp $output $input
awk ' ! /\/TEST\// { print; }' $input > $output; cp $output $input
awk ' ! /\.o$/ { print; }'     $input > $output; cp $output $input
awk ' ! /\.pyc$/ { print; }'   $input > $output; cp $output $input
awk ' ! /\.pdf$/ { print; }'   $input > $output; cp $output $input
awk ' ! /\~$/ { print; }'      $input > $output; cp $output $input
awk ' ! /\.bak$/ { print; }'   $input > $output; cp $output $input
awk ' ! /\.swo$/ { print; }'  $input > $output; cp $output $input
awk ' ! /\.swp$/ { print; }'  $input > $output; cp $output $input
awk ' ! /\.7z$/ { print; }'  $input > $output; cp $output $input
awk ' ! /\.tgz$/ { print; }'  $input > $output; cp $output $input
awk ' ! /\.tbz$/ { print; }'  $input > $output; cp $output $input
awk ' ! /\.zip$/ { print; }'  $input > $output; cp $output $input

# (*) create packages: .tar.7z, .tar.gz

# -- create tar file for ./trunk
tar cf /tmp/hwut-$1.tar `cat $output`

# -- change base directory from ./trunk to ./hwut-$version
cd /tmp/
tar xf hwut-$1.tar
rm hwut-$1.tar 
mv trunk hwut-$1
tar cf hwut-$1.tar ./hwut-$1

# -- compress the tar file
7z a hwut-$1.tar.7z hwut-$1.tar
gzip -9 hwut-$1.tar

# (*) clean up
rm $input $output

echo "Files are located in /tmp"
cd $orig_directory

# (*) branch on sourceforge subversion
svn copy https://hwut.svn.sourceforge.net/svnroot/hwut/trunk \
         https://hwut.svn.sourceforge.net/svnroot/hwut/tags/hwut-$1 \
         -m Release_$1

