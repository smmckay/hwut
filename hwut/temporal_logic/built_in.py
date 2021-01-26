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
from   hwut.temporal_logic.classes.object   import Object, FunctionObject
import hwut.temporal_logic.log              as     log

import sys
import math

def my_greater(X, Y):
    result = (X > Y)
    return result
    
def my_division(X, Y):
    if Y == 0: return 1e37
    else:      return X / Y

def my_modulo(X, Y):
    if Y == 0: return 1e37
    else:      return X % Y

def my_element_access(Container, Key):

    if Container.type == Object.LIST:
        if Key.type == Object.NUMBER: int_key = int(Key.content)
        else:                         int_key = int(Key.content)
        if int_key >= len(Container.content):
            Container.content.extend(
                Object.void()
                for i in xrange(int_key - len(Container.content) + 1)
            )
        return Container.content[int_key]

    elif Container.type == Object.MAP:
        entry = Container.content.get(Key.content)
        if entry is None: 
            entry = Object.void()
            Container.content[Key.content] = entry
        return entry
        
    else:
        print "Error: %s object does not support subscription." % Container.type
        return None

def my_assignment(world, ObjectRef, Value):
    prev = ObjectRef
    ObjectRef.content = Value.content
    ObjectRef.type    = Value.type
    if ObjectRef.name == Object.NAME_ANONYMOUS: ObjectRef.name = Value.name

    if prev.type != Object.VOID or prev.content != Value:
        log.attribute_value_change(world, ObjectRef.name, Value)

    return Object.bool(True)

def my_mod_assignment(world, ObjectRef, Value, DefaultValue, Operator):
    
    prev_content = ObjectRef.content

    if ObjectRef.type == Object.VOID: base_value = DefaultValue
    else:                             base_value = ObjectRef.content

    ObjectRef.content = Operator(base_value, Value.content)
    ObjectRef.type    = Value.type
    if ObjectRef.name == Object.NAME_ANONYMOUS: ObjectRef.name = Value.name

    if prev_content != ObjectRef.content:
        log.attribute_value_change(world, ObjectRef.name, Value)
    return ObjectRef
    
def my_plus_assignment(world, VariableName, Value):
    return my_mod_assignment(world, VariableName, Value, Object.number(0), lambda x, y: x + y)

def my_minus_assignment(world, VariableName, Value):
    return my_mod_assignment(world, VariableName, Value, Object.number(0), lambda x, y: x - y)

def my_verdict_event_occured(world, EventInfo):
    assert EventInfo is not None
    trigger_time = EventInfo.last_time
    current_time = world.time()
    result = (current_time == trigger_time)
    return Object.bool(result)

def my_member_time(world, TheEvent):
    return Object.number(world.event_db[TheEvent.name].last_time)

def my_member_time_in_state(world, TheEvent):
    return Object.number(world.event_db[TheEvent.name].time_in_state)

def my_member_count(world, TheEvent):
    return Object.number(world.event_db[TheEvent.name].count_n)

def my_event_adornment(world, TheEvent, Name):
    adornment_list = world.event_db[TheEvent.name].related_event.adornment_list()
    # Adornments 'time', 'count', 'time_in_state' are separate functions (see above).
    assert Name not in ("time", "count", "time_in_state")
    if   Name.content == "time":  return Object.number(TheEvent.last_time)
    elif Name.content == "count": return Object.number(TheEvent.count)

    for adornment in adornment_list:
        if adornment.name == Name.content: return adornment
    return Object.void()

def FunctionObject_for_binary_op(binary_op):
    return FunctionObject(lambda x, y:    
                          Object.from_string_or_number(binary_op(x.content, y.content)), 
                          ["Object", "Object"])
    
BuiltInFunctionDB = {
        "=":       FunctionObject(my_assignment, [Object.VOID, Object.VOID],   WorldRequiredF=True),
        "+=":      [ FunctionObject(my_plus_assignment, ["Object", "List"],   WorldRequiredF=True),
                     FunctionObject(my_plus_assignment, ["Object", Object.NUMBER], WorldRequiredF=True),
                     FunctionObject(my_plus_assignment, ["Object", Object.STRING], WorldRequiredF=True),
                   ],
        "-=":      [ FunctionObject(my_minus_assignment, ["Object", Object.NUMBER], WorldRequiredF=True),
                     FunctionObject(my_minus_assignment, ["Object", Object.STRING], WorldRequiredF=True),
                   ],
#        "*=":      [ FunctionObject(my_mult_assignment, [Object.STRING, Object.NUMBER], WorldRequiredF=True),
#                     FunctionObject(my_mult_assignment, [Object.STRING, Object.STRING], WorldRequiredF=True),
#                   ],
#        "/=":      [ FunctionObject(my_div_assignment, [Object.STRING, Object.NUMBER], WorldRequiredF=True),
#                     FunctionObject(my_div_assignment, [Object.STRING, Object.STRING], WorldRequiredF=True),
#                   ],
#        "<<=":      [ FunctionObject(my_lshift_assignment, [Object.STRING, Object.NUMBER], WorldRequiredF=True),
#                     FunctionObject(my_lshift_assignment, [Object.STRING, Object.STRING], WorldRequiredF=True),
#                   ],
#        ">>=":      [ FunctionObject(my_rshift_assignment, [Object.STRING, Object.NUMBER], WorldRequiredF=True),
#                     FunctionObject(my_rshift_assignment, [Object.STRING, Object.STRING], WorldRequiredF=True),
#                   ],
#        "&=":      [ FunctionObject(my_and_assignment, [Object.STRING, Object.NUMBER], WorldRequiredF=True),
#                     FunctionObject(my_and_assignment, [Object.STRING, Object.STRING], WorldRequiredF=True),
#                   ],
#        "|=":      [ FunctionObject(my_or_assignment, [Object.STRING, Object.NUMBER], WorldRequiredF=True),
#                     FunctionObject(my_or_assignment, [Object.STRING, Object.STRING], WorldRequiredF=True),
#                   ],
#        "^=":      [ FunctionObject(my_xor_assignment, [Object.STRING, Object.NUMBER], WorldRequiredF=True),
#                     FunctionObject(my_xor_assignment, [Object.STRING, Object.STRING], WorldRequiredF=True),
#                   ],
        #
        "+":       FunctionObject_for_binary_op(lambda x, y: x + y),
        "-":       FunctionObject_for_binary_op(lambda x, y: x - y), 
        "*":       FunctionObject_for_binary_op(lambda x, y: x * y),
        "**":      FunctionObject_for_binary_op(lambda x, y: x ** y),
        "/":       FunctionObject_for_binary_op(my_division),
        "%":       FunctionObject_for_binary_op(my_modulo),
        #
        "==":      FunctionObject_for_binary_op(lambda x, y: x == y),
        "!=":      FunctionObject_for_binary_op(lambda x, y: x != y),
        ">=":      FunctionObject_for_binary_op(lambda x, y: x >= y),
        ">":       FunctionObject_for_binary_op(my_greater),
        # ">":       FunctionObject_for_binary_op(lambda x, y: x >  y),
        "<=":      FunctionObject_for_binary_op(lambda x, y: x <= y),
        "<":       FunctionObject_for_binary_op(lambda x, y: x <  y),
        #
        "<<":      FunctionObject_for_binary_op(lambda x, y: x << y),
        ">>":      FunctionObject_for_binary_op(lambda x, y: x >> y),
        "&":       FunctionObject_for_binary_op(lambda x, y: x &  y),
        "|":       FunctionObject_for_binary_op(lambda x, y: x |  y),
        "^":       FunctionObject_for_binary_op(lambda x, y: x ^  y),
        #
        "or":      FunctionObject_for_binary_op(lambda x, y: x or y),
        "and":     FunctionObject_for_binary_op(lambda x, y: x and y),
        #
        "$variable-access":        FunctionObject(lambda world, name: world.variable_access(name), [Object.STRING], WorldRequiredF=True),
        #
        "$member-time":            FunctionObject(my_member_time,          ["Object"], WorldRequiredF=True),
        "$member-time-in-state":   FunctionObject(my_member_time_in_state, ["Object"], WorldRequiredF=True),
        "$member-count":           FunctionObject(my_member_count,         ["Object"], WorldRequiredF=True),
        #
        "$event-adornment":        FunctionObject(my_event_adornment, ["Object", "Object"], WorldRequiredF=True),
        #
        "$element-access":         FunctionObject(my_element_access, ["Object", "Object"]),
        #
        "$verdict-conversion":     FunctionObject(lambda x: Object.convert_to_bool(x), ["Object"]),
        "$verdict-inversion":      FunctionObject(lambda x: Object.bool(not Object.convert_to_bool(x).content), ["Object"]),
        "$verdict-event-occured":  FunctionObject(my_verdict_event_occured,    ["Object"], WorldRequiredF=True),
        #
        "$send":              FunctionObject(lambda world, event: world.receive_event(event),   ["Object"], WorldRequiredF=True),
        #
        "$freeze":            FunctionObject(lambda world, nsp: world.freeze_namespace(nsp),   ["PyList"], WorldRequiredF=True),
        "$unfreeze":          FunctionObject(lambda world, nsp: world.unfreeze_namespace(nsp), ["PyList"], WorldRequiredF=True),
        "$unfreeze-shallow":  FunctionObject(lambda world, nsp: world.unfreeze_namespace(nsp, ShallowF=True), ["PyList"], WorldRequiredF=True),
        # 
        "$replace": FunctionObject(lambda x, y, z: x.replace(y, z), [Object.STRING, Object.STRING]),
        "$split":   FunctionObject(lambda x, y:    x.split(y),      [Object.STRING, Object.STRING]),
        "$strip":   FunctionObject(lambda x:       x.strip(),       [Object.STRING]),
        "$number":  FunctionObject(lambda x:       float(x),        [Object.STRING]),
        #
        "exp":      FunctionObject(math.exp,   [Object.NUMBER]),
        "sqrt":     FunctionObject(math.sqrt,  [Object.NUMBER]),
        "pow":      FunctionObject(math.pow,   [Object.NUMBER]),
        "log":      FunctionObject(math.log,   [Object.NUMBER]),
        "log10":    FunctionObject(math.log10, [Object.NUMBER]),
        "sin":      FunctionObject(math.sin,   [Object.NUMBER]),
        "cos":      FunctionObject(math.cos,   [Object.NUMBER]),
        "tan":      FunctionObject(math.tan,   [Object.NUMBER]),
        "sinh":     FunctionObject(math.sinh,  [Object.NUMBER]),
        "cosh":     FunctionObject(math.cosh,  [Object.NUMBER]),
        "tanh":     FunctionObject(math.tanh,  [Object.NUMBER]),
        "asin":     FunctionObject(math.asin,  [Object.NUMBER]),
        "acos":     FunctionObject(math.acos,  [Object.NUMBER]),
        "atan":     FunctionObject(math.atan,  [Object.NUMBER]),
        "atan2":    FunctionObject(math.atan2, [Object.NUMBER, Object.NUMBER]),
        #
        "max":      FunctionObject(max, ["List"]),
        "min":      FunctionObject(min, ["List"]),
        #
        "$size":       FunctionObject(lambda x:    x.size(), ["Object"]),
        "$has":        FunctionObject(lambda x, y: x.has(y),                ["Object", "Object"]),
        "$key":        FunctionObject(lambda x, y: x.find_key(y),           ["Object", "Object"]),
        "$push":       FunctionObject(lambda x, y: x.content.insert(0, y),  ["List", "Object"]),
        "$pop":        FunctionObject(lambda x, y: x.content.append(y),     ["List", "Object"]),
        "$push_front": FunctionObject(lambda x:    x.content.pop(0),        ["List"]),
        "$pop_front":  FunctionObject(lambda x:    x.content.pop(-1),       ["List"]),
        "$delete":     FunctionObject(lambda x, y: x.delete(y),             ["Object", "Object"]),
        }

