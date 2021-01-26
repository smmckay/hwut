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
from   hwut.common import HWUT_PATH
import hwut.auxiliary.file_system as fs
from   hwut.code_generation.sm_walker.sm_walker import condition_interpret

from operator import itemgetter, attrgetter

def do(SmWalkerList, event_id_db, condition_id_db):
    return "".join(do_walker(walker, event_id_db, condition_id_db) 
                   for walker in SmWalkerList)

def do_walker(walker, event_id_db, condition_id_db):
    template_file_name = HWUT_PATH + "/hwut/code_generation/sm_walker/language/c/templates/sm_walker.hg"
    txt = fs.read_or_die(template_file_name)

    # Generating the 'source' before this makes sure that the walkers are 
    # setup propperly
    my_event_id_db = dict(
        (name[1], identifier) 
        for name, identifier in event_id_db.iteritems() if name[0] == walker.name
    )

    def condition_def(Name, Identifier):
        condition_name, not_f = condition_interpret(Name)
        if not_f: identifier = -Identifier
        else:     identifier = Identifier
        return (condition_name, identifier)
        
    my_condition_id_db = dict(
        condition_def(name[1], identifier) 
        for name, identifier in condition_id_db.iteritems() 
        if name[0] == walker.name and name[1] is not None
    )

    if my_event_id_db:
        L = max(len(str(name)) for name in my_event_id_db.iterkeys())
        event_defs = "".join(
            "    %s_%s %s= %i,\n" % (walker.name, name, " " * (L-len(str(name))), identifier)
            for name, identifier in sorted(my_event_id_db.iteritems(), key=itemgetter(1))
        )
        event_defs = "".join([
            "typedef enum {\n",
            event_defs,
            "} $$NAME$$_event_id_t;\n"
        ])
    else:
        event_defs = "/* No events */"

    if my_condition_id_db:
        L = max(len(str(name)) for name in my_condition_id_db.iterkeys())
        condition_defs = "".join(
            "    %s_%s %s= %i,\n" % (walker.name, name, " " * (L-len(str(name))), identifier)
            for name, identifier in sorted(my_condition_id_db.iteritems(), key=itemgetter(1))
        )
        condition_defs = "".join([
            "typedef enum {\n",
            condition_defs,
            "} $$NAME$$_condition_id_t;\n"
        ])
    else:
        condition_defs = "/* No conditions */"

    L = max(len(str(state.name)) for state in walker.state_list)
    name_beyond_id = "__BeyondId"
    if len(name_beyond_id) > L: L = len(name_beyond_id)

    state_id_defs = "".join(
        "    %s_%s %s= %i,\n" \
        % (walker.name, state.name, " " * (L-len(str(state.name))), state.global_id)
        for state in sorted(walker.state_list, key=lambda x: x.global_id)
    )
    real_limit = max(x.global_id for x in walker.state_list) + 1
    for state in sorted(walker.state_list, key=lambda x: x.global_id):
        if state.intermediate_f: real_limit = state.global_id; break
    state_id_defs += "    %s_%s %s= %i, /* Any state below is 'real' */\n" \
                     % (walker.name, name_beyond_id, " " * (L-len(str(name_beyond_id))), 
                        real_limit)

    condition_n = len(my_condition_id_db)
    if not condition_n: condition_n = 1
    state_n     = len(walker.state_list)
    txt = txt.replace("$$EVENT_DEFS$$",     event_defs)
    txt = txt.replace("$$CONDITION_DEFS$$", condition_defs)
    txt = txt.replace("$$STATE_N$$",        "%i" % state_n)
    txt = txt.replace("$$CONDITION_N$$",    "%i" % condition_n)
    txt = txt.replace("$$NAME$$",           walker.name) 
    txt = txt.replace("$$MAX_PATH_SIZE$$",  "%i" % walker.max_path_length)
    txt = txt.replace("$$MAX_LOOP_N$$",     "%i" % walker.max_loop_n)
    txt = txt.replace("$$USER_DATA_TYPE$$", walker.user_data_type)
    txt = txt.replace("$$SPACE$$",          " " * len(walker.name))
    txt = txt.replace("$$STATE_ID_DEFS$$",  state_id_defs)
    return txt

    
