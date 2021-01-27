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
import hwut.auxiliary.file_system                      as fs
from   hwut.code_generation.function_stubs.c.core      import extract_argument_list
import hwut.code_generation.generator.parser.generator as     generator
import hwut.code_generation.sm_walker.parser.sm_walker as     sm_walker
from   hwut.code_generation.generator.types            import E_Generator
from   collections import defaultdict


def do_file(FileName):
    fh = fs.open_or_die(FileName, "rb")
    return do_file_handle(fh)

def do_file_handle(fh):
    generator_db     = {}
    output_file_stem = None
    while 1 + 1 == 2:
    
        generator_type, \
        info_db         = find_begin(fh, output_file_stem)

        if generator_type is None: 
            break
        elif info_db["name"] in generator_db:
            print "Error: generator name has been used before"

        source_header = generator.snap_until_dash_line(fh)

        if generator_type == E_Generator.GENERATOR:
            section_list = generator.do(fh)
        elif generator_type == E_Generator.SM_WALKER:
            section_list = sm_walker.do(fh, info_db)
        else:
            assert False

        generator_db[info_db["name"]] = [
            generator_type, source_header, section_list, info_db
        ]
    
    return generator_db
        
def find_begin(fh, output_file_stem):
    """RETURNS: [0] Generator Type
                [1] info_db containing basic parameters for the code generator.
    """
    marker_gen       = "<<hwut-iterator:"
    marker_sm_walker = "<<hwut-sm_walker:"
    marker_racer     = "<<hwut-racer:"
    marker_file      = "<<hwut-file:"      # Ignored since 0.20.4; see comment below!
    info_db          = {}
    generator_type   = None
    while not generator.is_dash_line(fh): 
        line = fh.readline()
        if len(line) == 0:
            return None, None
        elif line.find(marker_gen) != -1:
            generator_type = E_Generator.GENERATOR
            content         = generator.get_marker_content(line, marker_gen, 1)
            info_db["name"] = content[0]
        elif line.find(marker_sm_walker) != -1:
            generator_type = E_Generator.SM_WALKER
            content                    = generator.get_marker_content(line, marker_sm_walker, 4)
            info_db["name"]            = content[0]
            info_db["user_data_type"]  = content[1]
            info_db["max_path_length"] = int(content[2])
            info_db["max_loop_n"]      = int(content[3])
        elif line.find(marker_racer) != -1:
            generator_type  = E_Generator.RACER
            content         = generator.get_marker_content(line, marker_racer, 1)
            info_db["name"] = content[0]
        elif line.find(marker_file) != -1:
            print "Error: maker '<<hwut-file: ...>>' is ignored since version 0.20.4."
            print "Error: use '-o file-stem' on command line instead."
            
    fh.readline()
            
    if info_db.get("name") is None:
        print "Error: no marker found (Expected '<<%s: ... >>' or '<<%s: ...>>' or '<<%s: ..>>'." \
              % (marker_gen, marker_sm_walker, marker_racer)

    return generator_type, info_db



