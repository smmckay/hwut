#ifndef INCLUDE_GUARD_SM_WALKER_COMMON_H
#define INCLUDE_GUARD_SM_WALKER_COMMON_H


static void  do_init(hwut_sm_walker_t* me);
static void  do_event(hwut_sm_walker_t* me, hwut_sm_state_t* StateP, int EventId);
static int   do_condition(hwut_sm_walker_t* me, hwut_sm_state_t* StateP, int ConditionId);
static void  do_terminal(hwut_sm_walker_t* me, hwut_sm_state_t* StateP);

#define MY_EVENT_N     128
#define MY_CONDITION_N 128
#define MY_STATE_N     128
static const char*   self_event_id_db[MY_EVENT_N];
static const char*   self_condition_id_db[MY_CONDITION_N];
static hwut_sm_condition_coverage_t   self_condition_coverage_array[MY_CONDITION_N];
static hwut_sm_condition_norm_t       self_condition_norm_array[MY_CONDITION_N];
static const char*   self_condition_norm_comment[MY_CONDITION_N];
static int           self_state_coverage_array[MY_STATE_N];
static int           self_state_fobidden_array[MY_STATE_N];
static const char*   self_state_fobidden_comment[MY_STATE_N];

static void 
common_setup(hwut_sm_walker_t* me) 
{
    me->aux.event_id_db.begin        = &self_event_id_db[0];
    me->aux.event_id_db.end          = &self_event_id_db[sizeof(self_event_id_db)/sizeof(const char*)];
    me->aux.condition_id_db.begin    = &self_condition_id_db[0];
    me->aux.condition_id_db.end      = &self_condition_id_db[sizeof(self_condition_id_db)/sizeof(const char*)];
    me->aux.condition.number         = MY_CONDITION_N;
    me->aux.condition.coverage       = &self_condition_coverage_array[0];
    me->aux.condition.norm           = &self_condition_norm_array[0];
    me->aux.condition.norm_comment   = &self_condition_norm_comment[0];
    me->aux.state.number             = MY_STATE_N;
    me->aux.state.coverage           = &self_state_coverage_array[0];
    me->aux.state.forbidden          = &self_state_fobidden_array[0];
    me->aux.state.forbidden_comment  = &self_state_fobidden_comment[0];

    me->do_init      = do_init;
    me->do_event     = do_event;
    me->do_condition = do_condition;
    me->do_terminal  = do_terminal;

}

static void 
do_init(hwut_sm_walker_t* me) 
{ 
    printf("do_init:    { user_data: ((%p)); }\n", me); 
}

static void 
do_event(hwut_sm_walker_t* me, hwut_sm_state_t* StateP, int EventId) 
{ 
    printf("do_event:    { user_data: ((%p)); name: %s; event_id: %i; }\n", 
           me, StateP->name, EventId); 
}

static int 
do_condition(hwut_sm_walker_t* me, hwut_sm_state_t* StateP, int ConditionId) 
{ 
    int result = (ConditionId == 1);

    if(ConditionId == 0) return 1;
    printf("condition:   { user_data: ((%p)); name: %s; condition_id: %i; result: %s; }\n", 
           me, StateP->name, ConditionId, result ? "OK" : "FAIL"); 

    return result;
}

static void 
do_terminal(hwut_sm_walker_t* me, hwut_sm_state_t* StateP) 
{ 
    printf("do_terminal: { user_data: ((%p)); name: %s; }\n\n", me, StateP->name); 
}

#endif /* INCLUDE_GUARD_SM_WALKER_COMMON_H */
