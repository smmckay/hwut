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

class StateTransition:
    def __init__(self, EventName, ConditionName, TargetStateName):
        self.condition_name      = ConditionName
        self.event_name          = EventName
        self.target_state_name   = TargetStateName
        self.walker              = None # To be assigned later

    def __str__(self):
        return "{ condition: %s; event: %s; target_state: %s; }" % \
               (self.condition_name, self.event_name, self.target_state_name)

class State:
    def __init__(self, Name, TransitionList):
        self.name            = Name
        self.transition_list = TransitionList
        self.walker          = None # To be assigned later
        self.intermediate_f  = False

    def __str__(self):
        txt  = "  {\n"
        txt += "    .name: %s;\n" % self.name
        txt += "    .transition_list: [\n"
        for t in self.transition_list:
            txt += "      %s\n" % str(t)
        txt += "    ]\n"
        txt += "  }\n"
        return txt

    def get_intermediate_state(self, state_db):
        i = 0
        while 1 + 1 == 2:
            name = "%s_post%i" % (self.name, i)
            if name not in state_db: break
            i += 1
        state = State(name, [])
        state.intermediate_f = True
        state_db[name] = state
        return state
        
        
class StateMachineWalker:
    def __init__(self, Name, StateList, UserDataType, MaxPathLength, MaxLoopN):
        self.name                = Name
        self.state_list          = StateList
        self.user_data_type      = UserDataType
        self.max_path_length     = MaxPathLength    
        self.max_loop_n          = MaxLoopN
        self.walker              = None # To be assigned later
        self.init_state_index    = None # To be assigned later
        self.condition_id_offset = -1

    def prepare_databases(self, state_list, event_id_db, condition_id_db):
        self.init_state_index = len(state_list)
        self.event_id_set     = set()
        condition_id_db[(self.name, None)] = 0
        self.condition_id_offset = 1 + sum(1 for key in condition_id_db.iterkeys() 
                                           if key[1] is not None)

        for state in self.state_list:
            # Relate state and all transition to this walker
            state.walker = self.name

            # Append states of state machine walker to global state list
            state_list.append(state)

        for state in self.state_list:
            # Append what results from transition information
            for t in state.transition_list:
                t.walker = self.name
                self.extract_from_transition(t, event_id_db, condition_id_db)

    def extract_from_transition(self, Transition, event_id_db, condition_id_db):
        """Transitions contain information about events and conditions. Those, 
        are extracted in this function and entered in the 'event_id_db' and the 
        'condition_id_db'.
        """
        def register(the_db, Key, BeginIndex=0):
            value = the_db.get(Key)
            if value is not None: return value

            # Count number of entries which are not None + 1
            new_index   = BeginIndex + sum(1 for key in the_db.iterkeys() if key[1] is not None)
            the_db[Key] = new_index
            return new_index

        if Transition.event_name is not None:
            register(event_id_db, (self.name, Transition.event_name), 
                     BeginIndex=0)
        self.event_id_set.add(Transition.event_name)

        if Transition.condition_name is not None: 
            if not condition_is_negated(Transition.condition_name):
                condition_name = Transition.condition_name
            else:
                condition_name = condition_negate(Transition.condition_name)

            register(condition_id_db, (self.name, condition_name), 
                     BeginIndex=1)

    def __str__(self):
        txt  = ""
        txt += ".name:            %s;\n" % self.name            
        txt += ".user_data_type:  %s;\n" % self.user_data_type  
        txt += ".max_path_length: %s;\n" % self.max_path_length 
        txt += ".max_loop_n:      %s;\n" % self.max_loop_n      
        txt += ".state_list: [\n"
        for state in self.state_list:
            txt += str(state)
        txt += "]\n"
        return txt
        

def condition_negate(ConditionName):
    """Negate a condition:

            "-Condition" means "not Condition"
    
   double negation is no negation, thus if '-' is already there then delete it.
    """
    if ConditionName is None:     return None

    assert len(ConditionName)

    if ConditionName[0] == "-": return ConditionName[1:]
    else:                       return "-%s" % ConditionName

def condition_interpret(ConditionName):
    if ConditionName is None:     return "NoCondition", False

    assert len(ConditionName)

    if ConditionName[0] == "-": return ConditionName[1:], True
    else:                       return ConditionName, False

def condition_is_negated(ConditionName):
    if ConditionName is None: return False

    assert len(ConditionName)

    return ConditionName[0] == "-"
