# PURPOSE: Creating a release of Quex
#   $1  version of the hwut release
#
# (C) 2007 Frank-Rene Schaefer  fschaef@users.sourceforge.net
# 
# ABSOLUTELY NO WARRANTY
#
###########################################################################
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

