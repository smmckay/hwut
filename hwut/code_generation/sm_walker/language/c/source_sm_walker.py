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
from hwut.code_generation.sm_walker.sm_walker import State, \
                                                     StateTransition, \
                                                     StateMachineWalker, \
                                                     condition_interpret
from collections import namedtuple
from operator    import itemgetter

def do(SmWalkerList):
    """Generate source code (.c files) for a given list of state machine walkers.
    """
    state_list      = []
    event_id_db     = {}
    condition_id_db = {}

    # Assign global state indices to states
    global_state_index = 0
    state_index_db     = {}
    for walker in SmWalkerList:
        for state in walker.state_list:
            state.global_id                           = global_state_index
            state_index_db[(walker.name, state.name)] = global_state_index
            global_state_index += 1

    for walker in SmWalkerList:
        walker.prepare_databases(state_list, event_id_db, condition_id_db)

    # (*) Code the objects
    objects_txt = do_state_list(state_list, event_id_db, condition_id_db, state_index_db)

    # (*) Code the initialization(s)
    init_txt = "".join(do_execute(walker) for walker in SmWalkerList)

    return objects_txt + init_txt, \
           event_id_db, \
           condition_id_db

def do_state_list(StateList, event_id_db, condition_id_db, state_index_db):
    txt = [
        do_name_db("event_id",     event_id_db),
        "\n",
        do_name_db("condition_id", condition_id_db),
        "\n",
        "/* Forward declaration--definition follows.                                  */\n",
        "static hwut_sm_state_t   self_states[%i];\n" % len(StateList),
        "\n",
    ]
    for state_index, state in enumerate(StateList):
        txt.append("static hwut_sm_transition_t self_tm_%i[%i] = {\n" % 
                   (state_index, len(state.transition_list)))
        txt.extend(
            "    %s,\n" % do_transition(transition, event_id_db, condition_id_db, state_index_db)
            for transition in state.transition_list
        )
        txt.append("};\n")

    def get_state_id(state):
        return "%s_%s" % (state.walker, state.name)

    L = max(map(lambda state: len(get_state_id(state)), StateList))
    txt.append("static hwut_sm_state_t self_states[%i] = {\n" % len(StateList))

    txt.extend(
        '   { %s, %s"%s", %s0, &self_tm_%i[0], &self_tm_%i[%i] },\n' \
        % (get_state_id(state), " " * (L - len(get_state_id(state))),  \
           state.name, " " * (L - len(state.name)),                \
           state.global_id, state.global_id, len(state.transition_list)) 
        for state in sorted(StateList, key=lambda x: x.global_id)
    )
    txt.append("};\n")
    return "".join(txt)
        
        
def do_name_db(Name, NameDb):
    # It is possible that there are more than one entry for 'condition = None'
    L = max(len(str(name[0])) for name in NameDb.iterkeys())

    items = [
        (i, '/* %s: %s%3i */ "%s",\n' % (name[0], " " * (L - len(name[0])), i, name[1]))
        for name, i in NameDb.iteritems() if name[1] is not None
    ]
    if len(items) != len(NameDb):
        items.append(
            (0, '/* All: %s%3i */ "None",\n' % (" " * (L - len("All")), i))
        )

    return "".join([
       "const char* (self_%s_db[]) = {\n" % Name, 
       "".join(content for i, content in sorted(items, key=itemgetter(0))),
       "};\n",
     ])

def do_transition(Transition, EventIdDb, ConditionIdDb, StateIndexDb):
    if Transition.event_name is None: 
        event_name = "0"
    else:                             
        event_name = "%s_%s" % (Transition.walker, Transition.event_name)
    
    if Transition.condition_name is None:
        condition_name = "0"
    else:
        condition_name, not_f = condition_interpret(Transition.condition_name)
        not_str = { True: "-", False: "" }[not_f]
        condition_name = "%s%s_%s" % (not_str, Transition.walker, condition_name)

    return "{ %s, %s, &self_states[%i] }" % \
           (event_name, condition_name,
            StateIndexDb[(Transition.walker, Transition.target_state_name)])
    
txt_execute = """
static void   
self_$$NAME$$_do_init(hwut_sm_walker_t* alter_ego)
{
    $$NAME$$_t* me = ($$NAME$$_t*)alter_ego;
    if( me->do_init != (void*)0 ) {
        me->do_init(me);
    }
}

static void   
self_$$NAME$$_do_event(hwut_sm_walker_t* alter_ego, hwut_sm_state_t* state, int EventId)
{
    $$NAME$$_t* me = ($$NAME$$_t*)alter_ego;
#   define      self (*(($$USER_DATA_TYPE$$*)(me->subject)))
$$EVENT_JOKER_TEST$$
    {
$$EVENT_AT_BEGIN$$
    (void)me;

$$EVENT_CASE_LIST$$

#   undef self
    }
}

static int   
self_$$NAME$$_do_condition(hwut_sm_walker_t* alter_ego, hwut_sm_state_t* state, int ConditionId)
{
    $$NAME$$_t* me = ($$NAME$$_t*)alter_ego;
#   define      self (*(($$USER_DATA_TYPE$$*)(me->subject)))
$$CONDITION_AT_BEGIN$$
    (void)me;

$$CONDITION_CASE_LIST$$

#   undef self
    return 1;
}

static void   
self_$$NAME$$_do_terminal(hwut_sm_walker_t* alter_ego, hwut_sm_state_t* state_p)
{
    $$NAME$$_t* me = ($$NAME$$_t*)alter_ego;
    if( me->do_terminal != (void*)0 ) {
        me->do_terminal(me, state_p);
    }
}

hwut_sm_stack_frame_t  self_stack_memory_$$NAME$$[$$MAX_PATH_SIZE$$ + 1];

static void
$$NAME$$_init($$NAME$$_t*   me,
$$SPACE$$     $$USER_DATA_TYPE$$* subject,
$$SPACE$$     void   (*do_init)($$NAME$$_t* me),
$$SPACE$$     void   (*do_terminal)($$NAME$$_t* me, hwut_sm_state_t*))
{
    hwut_sm_walker_init(&me->base, $$MAX_PATH_SIZE$$ + 1, &self_stack_memory_$$NAME$$[0]); 

    me->subject       = subject;
    me->base.state_db = &self_states[0];

    hwut_sm_walker_aux_init(&me->base.aux, 
                            /* State index offset */$$INIT_STATE_INDEX$$, /* State number */$$STATE_N$$,
                            &me->memory.state_coverage[0],                  
                            &me->memory.state_forbidden[0],                  
                            &me->memory.state_forbidden_comment[0],                  
                            /* Condition id offset */$$CONDITION_ID_OFFSET$$, /* Condition number */$$CONDITION_N$$,
                            &me->memory.condition_coverage[0],      
                            &me->memory.condition_norm[0],      
                            &me->memory.condition_norm_comment[0], 
                            sizeof(self_event_id_db)/sizeof(const char*),
                            &self_event_id_db[0],
                            sizeof(self_condition_id_db)/sizeof(const char*),
                            &self_condition_id_db[0]);      

    me->do_init      = do_init;
    me->do_terminal  = do_terminal;

    me->base.do_init      = self_$$NAME$$_do_init;
    me->base.do_event     = self_$$NAME$$_do_event;
    me->base.do_condition = self_$$NAME$$_do_condition;
    me->base.do_terminal  = self_$$NAME$$_do_terminal;
}

void
$$NAME$$_execute($$NAME$$_t*   me,
$$SPACE$$         $$USER_DATA_TYPE$$* subject,
$$SPACE$$         void   (*do_init)($$NAME$$_t* me),
$$SPACE$$         void   (*do_terminal)($$NAME$$_t* me, hwut_sm_state_t*))
{
    $$NAME$$_init(me, subject, do_init, do_terminal);
    hwut_sm_walker_walk(&me->base, &self_states[$$INIT_STATE_INDEX$$], $$MAX_LOOP_N$$);
}

int
$$NAME$$_state_is_real(const hwut_sm_state_t* State)
{
    return State->id < $$NAME$$___BeyondId;
}
"""

def do_execute(walker):
    Name            = walker.name 
    InitStateIndex  = walker.init_state_index 
    UserDataType    = walker.user_data_type 
    PathMaxLength   = walker.max_path_length 
    MaxLoopN        = walker.max_loop_n 
    EventIdSet      = walker.event_id_set
    EventCaseDb     = walker.event_code_db 
    ConditionCaseDb = walker.condition_code_db

    state_n             = len(walker.state_list)
    condition_id_offset = walker.condition_id_offset
    condition_n         = len(ConditionCaseDb)
    if not condition_n: condition_n = 1

    txt = txt_execute.replace("$$NAME$$",        Name) 
    txt = txt.replace("$$MAX_PATH_SIZE$$",       "%i" % PathMaxLength)
    txt = txt.replace("$$MAX_LOOP_N$$",          "%i" % MaxLoopN)
    txt = txt.replace("$$INIT_STATE_INDEX$$",    "%i" % InitStateIndex)
    txt = txt.replace("$$USER_DATA_TYPE$$",      UserDataType)
    txt = txt.replace("$$SPACE$$",               " " * len(Name))

    joker_check       = get_event_joker_code(Name, EventCaseDb)
    at_begin, content = get_case_list(Name, "EventId", EventCaseDb)
    txt = txt.replace("$$EVENT_JOKER_TEST$$", joker_check)
    txt = txt.replace("$$EVENT_AT_BEGIN$$",  at_begin)
    txt = txt.replace("$$EVENT_CASE_LIST$$", content)

    at_begin, content = get_case_list(Name, "ConditionId", ConditionCaseDb)
    txt = txt.replace("$$CONDITION_AT_BEGIN$$",  at_begin)
    txt = txt.replace("$$CONDITION_CASE_LIST$$", content)
    txt = txt.replace("$$STATE_N$$",             "%i" % state_n)
    txt = txt.replace("$$CONDITION_N$$",         "%i" % condition_n)
    txt = txt.replace("$$CONDITION_ID_OFFSET$$", "%i" % condition_id_offset)
    return txt

def get_event_joker_code(WalkerName, EventCaseDb):
    txt     = "    switch( EventId ) {\n"
    joker_f = False
    # code = None => Joker
    for event_id, code in EventCaseDb.iteritems():
        if code is not None: continue
        txt     += "    case %s_%s: return;\n" % (WalkerName, event_id)
        joker_f  = True
    txt += "    }\n"

    if joker_f: return txt
    else:       return ""

def get_case_list(WalkerName, IdName, CaseDb):
    def get_code(Name, Code, CaseF=True):
        if Code is None: return "" # Joker
        txt =  "#   line %i \"%s\"\n" % (Code.line_n, Code.file_name)
        if CaseF:
            txt += "    case %s_%s: {\n" % (WalkerName, Name)
        txt += Code.text
        if CaseF:
            txt += "    }\n"
            txt += "    break;\n"
        return txt

    if len(CaseDb) == 0:
        return "", ""

    content_begin = ""
    if "@begin" in CaseDb:
        content_begin = get_code("", CaseDb["@begin"], CaseF=False)

    content = []
    if IdName != "EventId":
        # The 'do_condition' function is also called for 'condition 0', even though
        # the condition means: always ok. The thing is: such a setup allows for 
        # setting something in "@begin{ ... }" that hinders further diving into 
        # the state machine by returning '0' even for the 'always ok' case.
        content.append(
            "    case 0: return 1; /* Condition 0 --> Always OK */\n"
        )
    content.extend(
        get_code(name, code)
        for name, code in CaseDb.iteritems() if name not in ("@begin", "@end")
    )
    content =   "    switch( %s ) {\n" % IdName  \
              + "%s\n"                 % "".join(content) \
              + "    }\n"                               

    if IdName != "EventId": content_end = "    return 1;"
    else:                   content_end = ""
    if "@end" in CaseDb:
        content_end = get_code("", CaseDb["@end"], CaseF=False)

    content =   "%s\n" % content       \
              + "%s\n" % content_end 
    
    return content_begin, content
