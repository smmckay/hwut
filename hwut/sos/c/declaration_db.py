# SPDX license identifier: LGPL0.1
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
import hwut.sos.implementation_db     as     base
import hwut.io.select                 as     select
import hwut.auxiliary.path            as     path
import hwut.auxiliary.file_system     as     fs
import hwut.auxiliary.ctags_interface as     ctags
import hwut.sos.c.system              as     system

from   collections import defaultdict, namedtuple
from   operator    import itemgetter


import os
from   copy import copy
import re

re_quoted_string = re.compile('\"[^"]+\"')


class DeclarationDb:
    """Database containing information about what references are present in
    what files. 

    Objects of this class are constructed via one of the following:

                DeclarationDb.with_ctags()
                DeclarationDb.without_ctags()

    """
    header_extension_list = [".h", ".cfg"]

    @classmethod
    def with_ctags(cls, IdentifierList, IncludePathList):
        identifier_set = set(IdentifierList)

        result = defaultdict(set)
        db     = ctags.reference_source_iterable(IncludePathList, "c", 
                                                 HeaderSymbolsF=True, 
                                                 ExtensionList = DeclarationDb.header_extension_list)
        for reference, file_name in db:
            if reference not in identifier_set: continue 
            result[reference].add(file_name)

        return DeclarationDb._disambiguify(result)

    @classmethod
    def without_ctags(cls, IdentifierList, IncludePathList):
        regex_list = [
            (identifier, re.compile("\\b%s\\b" % identifier))
            for identifier in IdentifierList
        ]

        def content_iterable(IncludePathList):
            for directory in IncludePathList:
                for f in path.files_of_directory(directory, DeclarationDb.header_extension_list):
                    # TRICK: Preprocess with empty include list. The pre-
                    #        processor will extract all comments propperly.
                    txt = fs.read_or_die(f)
                    candidate_list = [
                        identifier 
                        for identifier in IdentifierList if identifier in txt
                    ]
                    if not candidate_list:
                        continue
                    txt = delete_string_constants(txt)
                    for identifier, regex in regex_list:
                        if identifier not in candidate_list: 
                            continue
                        if regex.search(txt) is not None:
                            yield f, identifier

        result = defaultdict(set)
        for file_name, identifier in content_iterable(IncludePathList):
            result[identifier].add(file_name)

        return DeclarationDb._disambiguify(result)

    @staticmethod
    def _disambiguify(db):
        result_db = {}
        for identifier, file_name_set in db.iteritems():
            if not file_name_set:       
                continue

            elif len(file_name_set) == 1:                 
                file_name = next(iter(file_name_set))

            else:
                # If there is a directory in 'file_name_set' that has already 
                # been chosen, then take that. 
                for f in file_name_set:
                    if f not in result_db.itervalues(): continue
                    file_name = f
                    break
                else:
                    file_list     = [path.relative(x) for x in file_name_set]
                    choice_index, \
                    dummy         = select.implementation(identifier, file_list, 
                                                          CrashOnCallF=False, 
                                                          PreferenceOptionF=False)
                    if choice_index is None: continue
                    file_name     = file_list[choice_index]

            result_db[identifier] = file_name

        return result_db

    @staticmethod
    def get_string(db):
        if not db: return "<empty>"
        
        L = max(len(x) for x in db.iterkeys())
        return "".join(
            "%s: %s%s\n" % (identifier, " "*(L-len(identifier)), file_name_list)
            for identifier, file_name_list in sorted(db.iteritems())
        )


def delete_string_constants(Content):
    # Avoid the problem with quoted strings by deleting them altogether
    content = Content.replace("\\\"", "")

    return re_quoted_string.sub("", content)
