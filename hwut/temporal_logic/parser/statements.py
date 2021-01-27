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
import hwut.auxiliary.file_system                       as fs
from   hwut.temporal_logic.classes.world                import EventOrigin
from   hwut.temporal_logic.parser.lilli_peg             import _alternatives, Chain, Repeat, Regress, node_cache
from   hwut.temporal_logic.classes.primary              import *
from   hwut.temporal_logic.classes.event                import *
from   hwut.temporal_logic.classes.time_span            import *
from   hwut.temporal_logic.classes.statement            import *
from   hwut.temporal_logic.classes.rule                 import *
from   hwut.temporal_logic.classes.action               import *
from   hwut.temporal_logic.classes.action_function_call import *
from   hwut.temporal_logic.classes.control              import *
from   hwut.temporal_logic.classes.statement_element    import Fork
from   hwut.temporal_logic.parser.statements            import *
import sys
import os

import hwut.temporal_logic.parser.lexical_analysis as lex

def register_input_source(Filename, LineN=0):
    node_cache.clear()
    lex.__current_file_name = Filename
    lex.__current_line_n    = LineN

def event_iterable(sh, world):
    while 1 + 1 == 2:
        event_trigger, origin = snap_event_occurence(sh)

        if origin is None: world.time_update(-1.0)
        else:              world.time_update(origin.time)

        if event_trigger is None:
            if  origin is None: break
            else:               continue

        event = event_trigger.execute(world)

        if type(event) == list:
            for x in event: 
                if origin is not None: x.set_origin(origin)
                yield x
        else:
            if origin is not None: event.set_origin(origin)
            yield event

    return

def snap_event_occurence(sh):
    result = _alternatives(sh, 
        [[snap_reported_origin, ":", snap_event_trigger], "EventOrigin_Event"],
        [[snap_reported_origin],                          "EventOrigin"      ],
        [[snap_event_trigger],                            "Event"            ],
    )
    if result.error() or result is None:
        return None, None

    if   result.name == "EventOrigin_Event": event_trigger = result.sub_node_list[1]
    elif result.name == "EventOrigin":       event_trigger = EventTrigger("")
    elif result.name == "Event":             event_trigger = result.sub_node_list[0]
    else:                                    assert False

    if   result.name == "EventOrigin_Event": event_origin  = result.sub_node_list[0]
    elif result.name == "EventOrigin":       event_origin  = result.sub_node_list[0]
    elif result.name == "Event":             event_origin  = None
    else:                                    assert False

    return event_trigger, event_origin
    
def snap_reported_origin(sh):
    return _alternatives(sh,
        [[lex.string, ":", lex.number, ":", lex.number], EventOrigin], 
        [[lex.string, ":", lex.number],                  EventOrigin], 
        [[lex.number],                                   EventOrigin], 
    )

def snap_object_list(sh):
    return _alternatives(sh,
        # [["[", Chain([snap_term], [",", snap_term]), "]"],    None],
        [["[", Chain([snap_term], [",", snap_term]), "]"],    Primary_CollectionList],
        # NOTE: Chain(X, [",", Y]) == [X, Repeat([Y, Z])]
        #       only the result is a single list consisting of results
        #       [X, Y, Z, Y, Z] ....
        #       The results of the right approach is
        #       [X, [Y, Z,], [Y, Z]] ....
    )

def snap_object_dictionary(sh):
    return _alternatives(sh,
        [["{", Chain([snap_key_value_pair], [",", snap_key_value_pair], 0), "}"],  Primary_CollectionMap],
    )

def snap_key_value_pair(sh):
    return _alternatives(sh,
        [[lex.string, ":", snap_term], "StringKeyValuePair"],
        [[lex.number, ":", snap_term], "NumberKeyValuePair"],
    )

def snap_assignment(sh):
    return _alternatives(sh,
        [[snap_lvalue, ["=", "+=", "-=", "*=", "/=", "<<=", ">>=", "&=", "|=", "^="], snap_term, ";"], Action_BinaryOp], 
        [[snap_lvalue, ["=", ], snap_function_definition, ";"],                                        Action_BinaryOp], 
        [[snap_lvalue, ["=", ], lex.variable_name, ";"],                                               Action_BinaryOp], 
    )

def snap_event_trigger(sh): 
    SourceOrigin = lex.origin(sh, sh.tell())
    return _alternatives(sh,
        [["{", Repeat([snap_event_trigger]), "}"],             EventTrigger_List, [SourceOrigin]], 
        [[lex.event_name, ";"],                                EventTrigger,      [SourceOrigin]], 
        [[lex.event_name, "(", snap_adornment_list, ")", ";"], EventTrigger,      [SourceOrigin]], 
    )

def snap_adornment_list(sh):
    return _alternatives(sh,
        [[Chain([snap_adornment], [",", snap_adornment])],  "AdornmentList"], 
    )

def snap_adornment(sh):
    return _alternatives(sh,
        [[lex.identifier, "=", snap_term], EventTrigger_Adornment], 
        [[snap_term],                      EventTrigger_Adornment], 
    )

def snap_term(sh):
    """The 'correct' grammar rule to parse for example 'a - b + c' would be 
       
       term: term +/- expr 
             expr

       However, this is not possible with right-descendent parsers. Indeed it 
       would cause an infinite recursion. The grammar rule

       term: expr +/- term
             expr

       can avoid infinite recursion but it constructs the nodes in a wrong order.
       The term 'a - b + c' would be represented by

              a    b
             /    /
           (-)--(+)-- c

       because nodes are created at the end of the descendence. The result would
       correspond to 'a - (b + c)' which is not 'a - b + c'. The binary chain
       allows to create a structure like

           (+)--(-)--a
             \    \
              c    b
    """
    return _alternatives(sh, 
        [[Regress(snap_expr, ["+", "-"], snap_expr)],  None]
    )

def snap_expr(sh):
    return _alternatives(sh,
        [[snap_object, ["**", "*", "/", "%"], snap_expr], Action_BinaryOp], 
        [[snap_object],                                   None], 
    )

def snap_object(sh):
    return _alternatives(sh,
        [[snap_primary, Repeat([snap_object_access])],  Action_ObjectAccess], 
        [[snap_event, Repeat([snap_object_access], 1)], Action_ObjectAccess], 
        [[snap_event, ],                                Action_Op("$verdict-event-occured")], 
    )

def snap_object_access(sh):
    return _alternatives(sh,
        [["[", snap_term, "]"],                 Action_Op("$element-access")], 
        [["[", snap_term, ":", snap_term, "]"], Action_Op("$element-range-access")], 
        [[".", "size", "(", ")"],               Action_Op("$size")], 
        [[".", "has", "(", snap_term, ")"],     Action_Op("$has")], 
        [[".", "key", "(", snap_term, ")"],     Action_Op("$key")], 
        [[".", "delete", "(", snap_term, ")"],  Action_Op("$delete")], 
        [[".", "split", "(", snap_term, ")"],   Action_Op("$split")], 
        [[".", "replace", "(", snap_term, ", ", snap_term, ")"],   Action_Op("$replace")], 
        [[".", "time_in_state", "(", ")"],      Action_Op("$member-time-in-state")], 
        [[".", "time", "(", ")"],               Action_Op("$member-time")], 
        [[".", "count", "(", ")"],              Action_Op("$member-count")], 
        [[".", lex.identifier],                 Action_Op("$event-adornment")],
        [["(", snap_adornment_list, ")"],       Action_OpCall], 
    )

def snap_event(sh):
    return _alternatives(sh,
        [[lex.event_name],  None], 
    )

def snap_lvalue(sh):
    return _alternatives(sh, 
        [[lex.variable_name, Repeat([snap_object_access])],  Action_ObjectAccess], 
    )

def snap_function_definition(sh):
    SourceOrigin = lex.origin(sh, sh.tell())
    result = _alternatives(sh, 
        [["function", snap_function_header,  ":", "{", Repeat([snap_basic_rule], 0), "}"], Primary_FunctionDefinition, [SourceOrigin]], 
    )
    return result

def snap_function_header(sh):
    result = _alternatives(sh,
        [["(", Chain([lex.variable_name], [",", lex.variable_name], 0), ")"], Fork],
    )
    return result

def snap_basic_rule(sh):
    SourceOrigin = lex.origin(sh, sh.tell())
    return _alternatives(sh,
         [["if",       snap_condition, ":", snap_basic_rule, snap_else],        Control_IfElse,        [SourceOrigin]], 
         [["if",       snap_condition, ":", snap_basic_rule],                   Control_IfElse,        [SourceOrigin]], 
         [["send",     snap_event_trigger],                                     Action_Op("$send")], 
         [["freeze",   snap_namespace_specifier, ";"],                          Action_Op("$freeze")], 
         [["unfreeze", snap_namespace_specifier, "shallow", ";"],               Action_Op("$unfreeze-shallow")], 
         [["unfreeze", snap_namespace_specifier, ";"],                          Action_Op("$unfreeze")], 
         [["for", lex.variable_name, "in", snap_term, ":", snap_basic_rule],    Control_ForLoop,       [SourceOrigin]],
         [["switch", snap_term, ":", "{", Repeat([snap_switch_case], 1), "}"],  Control_Switch,        [SourceOrigin]],
         [[snap_assignment],                                                    None], 
         [[snap_condition, ";"],                                                Action_ConditionTest,  [SourceOrigin]], 
         [[snap_print],                                                         None], 
         [["{", Repeat([snap_basic_rule], 0), "}"],                             Rule_List,             [SourceOrigin]], 
    )

def snap_rule_list(sh):
    return _alternatives(sh,
        [[Repeat([snap_rule])],    None], 
    )

include_stack = []
def snap_import(sh):
    global include_stack

    SourceOrigin = lex.origin(sh, sh.tell())
    result = _alternatives(sh,
        [["import", lex.string, "as", snap_namespace_specifier, ";"], Fork], 
        [["import", lex.string, ";"],                                 Fork], 
    )
    if result.error(): return result

    # Store the current file status
    prev_line_n    = lex.__current_line_n
    prev_file_name = lex.__current_file_name
    prev_sh        = sh

    if len(result.sub_node_list) > 1: namespace = result.sub_node_list[1]
    else:                             namespace = Fork([])
    file_name = result.sub_node_list[0].content

    # Ensure that there is no circular inclusion
    if file_name in include_stack: 
        print "%s:%i: Circular inclusion file '%s' is included from '%s'" % (prev_file_name, prev_line_n, file_name, prev_file_name)
        for name in include_stack[1:]:
            print "%s:%i: '%s' is included from '%s'" % (prev_file_name, prev_line_n, prev_file_name, name)
            prev_file_name = name
        sys.exit(-1)

    # Open the new file
    if os.access(file_name, os.F_OK) == False:
        print "%s:%i: File %s cannot be found." % (prev_file_name, prev_line_n, file_name)
        sys.exit(-1)

    include_stack.append(file_name)
    sh = fs.open_or_die(file_name, Mode="rb")
    register_input_source(file_name)

    # Read new content
    sub_result = snap_rule_list(sh)

    # Reset the old file status
    register_input_source(prev_file_name, prev_line_n)
    sh = prev_sh

    # Setup the real result as a rule set (namespace == empty).
    real_result = Primary_Namespace([SourceOrigin, namespace, sub_result])

    # Maybe, the user wanted to import the file under a specific namespace
    if len(result.sub_node_list) == 1: 
        return real_result # Done, no namespace adaptions.

    # The rule list is actually the rule list of the included file
    return real_result

def snap_namespace_specifier(sh):
    SourceOrigin = lex.origin(sh, sh.tell())
    return _alternatives(sh,
        [[Chain([lex.identifier], [".", lex.identifier], 0)], None, [SourceOrigin]], 
    )

def snap_namespace(sh):
    SourceOrigin = lex.origin(sh, sh.tell())
    return _alternatives(sh,
        [["space", snap_namespace_specifier, ":", snap_rule],                Primary_Namespace, [SourceOrigin]], 
        [["space", snap_namespace_specifier, ":", "{", snap_rule_list, "}"], Primary_Namespace, [SourceOrigin]], 
    )

def snap_state_machine(sh):
    SourceOrigin = lex.origin(sh, sh.tell())
    return _alternatives(sh,
        [["state_machine", Chain([lex.identifier], [",", lex.identifier], 0), ";"], Action_DefineStateMachine, [SourceOrigin]], 
    )

def snap_rule(sh):
    """NOTE: There is a fundamental difference between an event that is triggered via 'on' condition ':'
             and an event that appears in the 'then' block of an 'if' statement. The 'on' triggering
             appears only at a transition from 'false' to 'true' whereas the event in the if statement
             triggers 'all-the-time'.
    """
    return _alternatives(sh,
        [[snap_namespace],     None],
        [[snap_import],        None],
        [[snap_state_machine], None],
        [[snap_rule_core],     None],
    )

def snap_rule_core(sh):
    SourceOrigin = lex.origin(sh, sh.tell())
    return _alternatives(sh,
        [["once",     snap_condition,        ":", snap_basic_rule], Rule_EventCondition,        [SourceOrigin]], 
        [["on",       snap_event_spec_list,  ":", snap_basic_rule], Rule_EventHandler,          [SourceOrigin]], 
        [[snap_time_span,                    ":", snap_basic_rule], Rule_TemporalCondition,     [SourceOrigin]], 
        [[snap_basic_rule],                                         Rule_AbsoluteCondition,     [SourceOrigin]], 
    )

def snap_else(sh):
    SourceOrigin = lex.origin(sh, sh.tell())
    return _alternatives(sh,
        [["elif", snap_condition, ":", snap_basic_rule, snap_else], Control_IfElse, [SourceOrigin]], 
        [["elif", snap_condition, ":", snap_basic_rule],            Control_IfElse, [SourceOrigin]], 
        [["else",                 ":", snap_basic_rule],            None,           [SourceOrigin]], 
    )

def snap_switch_case(sh):
    result = _alternatives(sh,
        [[lex.cmp, snap_term, ":", snap_basic_rule], Control_SwitchCase],
        [["else",             ":", snap_basic_rule], None],
    )
    return result

def snap_event_spec_list(sh):
    return _alternatives(sh,
        [[Chain([snap_event_spec],  [",", snap_event_spec], 0)], None], 
    )

def snap_event_spec(sh):
    return _alternatives(sh, 
        [[lex.event_name,  "->", lex.event_name],  "StateTransition"], 
        [[lex.event_name],                         None],
    )

def snap_time_span(sh):
    return _alternatives(sh,
        [["from", snap_condition, "to", snap_condition], TimeSpan_FromTo], 
        [["from", snap_condition],                       TimeSpan_From], 
        [["to",   snap_condition],                       TimeSpan_To], 
    )

def snap_condition(sh):
    return  _alternatives(sh, 
         [[snap_condition_expression, ["or"], snap_condition], Action_BinaryOp], 
         [[snap_condition_expression],                         None]
    )

def snap_condition_expression(sh):
    return  _alternatives(sh, 
         [[snap_condition_primary, ["and"], snap_condition_expression], Action_BinaryOp], 
         [[snap_condition_primary],                                     None]
    )

def snap_condition_primary(sh):
    return  _alternatives(sh, 
         [[snap_term, lex.cmp,  snap_term], Action_BinaryOp], 
         [[snap_term],                      Action_Op("$verdict-conversion")], 
         [["(", snap_condition, ")"],       None], 
         [["not", snap_condition],          Action_Op("$verdict-inversion")]
    )
    
def snap_print(sh):
    pos = sh.tell()
    SourceOrigin = lex.origin(sh, pos)
    result = _alternatives(sh,
        [["print", Chain([snap_term], [",", snap_term], 0), ";"], Action_Print, [SourceOrigin]], 
    )
    
    if result.error(): return result

    pos_end = sh.tell()
    sh.seek(pos)
    term_str = sh.read(pos_end - pos)
    result.set_original_str(term_str)

    return result

def snap_primary(sh):
    return _alternatives(sh,
        [["true", "false"],                      Primary_Bool],
        [[lex.number],                           None], 
        [[lex.string],                           None], 
        [[snap_object_dictionary],               None],
        [[snap_object_list],                     None],
        [[lex.variable_name],                    None],
        [[lex.event_name, "->", lex.event_name], Primary_StateTransition], 
        [["(", snap_term, ")"],                  None], 
    )

