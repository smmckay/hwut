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
import hwut.code_generation.generator.parser.core                 as     parser
import hwut.code_generation.generator.language.c.header           as     header
import hwut.code_generation.generator.language.c.source           as     source
import hwut.code_generation.sm_walker.language.c.header_sm_walker as     header_sm_walker
import hwut.code_generation.sm_walker.language.c.source_sm_walker as     source_sm_walker
from   hwut.code_generation.generator.types                       import E_Generator
from   hwut.code_generation.generator.array_db                    import ArrayDb
import hwut.common                                                as     common

from operator    import attrgetter
from collections import defaultdict

def do(FileName, FileStemSuffix):
    """(1) Parse generator description in 'FileName'
       (2) Generate the iterator implementation.
    """
    assert isinstance(FileName, (str, unicode))

    generator_db = parser.do_file(FileName)

    if len(generator_db) == 0:
        print "No generator found in file '%s'" % FileName
        return

    db = defaultdict(list)
    for name, info in generator_db.iteritems():
        generator_type = info[0]
        info_db = info[-1]
        db[generator_type].append(info)

    for generator_type, info_list in db.iteritems():

        file_stem = get_file_stem(generator_type)

        function = { 
            E_Generator.GENERATOR: implement_generator,
            E_Generator.SM_WALKER: implement_sm_walker,
            E_Generator.RACER:     implement_racer,
        }[generator_type]

        header_content, source_content = function(file_stem, info_list)

        write_header("%s.h" % file_stem, header_content)
        write_source("%s.c" % file_stem, source_content)

def write_header(FileName, Text):
    def safe(Name):
        result = []
        for letter in Name:
            if letter.isalpha(): result.append(letter)
            else:                result.append("_")
        return "".join(result)
        
    fh = open(FileName, "wb")
    fh.write(  "#ifndef INCLUDE_GUAGE_HWUT_GENERATOR_%s\n" % safe(FileName)
             + "#define INCLUDE_GUAGE_HWUT_GENERATOR_%s\n" % safe(FileName))
    fh.write(Text)
    fh.write("#endif /* INCLUDE_GUAGE_HWUT_GENERATOR_%s */\n" % safe(FileName))
    fh.close()

def write_source(FileName, Text):
    fh = open(FileName, "wb")
    fh.write(Text)
    fh.close()

def get_file_stem(GeneratorType):
    file_stem = common.setup.output_file_stem
    if   file_stem:                              return file_stem
    elif GeneratorType == E_Generator.GENERATOR: return "hwut_generated_iterator"  
    elif GeneratorType == E_Generator.SM_WALKER: return "hwut_generated_sm_walker"
    elif GeneratorType == E_Generator.RACER    : return "hwut_generated_racer"   
    else:                                        assert False

def implement_generator(FileStem, InfoList):
    """Implements the code of a iterator which iterates over the
    given SectionList.
    """ 
    header_txt = ""
    source_txt = ""
    for info in InfoList:
        generator_type, source_header, section_list, info_db = info

        array_db = get_array_db(section_list)
        format_focus_expressions(section_list)
        header_txt += "%s\n" % source_header
        header_txt += "%s\n" % header.do(info_db["name"], section_list, array_db)
        source_txt += source.do(info_db["name"], section_list, array_db, FileStem)

    return header_txt, source_txt

def implement_sm_walker(FileStem, InfoList):
    sm_walker_list = [ x[2] for x in InfoList ]
    source_header  = "".join(x[1] for x in InfoList)

    # source_sm_walker prepares global_id in states.
    source_txt, event_id_db, condition_id_db = source_sm_walker.do(sm_walker_list)
    header_txt  = "%s\n" % source_header
    header_txt += "%s\n" % header_sm_walker.do(sm_walker_list, event_id_db, condition_id_db)

    source_txt  = "#include \"%s.h\"\n" % FileStem + source_txt
    
    return header_txt, source_txt

def implement_racer(FileStem, InfoList):
    # TODO
    pass

def get_array_db(SectionList):
    result = ArrayDb()

    for section in SectionList:
        if hasattr(section, "setting_list"):
            for setting in section.setting_list:
                result.absorb(setting)
        else:
            result.absorb(section.parameter_list)

    return result

def format_focus_expressions(SectionList):
    # Search for the longest names first, for safety to avoid replacing 
    # parts of larger names.
    name_re_list = [
       (common.re_compile("\\b%s\\b" % p.name), p.name)     
       for p in sorted(SectionList[0].parameter_list, key=attrgetter("name"), reverse=True)
    ]
    def iterable(SectionList):
        for section in SectionList:
            if hasattr(section, "setting_list"): continue
            for p in section.parameter_list:
                if not hasattr(p, "focus"): continue
                yield p

    for p in iterable(SectionList):
        for entry in name_re_list:
            p.focus = entry[0].sub("it->%s" % entry[1], p.focus)
            
            
        
            
        
