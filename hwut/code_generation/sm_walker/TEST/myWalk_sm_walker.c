#include "myWalk_sm_walker.h"
const char* (self_event_id_db[]) = {
/* myWalk4:   0 */ "JUMP",
/* myWalk4:   1 */ "FLY",
/* myWalk4:   2 */ "HOP",
/* myWalk5:   3 */ "X",
/* myWalk1:   4 */ "walkes",
/* myWalk1:   5 */ "goes",
/* myWalk2:   6 */ "goes",
/* myWalk2:   7 */ "walkes",
/* myWalk3:   8 */ "BUZZ",
};

const char* (self_condition_id_db[]) = {
/* All:       0 */ "None",
/* myWalk5:   1 */ "C0",
/* myWalk5:   2 */ "C1",
/* myWalk3:   3 */ "WARM",
/* myWalk3:   4 */ "COLD",
};

/* Forward declaration--definition follows.                                  */
static hwut_sm_state_t   self_states[17];

static hwut_sm_transition_t self_tm_0[1] = {
    { myWalk4_JUMP, 0, &self_states[2] },
};
static hwut_sm_transition_t self_tm_1[1] = {
    { myWalk4_FLY, 0, &self_states[3] },
};
static hwut_sm_transition_t self_tm_2[1] = {
    { myWalk4_HOP, 0, &self_states[1] },
};
static hwut_sm_transition_t self_tm_3[0] = {
};
static hwut_sm_transition_t self_tm_4[2] = {
    { myWalk5_X, 0, &self_states[7] },
    { myWalk5_X, 0, &self_states[8] },
};
static hwut_sm_transition_t self_tm_5[0] = {
};
static hwut_sm_transition_t self_tm_6[0] = {
};
static hwut_sm_transition_t self_tm_7[2] = {
    { 0, myWalk5_C0, &self_states[6] },
    { 0, -myWalk5_C0, &self_states[4] },
};
static hwut_sm_transition_t self_tm_8[2] = {
    { 0, myWalk5_C1, &self_states[5] },
    { 0, -myWalk5_C1, &self_states[4] },
};
static hwut_sm_transition_t self_tm_9[2] = {
    { myWalk1_walkes, 0, &self_states[10] },
    { myWalk1_goes, 0, &self_states[10] },
};
static hwut_sm_transition_t self_tm_10[0] = {
};
static hwut_sm_transition_t self_tm_11[1] = {
    { myWalk2_goes, 0, &self_states[13] },
};
static hwut_sm_transition_t self_tm_12[1] = {
    { myWalk2_walkes, 0, &self_states[13] },
};
static hwut_sm_transition_t self_tm_13[1] = {
    { myWalk2_goes, 0, &self_states[12] },
};
static hwut_sm_transition_t self_tm_14[2] = {
    { myWalk3_BUZZ, myWalk3_WARM, &self_states[16] },
    { myWalk3_BUZZ, myWalk3_COLD, &self_states[15] },
};
static hwut_sm_transition_t self_tm_15[1] = {
    { myWalk3_BUZZ, 0, &self_states[14] },
};
static hwut_sm_transition_t self_tm_16[1] = {
    { myWalk3_BUZZ, 0, &self_states[15] },
};
static hwut_sm_state_t self_states[17] = {
   { myWalk4_A,          "A",                  0, &self_tm_0[0], &self_tm_0[1] },
   { myWalk4_C,          "C",                  0, &self_tm_1[0], &self_tm_1[1] },
   { myWalk4_B,          "B",                  0, &self_tm_2[0], &self_tm_2[1] },
   { myWalk4_D,          "D",                  0, &self_tm_3[0], &self_tm_3[0] },
   { myWalk5_A,          "A",                  0, &self_tm_4[0], &self_tm_4[2] },
   { myWalk5_C,          "C",                  0, &self_tm_5[0], &self_tm_5[0] },
   { myWalk5_B,          "B",                  0, &self_tm_6[0], &self_tm_6[0] },
   { myWalk5_A_post0,    "A_post0",            0, &self_tm_7[0], &self_tm_7[2] },
   { myWalk5_A_post1,    "A_post1",            0, &self_tm_8[0], &self_tm_8[2] },
   { myWalk1_BEGIN1,     "BEGIN1",             0, &self_tm_9[0], &self_tm_9[2] },
   { myWalk1_Frieda,     "Frieda",             0, &self_tm_10[0], &self_tm_10[0] },
   { myWalk2_BEGIN2,     "BEGIN2",             0, &self_tm_11[0], &self_tm_11[1] },
   { myWalk2_Erwin,      "Erwin",              0, &self_tm_12[0], &self_tm_12[1] },
   { myWalk2_Otto,       "Otto",               0, &self_tm_13[0], &self_tm_13[1] },
   { myWalk3_Bed,        "Bed",                0, &self_tm_14[0], &self_tm_14[2] },
   { myWalk3_LivingRoom, "LivingRoom",         0, &self_tm_15[0], &self_tm_15[1] },
   { myWalk3_Garden,     "Garden",             0, &self_tm_16[0], &self_tm_16[1] },
};

static void   
self_myWalk4_do_init(hwut_sm_walker_t* alter_ego)
{
    myWalk4_t* me = (myWalk4_t*)alter_ego;
    if( me->do_init != (void*)0 ) {
        me->do_init(me);
    }
}

static void   
self_myWalk4_do_event(hwut_sm_walker_t* alter_ego, hwut_sm_state_t* state, int EventId)
{
    myWalk4_t* me = (myWalk4_t*)alter_ego;
#   define      self (*((my_data_t*)(me->subject)))
    switch( EventId ) {
    case myWalk4_JUMP: return;
    case myWalk4_FLY: return;
    case myWalk4_HOP: return;
    }

    {

    (void)me;

    switch( EventId ) {

    }




#   undef self
    }
}

static int   
self_myWalk4_do_condition(hwut_sm_walker_t* alter_ego, hwut_sm_state_t* state, int ConditionId)
{
    myWalk4_t* me = (myWalk4_t*)alter_ego;
#   define      self (*((my_data_t*)(me->subject)))

    (void)me;



#   undef self
    return 1;
}

static void   
self_myWalk4_do_terminal(hwut_sm_walker_t* alter_ego, hwut_sm_state_t* state_p)
{
    myWalk4_t* me = (myWalk4_t*)alter_ego;
    if( me->do_terminal != (void*)0 ) {
        me->do_terminal(me, state_p);
    }
}

hwut_sm_stack_frame_t  self_stack_memory_myWalk4[4 + 1];

static void
myWalk4_init(myWalk4_t*   me,
            my_data_t* subject,
            void   (*do_init)(myWalk4_t* me),
            void   (*do_terminal)(myWalk4_t* me, hwut_sm_state_t*))
{
    hwut_sm_walker_init(&me->base, 4 + 1, &self_stack_memory_myWalk4[0]); 

    me->subject       = subject;
    me->base.state_db = &self_states[0];

    hwut_sm_walker_aux_init(&me->base.aux, 
                            /* State index offset */0, /* State number */4,
                            &me->memory.state_coverage[0],                  
                            &me->memory.state_forbidden[0],                  
                            &me->memory.state_forbidden_comment[0],                  
                            /* Condition id offset */1, /* Condition number */1,
                            &me->memory.condition_coverage[0],      
                            &me->memory.condition_norm[0],      
                            &me->memory.condition_norm_comment[0], 
                            sizeof(self_event_id_db)/sizeof(const char*),
                            &self_event_id_db[0],
                            sizeof(self_condition_id_db)/sizeof(const char*),
                            &self_condition_id_db[0]);      

    me->do_init      = do_init;
    me->do_terminal  = do_terminal;

    me->base.do_init      = self_myWalk4_do_init;
    me->base.do_event     = self_myWalk4_do_event;
    me->base.do_condition = self_myWalk4_do_condition;
    me->base.do_terminal  = self_myWalk4_do_terminal;
}

void
myWalk4_execute(myWalk4_t*   me,
                my_data_t* subject,
                void   (*do_init)(myWalk4_t* me),
                void   (*do_terminal)(myWalk4_t* me, hwut_sm_state_t*))
{
    myWalk4_init(me, subject, do_init, do_terminal);
    hwut_sm_walker_walk(&me->base, &self_states[0], 1);
}

int
myWalk4_state_is_real(const hwut_sm_state_t* State)
{
    return State->id < myWalk4___BeyondId;
}

static void   
self_myWalk5_do_init(hwut_sm_walker_t* alter_ego)
{
    myWalk5_t* me = (myWalk5_t*)alter_ego;
    if( me->do_init != (void*)0 ) {
        me->do_init(me);
    }
}

static void   
self_myWalk5_do_event(hwut_sm_walker_t* alter_ego, hwut_sm_state_t* state, int EventId)
{
    myWalk5_t* me = (myWalk5_t*)alter_ego;
#   define      self (*((my_data_t*)(me->subject)))

    {

    (void)me;

    switch( EventId ) {
#   line 128 "total-sm_walker.c"
    case myWalk5_X: {
    
      printf("event:       { user_data: ((%p)); name: %s; event_id: %s; }\n", 
             me->subject, state->name, me->base.aux.event_id_db.begin[EventId]); 
       }
    break;

    }




#   undef self
    }
}

static int   
self_myWalk5_do_condition(hwut_sm_walker_t* alter_ego, hwut_sm_state_t* state, int ConditionId)
{
    myWalk5_t* me = (myWalk5_t*)alter_ego;
#   define      self (*((my_data_t*)(me->subject)))
#   line 135 "total-sm_walker.c"

     printf("state: %s; real: %s;\n", 
            state->name, myWalk5_state_is_real(state) ? "true" : "false");
   
    (void)me;

    switch( ConditionId ) {
    case 0: return 1; /* Condition 0 --> Always OK */
#   line 145 "total-sm_walker.c"
    case myWalk5_C1: {
 
       printf("condition:   { user_data: ((%p)); name: %s(%i); condition_id: %s; result: %s; }\n", 
               me->subject, state->name, state->pass_n, me->base.aux.condition_id_db.begin[ConditionId], "OK"); 
       return 1; 
        }
    break;
#   line 140 "total-sm_walker.c"
    case myWalk5_C0: {
 
       printf("condition:   { user_data: ((%p)); name: %s(%i); condition_id: %s; result: %s; }\n", 
               me->subject, state->name, state->pass_n, me->base.aux.condition_id_db.begin[ConditionId], "FAIL"); 
       return 0; 
        }
    break;

    }

    return 1;


#   undef self
    return 1;
}

static void   
self_myWalk5_do_terminal(hwut_sm_walker_t* alter_ego, hwut_sm_state_t* state_p)
{
    myWalk5_t* me = (myWalk5_t*)alter_ego;
    if( me->do_terminal != (void*)0 ) {
        me->do_terminal(me, state_p);
    }
}

hwut_sm_stack_frame_t  self_stack_memory_myWalk5[100 + 1];

static void
myWalk5_init(myWalk5_t*   me,
            my_data_t* subject,
            void   (*do_init)(myWalk5_t* me),
            void   (*do_terminal)(myWalk5_t* me, hwut_sm_state_t*))
{
    hwut_sm_walker_init(&me->base, 100 + 1, &self_stack_memory_myWalk5[0]); 

    me->subject       = subject;
    me->base.state_db = &self_states[0];

    hwut_sm_walker_aux_init(&me->base.aux, 
                            /* State index offset */4, /* State number */5,
                            &me->memory.state_coverage[0],                  
                            &me->memory.state_forbidden[0],                  
                            &me->memory.state_forbidden_comment[0],                  
                            /* Condition id offset */1, /* Condition number */3,
                            &me->memory.condition_coverage[0],      
                            &me->memory.condition_norm[0],      
                            &me->memory.condition_norm_comment[0], 
                            sizeof(self_event_id_db)/sizeof(const char*),
                            &self_event_id_db[0],
                            sizeof(self_condition_id_db)/sizeof(const char*),
                            &self_condition_id_db[0]);      

    me->do_init      = do_init;
    me->do_terminal  = do_terminal;

    me->base.do_init      = self_myWalk5_do_init;
    me->base.do_event     = self_myWalk5_do_event;
    me->base.do_condition = self_myWalk5_do_condition;
    me->base.do_terminal  = self_myWalk5_do_terminal;
}

void
myWalk5_execute(myWalk5_t*   me,
                my_data_t* subject,
                void   (*do_init)(myWalk5_t* me),
                void   (*do_terminal)(myWalk5_t* me, hwut_sm_state_t*))
{
    myWalk5_init(me, subject, do_init, do_terminal);
    hwut_sm_walker_walk(&me->base, &self_states[4], 1);
}

int
myWalk5_state_is_real(const hwut_sm_state_t* State)
{
    return State->id < myWalk5___BeyondId;
}

static void   
self_myWalk1_do_init(hwut_sm_walker_t* alter_ego)
{
    myWalk1_t* me = (myWalk1_t*)alter_ego;
    if( me->do_init != (void*)0 ) {
        me->do_init(me);
    }
}

static void   
self_myWalk1_do_event(hwut_sm_walker_t* alter_ego, hwut_sm_state_t* state, int EventId)
{
    myWalk1_t* me = (myWalk1_t*)alter_ego;
#   define      self (*((my_data_t*)(me->subject)))

    {

    (void)me;

    switch( EventId ) {
#   line 17 "total-sm_walker.c"
    case myWalk1_walkes: {
 printf("I walk!\n");     }
    break;
#   line 16 "total-sm_walker.c"
    case myWalk1_goes: {
 printf("I go!\n");     }
    break;

    }

#   line 19 "total-sm_walker.c"
 
      printf("do_event:    { user_data: ((%p)); name: %s; event: %s; }\n", 
             me->subject, state->name, me->base.aux.event_id_db.begin[EventId]);  
   


#   undef self
    }
}

static int   
self_myWalk1_do_condition(hwut_sm_walker_t* alter_ego, hwut_sm_state_t* state, int ConditionId)
{
    myWalk1_t* me = (myWalk1_t*)alter_ego;
#   define      self (*((my_data_t*)(me->subject)))

    (void)me;

    switch( ConditionId ) {
    case 0: return 1; /* Condition 0 --> Always OK */

    }

#   line 26 "total-sm_walker.c"
 
        int result = (ConditionId == 1);
        assert(ConditionId != 0);
        printf("condition:   { user_data: ((%p)); name: %s; condition_id: %i; result: %s; }\n", 
               me->subject, state->name, ConditionId, result ? "OK" : "FAIL"); 
        return result;
   


#   undef self
    return 1;
}

static void   
self_myWalk1_do_terminal(hwut_sm_walker_t* alter_ego, hwut_sm_state_t* state_p)
{
    myWalk1_t* me = (myWalk1_t*)alter_ego;
    if( me->do_terminal != (void*)0 ) {
        me->do_terminal(me, state_p);
    }
}

hwut_sm_stack_frame_t  self_stack_memory_myWalk1[4 + 1];

static void
myWalk1_init(myWalk1_t*   me,
            my_data_t* subject,
            void   (*do_init)(myWalk1_t* me),
            void   (*do_terminal)(myWalk1_t* me, hwut_sm_state_t*))
{
    hwut_sm_walker_init(&me->base, 4 + 1, &self_stack_memory_myWalk1[0]); 

    me->subject       = subject;
    me->base.state_db = &self_states[0];

    hwut_sm_walker_aux_init(&me->base.aux, 
                            /* State index offset */9, /* State number */2,
                            &me->memory.state_coverage[0],                  
                            &me->memory.state_forbidden[0],                  
                            &me->memory.state_forbidden_comment[0],                  
                            /* Condition id offset */3, /* Condition number */1,
                            &me->memory.condition_coverage[0],      
                            &me->memory.condition_norm[0],      
                            &me->memory.condition_norm_comment[0], 
                            sizeof(self_event_id_db)/sizeof(const char*),
                            &self_event_id_db[0],
                            sizeof(self_condition_id_db)/sizeof(const char*),
                            &self_condition_id_db[0]);      

    me->do_init      = do_init;
    me->do_terminal  = do_terminal;

    me->base.do_init      = self_myWalk1_do_init;
    me->base.do_event     = self_myWalk1_do_event;
    me->base.do_condition = self_myWalk1_do_condition;
    me->base.do_terminal  = self_myWalk1_do_terminal;
}

void
myWalk1_execute(myWalk1_t*   me,
                my_data_t* subject,
                void   (*do_init)(myWalk1_t* me),
                void   (*do_terminal)(myWalk1_t* me, hwut_sm_state_t*))
{
    myWalk1_init(me, subject, do_init, do_terminal);
    hwut_sm_walker_walk(&me->base, &self_states[9], 1);
}

int
myWalk1_state_is_real(const hwut_sm_state_t* State)
{
    return State->id < myWalk1___BeyondId;
}

static void   
self_myWalk2_do_init(hwut_sm_walker_t* alter_ego)
{
    myWalk2_t* me = (myWalk2_t*)alter_ego;
    if( me->do_init != (void*)0 ) {
        me->do_init(me);
    }
}

static void   
self_myWalk2_do_event(hwut_sm_walker_t* alter_ego, hwut_sm_state_t* state, int EventId)
{
    myWalk2_t* me = (myWalk2_t*)alter_ego;
#   define      self (*((my_data_t*)(me->subject)))

    {

    (void)me;

    switch( EventId ) {

    }

#   line 48 "total-sm_walker.c"
 
      printf("do_event:    { user_data: ((%p)); name: %s; event: %s; }\n", 
             me->subject, state->name, me->base.aux.event_id_db.begin[EventId]);  
   


#   undef self
    }
}

static int   
self_myWalk2_do_condition(hwut_sm_walker_t* alter_ego, hwut_sm_state_t* state, int ConditionId)
{
    myWalk2_t* me = (myWalk2_t*)alter_ego;
#   define      self (*((my_data_t*)(me->subject)))

    (void)me;

    switch( ConditionId ) {
    case 0: return 1; /* Condition 0 --> Always OK */

    }

#   line 55 "total-sm_walker.c"
 
        int result = (ConditionId == 1);
        assert(ConditionId != 0);
        printf("condition:   { user_data: ((%p)); name: %s; condition_id: %i; result: %s; }\n", 
               me->subject, state->name, ConditionId, result ? "OK" : "FAIL"); 
        return result;
   


#   undef self
    return 1;
}

static void   
self_myWalk2_do_terminal(hwut_sm_walker_t* alter_ego, hwut_sm_state_t* state_p)
{
    myWalk2_t* me = (myWalk2_t*)alter_ego;
    if( me->do_terminal != (void*)0 ) {
        me->do_terminal(me, state_p);
    }
}

hwut_sm_stack_frame_t  self_stack_memory_myWalk2[4 + 1];

static void
myWalk2_init(myWalk2_t*   me,
            my_data_t* subject,
            void   (*do_init)(myWalk2_t* me),
            void   (*do_terminal)(myWalk2_t* me, hwut_sm_state_t*))
{
    hwut_sm_walker_init(&me->base, 4 + 1, &self_stack_memory_myWalk2[0]); 

    me->subject       = subject;
    me->base.state_db = &self_states[0];

    hwut_sm_walker_aux_init(&me->base.aux, 
                            /* State index offset */11, /* State number */3,
                            &me->memory.state_coverage[0],                  
                            &me->memory.state_forbidden[0],                  
                            &me->memory.state_forbidden_comment[0],                  
                            /* Condition id offset */3, /* Condition number */1,
                            &me->memory.condition_coverage[0],      
                            &me->memory.condition_norm[0],      
                            &me->memory.condition_norm_comment[0], 
                            sizeof(self_event_id_db)/sizeof(const char*),
                            &self_event_id_db[0],
                            sizeof(self_condition_id_db)/sizeof(const char*),
                            &self_condition_id_db[0]);      

    me->do_init      = do_init;
    me->do_terminal  = do_terminal;

    me->base.do_init      = self_myWalk2_do_init;
    me->base.do_event     = self_myWalk2_do_event;
    me->base.do_condition = self_myWalk2_do_condition;
    me->base.do_terminal  = self_myWalk2_do_terminal;
}

void
myWalk2_execute(myWalk2_t*   me,
                my_data_t* subject,
                void   (*do_init)(myWalk2_t* me),
                void   (*do_terminal)(myWalk2_t* me, hwut_sm_state_t*))
{
    myWalk2_init(me, subject, do_init, do_terminal);
    hwut_sm_walker_walk(&me->base, &self_states[11], 1);
}

int
myWalk2_state_is_real(const hwut_sm_state_t* State)
{
    return State->id < myWalk2___BeyondId;
}

static void   
self_myWalk3_do_init(hwut_sm_walker_t* alter_ego)
{
    myWalk3_t* me = (myWalk3_t*)alter_ego;
    if( me->do_init != (void*)0 ) {
        me->do_init(me);
    }
}

static void   
self_myWalk3_do_event(hwut_sm_walker_t* alter_ego, hwut_sm_state_t* state, int EventId)
{
    myWalk3_t* me = (myWalk3_t*)alter_ego;
#   define      self (*((my_data_t*)(me->subject)))

    {

    (void)me;

    switch( EventId ) {
#   line 78 "total-sm_walker.c"
    case myWalk3_BUZZ: {
    }
    break;

    }

#   line 80 "total-sm_walker.c"
 
      printf("do_event:    { user_data: ((%p)); name: %s; event: %s; }\n", 
             me->subject, state->name, me->base.aux.event_id_db.begin[EventId]);  
   


#   undef self
    }
}

static int   
self_myWalk3_do_condition(hwut_sm_walker_t* alter_ego, hwut_sm_state_t* state, int ConditionId)
{
    myWalk3_t* me = (myWalk3_t*)alter_ego;
#   define      self (*((my_data_t*)(me->subject)))

    (void)me;

    switch( ConditionId ) {
    case 0: return 1; /* Condition 0 --> Always OK */
#   line 88 "total-sm_walker.c"
    case myWalk3_COLD: {
 printf("COLD?\n");     }
    break;
#   line 87 "total-sm_walker.c"
    case myWalk3_WARM: {
 printf("WARM?\n");     }
    break;

    }

#   line 90 "total-sm_walker.c"
 
        assert(ConditionId != 0);
        printf("condition:   { user_data: ((%p)); name: %s; condition_id: %s; result: %s; }\n", 
               me->subject, state->name, me->base.aux.condition_id_db.begin[ConditionId], "OK"); 
        return 1;
   


#   undef self
    return 1;
}

static void   
self_myWalk3_do_terminal(hwut_sm_walker_t* alter_ego, hwut_sm_state_t* state_p)
{
    myWalk3_t* me = (myWalk3_t*)alter_ego;
    if( me->do_terminal != (void*)0 ) {
        me->do_terminal(me, state_p);
    }
}

hwut_sm_stack_frame_t  self_stack_memory_myWalk3[6 + 1];

static void
myWalk3_init(myWalk3_t*   me,
            my_data_t* subject,
            void   (*do_init)(myWalk3_t* me),
            void   (*do_terminal)(myWalk3_t* me, hwut_sm_state_t*))
{
    hwut_sm_walker_init(&me->base, 6 + 1, &self_stack_memory_myWalk3[0]); 

    me->subject       = subject;
    me->base.state_db = &self_states[0];

    hwut_sm_walker_aux_init(&me->base.aux, 
                            /* State index offset */14, /* State number */3,
                            &me->memory.state_coverage[0],                  
                            &me->memory.state_forbidden[0],                  
                            &me->memory.state_forbidden_comment[0],                  
                            /* Condition id offset */3, /* Condition number */3,
                            &me->memory.condition_coverage[0],      
                            &me->memory.condition_norm[0],      
                            &me->memory.condition_norm_comment[0], 
                            sizeof(self_event_id_db)/sizeof(const char*),
                            &self_event_id_db[0],
                            sizeof(self_condition_id_db)/sizeof(const char*),
                            &self_condition_id_db[0]);      

    me->do_init      = do_init;
    me->do_terminal  = do_terminal;

    me->base.do_init      = self_myWalk3_do_init;
    me->base.do_event     = self_myWalk3_do_event;
    me->base.do_condition = self_myWalk3_do_condition;
    me->base.do_terminal  = self_myWalk3_do_terminal;
}

void
myWalk3_execute(myWalk3_t*   me,
                my_data_t* subject,
                void   (*do_init)(myWalk3_t* me),
                void   (*do_terminal)(myWalk3_t* me, hwut_sm_state_t*))
{
    myWalk3_init(me, subject, do_init, do_terminal);
    hwut_sm_walker_walk(&me->base, &self_states[14], 1);
}

int
myWalk3_state_is_real(const hwut_sm_state_t* State)
{
    return State->id < myWalk3___BeyondId;
}
