# PURPOSE: Cleaning the directory tree from useless things.
#
# (C) 2007-2015 Frank-Rene Schaefer  fschaef@users.sourceforge.net
# 
# ABSOLUTELY NO WARRANTY
#
###########################################################################


# -- filter out all files that are not directly required for 
#    a working application.
extension_list="svn o obj exe pyc pyo bak orig swo swp stackdump 7z backup orig tgz tbz zip pdf ps"
path_list="TEST\/OUT TEST\/f?[0-9]+\/OUT doc\/manual\/build TEST\/htmlcov dumpster"
# path_list="TEST TEST-old TEST\/OUT TEST\/f?[0-9]+\/OUT doc\/manual\/build TEST\/htmlcov dumpster " 
file_list="tmp\.[a-z]+\$ stats.log\$ core\$ °$ *~\$ TEST\/ADM\/cache\.fly\$"

txt0=$(for x in $(echo "$extension_list"); do printf "/\.%s$/ || " $x; done; echo) 
txt1=$(for x in $(echo "$path_list"); do      printf "/\/%s\// || " $x; done; echo) 
txt2=$(for x in $(echo "$file_list"); do      printf "/\/%s/ || " $x; done; echo)
txt_end="/\/nOnSeNse.txt/ { print; }"

find -type f | awk "$txt0 $txt1 $txt2 $txt_end" 
