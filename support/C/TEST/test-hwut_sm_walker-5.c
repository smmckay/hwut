/* State Machine Walker 'hwut_sm_walker'.
 *
 * Forks. 
 *
 * CHOICES:
 *
 *  '0-open':  Init state forks with open ends.
 *  '0-losed': Init state forks with closed ends (same terminal state).
 *  '1-open':  Prehistoric state before Init. Init state forks with open ends.
 *  '1-losed': Prehistoric state before Init. Init state forks with closed 
 *             ends (same terminal state).
 *
 * The walk the paths with different stack sizes (stack size = max. number 
 * of path elements).
 *
 * (C) Frank-Rene Schaefer
 *___________________________________________________________________________*/
#include "hwut_unit.h"
#include "hwut_sm_walker.h"

#include "stdio.h"
#include "stdarg.h"
#include "assert.h"

hwut_sm_state_t  states[10];

/* Targets: '0' -- no condition
 *          '1' -- callback 'do_condition' will reply 'OK'
 *          '2' -- callback 'do_condition' will reply 'FAIL'
 *                                                                           */ 

/* Events: Only one event '66' connected to the targets.
 *                                                                           */ 
hwut_sm_transition_t TM_pre[] = { { 66, 0, &states[0] } }; 
hwut_sm_transition_t TM_0[]   = { { 11, 0, &states[1] }, 
                                  { 22, 0, &states[3] } 
};  
hwut_sm_transition_t TM_1[]   = { { 66, 0, &states[2] } }; 
hwut_sm_transition_t TM_2[]   = { { 66, 0, &states[5] } };
hwut_sm_transition_t TM_3[]   = { { 66, 0, &states[4] } };
hwut_sm_transition_t TM_4[]   = { { 66, 0, &states[5] } };

hwut_sm_stack_frame_t  stack_memory[256];

#include "sm_walker-common.h"

int
main(int argc, char** argv) 
{
    hwut_sm_walker_t  walker;
    hwut_sm_state_t*  init_state;

	hwut_info("State Machine Walker: Forks;\n"
              "CHOICES: 0-open, 0-closed, 1-open, 1-closed;");

    hwut_if_choice("0-open") {
        init_state = &states[0];

        hwut_sm_state_init(&states[0], "0", 2, TM_0);
        hwut_sm_state_init(&states[1], "1", 1, TM_1);
        hwut_sm_state_init(&states[2], "2", 0, (void*)0);
        hwut_sm_state_init(&states[3], "3", 1, TM_3);
        hwut_sm_state_init(&states[4], "4", 0, (void*)0);
    }
    hwut_if_choice("0-closed") {
        init_state = &states[0];

        hwut_sm_state_init(&states[0], "0", 2, TM_0);
        hwut_sm_state_init(&states[1], "1", 1, TM_1);
        hwut_sm_state_init(&states[2], "2", 1, TM_2);
        hwut_sm_state_init(&states[3], "3", 1, TM_3);
        hwut_sm_state_init(&states[4], "4", 1, TM_4);
        hwut_sm_state_init(&states[5], "5", 0, (void*)0);
    }
    hwut_if_choice("1-open") {
        init_state = &states[6];
        hwut_sm_state_init(&states[6], "PRE", 1, TM_pre);

        hwut_sm_state_init(&states[0], "0", 2, TM_0);
        hwut_sm_state_init(&states[1], "1", 1, TM_1);
        hwut_sm_state_init(&states[2], "2", 0, (void*)0);
        hwut_sm_state_init(&states[3], "3", 1, TM_3);
        hwut_sm_state_init(&states[4], "4", 0, (void*)0);
    }
    hwut_if_choice("1-closed") {
        init_state = &states[6];
        hwut_sm_state_init(&states[6], "PRE", 1, TM_pre);

        hwut_sm_state_init(&states[0], "0", 2, TM_0);
        hwut_sm_state_init(&states[1], "1", 1, TM_1);
        hwut_sm_state_init(&states[2], "2", 1, TM_2);
        hwut_sm_state_init(&states[3], "3", 1, TM_3);
        hwut_sm_state_init(&states[4], "4", 1, TM_4);
        hwut_sm_state_init(&states[5], "5", 0, (void*)0);
    }

    hwut_sm_walker_init(&walker, 
                        /* stack size   */ 256, 
                        /* stack memory */ stack_memory); 

    common_setup(&walker);

    hwut_sm_walker_walk(&walker, init_state, 256);

    return 0;
}

