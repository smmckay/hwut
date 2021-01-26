/* State Machine Walker 'hwut_sm_walker'.
 *
 * The 'print' function.
 *
 * This function prints the current path of the state machine. Sub-cases:
 *
 * (1) Empty stack.
 * (2) Stack size: one element.
 * (3) Stack size: two elements.
 * (4) Stack size: full - 1.
 * (5) Stack size: full.
 *
 * (C) Frank-Rene Schaefer
 *___________________________________________________________________________*/
#include "hwut_unit.h"
#include "hwut_sm_walker.h"

#include "stdio.h"
#include "stdarg.h"
#include "assert.h"
#include "sm_walker-common.h"

extern hwut_sm_state_t  states[6];

const char* (self_my_event_id_db[]) = {
    "NoEvent",
    "THE_GREAT_EVENT",
};

const char* (self_my_condition_id_db[]) = {
    "NoCondition",
    "MARVELOUS",
    "EXCELLENT",
    "FORMIDABLE",
};

hwut_sm_transition_t TM_0[] = { { 0,  0, &states[1] } };
hwut_sm_transition_t TM_1[] = { { 0, -1, &states[2] } };
hwut_sm_transition_t TM_2[] = { { 1, 2, &states[3] } };
hwut_sm_transition_t TM_3[] = { { 1, 3, &states[4] } };
hwut_sm_transition_t TM_4[] = { { 1, 4, &states[5] } };

hwut_sm_state_t states[6] = {
   { 0, "A_STATE_A", 0, &TM_0[0], &TM_0[1] },
   { 1, "B_STATE_B", 1, &TM_1[0], &TM_1[1] },
   { 2, "C_STATE_C", 2, &TM_2[0], &TM_2[1] },
   { 3, "D_STATE_D", 1, &TM_3[0], &TM_3[1] },
   { 4, "E_STATE_E", 0, &TM_4[0], &TM_4[0] },
};


hwut_sm_stack_frame_t  stack_memory[7];

static void 
do_my_init(hwut_sm_walker_t* me) 
{ 
    printf("do_init:\n");
    hwut_sm_walker_print(stdout, me, 50);
    printf("\n\n____________________________________________________________\n");
}

static void 
do_my_event(hwut_sm_walker_t* me, hwut_sm_state_t* StateP, int EventId) 
{ 
    printf("do_event:\n");
    hwut_sm_walker_print(stdout, me, 50);
    printf("\n\n____________________________________________________________\n");
}

static int 
do_my_condition(hwut_sm_walker_t* me, hwut_sm_state_t* StateP, int ConditionId) 
{ 
    printf("on_condition:\n");
    hwut_sm_walker_print(stdout, me, 50);
    printf("\n\n____________________________________________________________\n");
    if( ConditionId == 1 ) {
        return 0; /* I.e. not MARVERLOUS. */
    }
    else { 
        return 1;
    }
}

static void 
do_my_terminal(hwut_sm_walker_t* me, hwut_sm_state_t* state) 
{ 
    printf("do_terminal:\n");
    hwut_sm_walker_print(stdout, me, 50);
    printf("\n\n____________________________________________________________\n");
}

static int 
do_my_condition_plain(hwut_sm_walker_t* me, hwut_sm_state_t* StateP, int ConditionId) 
{ 
    if( ConditionId == 1 ) {
        return 0; /* I.e. not MARVERLOUS. */
    }
    else { 
        return 1;
    }
}

static void 
do_my_terminal_plain(hwut_sm_walker_t* me, hwut_sm_state_t* state) 
{ 
    printf("do_terminal:\n");
    hwut_sm_walker_print_plain(stdout, me);
    printf("\n\n____________________________________________________________\n");
}

int
main(int argc, char** argv) 
{
    hwut_sm_walker_t  walker;

	hwut_info("State Machine Walker: print;\n"
              "CHOICES: pretty, plain;\n");

    hwut_sm_walker_init(&walker, 
                        /* stack size   */ 7, 
                        /* stack memory */ stack_memory); 

    common_setup(&walker);

    walker.aux.event_id_db.begin     = &self_my_event_id_db[0];
    walker.aux.event_id_db.end       = &self_my_event_id_db[sizeof(self_event_id_db)/sizeof(const char*)];
    walker.aux.condition_id_db.begin = &self_my_condition_id_db[0];
    walker.aux.condition_id_db.end   = &self_my_condition_id_db[sizeof(self_condition_id_db)/sizeof(const char*)];

    hwut_if_choice("pretty") { 
        walker.do_init      = do_my_init;
        walker.do_event     = do_my_event;
        walker.do_condition = do_my_condition;
        walker.do_terminal  = do_my_terminal;
    }
    hwut_if_choice("plain") {
        walker.do_init      = (void*)0;
        walker.do_event     = (void*)0;
        walker.do_condition = do_my_condition_plain;
        walker.do_terminal  = do_my_terminal_plain;
    }

    hwut_sm_walker_walk(&walker, &states[0], 7);

    return 0;
}
