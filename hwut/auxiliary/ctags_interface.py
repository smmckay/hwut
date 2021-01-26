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
# For further information see http://www.genivi.org/. 
#------------------------------------------------------------------------------
import hwut.auxiliary.executer    as executer
import hwut.auxiliary.file_system as fs
import hwut.common                as common

from   collections import defaultdict
import os

def do(RootDirectoryList, Language, HeaderSymbolsF=False, ExtensionList=None):
    """Invokes the 'ctags' utility in order to find the implementation of
    references.

    RootDirectoryList -- list of root directories from where the search for 
                         files shall begin.

    Language -- search for implementations will be restricted to a certain
                language.
    """
    Language = Language.lower()
    assert Language in ("c",)

    ctags_app = common.get_ctags_application()
    if ctags_app is None: return None

    # It is not clear, whether ctags generates a 'tags' or a 'TAGS' file. 
    # So, for the moment, try to move both old files away, if they exist. 
    backup_tags = fs.move_away("tags")
    backup_TAGS = fs.move_away("TAGS")

    # Use 'etags' output format because it is more dense and faster to
    # parse.
    cmd_line  = ctags_app 
    cmd_line += ["-R", "-e", "--languages=%s" % Language] 
    if HeaderSymbolsF: 
        cmd_line += [ 
            # +p --> function prototypes
            # +x --> external and forward variable declarations
            # +l --> local variables
            "--%s-kinds=+p+x+l" % Language.lower(),
            # .h   --> header filers
            # .cfg --> configuration files
            "--langmap=c:%s" % "".join(ExtensionList)
        ]
    cmd_line += [ os.path.normpath(f) for f in RootDirectoryList]
    executer.do(cmd_line)

    fh     = fs.open_one_or_die(["TAGS", "tags"], "rb")
    if fh is None:
        print "Error: 'ctags' failed to generate 'tags' or 'TAGS' file."
        return {}

    result = parse_etags_file(fh)

    fs.rename_file(backup_tags, "tags")
    fs.rename_file(backup_TAGS, "TAGS")

    return result

def reference_source_iterable(RootDirectoryList, Language, 
                              HeaderSymbolsF=False, ExtensionList=None):
    source_db = do(RootDirectoryList, Language, HeaderSymbolsF, ExtensionList)

    for reference, source_file_set in source_db.iteritems():
        for file_name in source_file_set:
            yield reference, file_name

def parse_etags_file(fh):
    """Parses an output file of 'ctags' in 'etags' format. 

    RETURNS: Database mapping

             reference --> set of files that contain it.
    """
    def get_file_name(line):
        i = line.find(",")
        if i == -1: return None
        else:       return line[:i]

    def get_reference(line):
        begin_i = line.find("\x7f")            # Begin of identifier marker
        end_i   = line.find("\x01", begin_i+1) # End of identifier marker
        if begin_i == -1 or end_i == -1: return None
        elif begin_i + 1 >= end_i:       return None
        else:                            return line[begin_i+1:end_i]
            
    db        = defaultdict(set)
    file_name = None
    reference = None
    while 1 + 1 == 2:
        line = fh.readline()
        if not line: break
        elif line[0] == "\x0C":
            line      = fh.readline()
            file_name = get_file_name(line)
        elif file_name is not None:
            reference = get_reference(line)
            if reference is not None:
                db[reference].add(file_name)

    return db



    
