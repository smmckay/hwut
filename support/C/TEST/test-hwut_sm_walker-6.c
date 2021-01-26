/* State Machine Walker 'hwut_sm_walker'.
 *
 * This file tests the very basic functionality of the state machine walker. 
 * That is, it considers a state machine which consideres of a single step.
 * It tests whether all three callbacks are called properly, i.e.
 *
 *   do_init        -- whenever a new path begins.
 *   do_event        -- for the occurrence of an event.
 *   do_condition -- to check whether a condition is fulfilled.
 *   on_end          -- whenever a path has ended.
 *
 *         ,----- event 1 --->----.                                 
 *   .-----.                     .-----.                      .-----.
 *   |  0  |----- event 2 ---> --|  1  |------ event 0 --->---|  2  |
 *   '-----'                     '-----'                      '-----'
 *         '----- event 3 --->----'                                 
 *
 * (C) Frank-Rene Schaefer
 *___________________________________________________________________________*/
#include "hwut_unit.h"
#include "hwut_sm_walker.h"

#include "stdio.h"
#include "stdarg.h"
#include "assert.h"

hwut_sm_state_t  states[3];
/* states[0] -- Init State 
 * states[1] -- Terminal
 * states[2] -- Prehistoric (state before init in 'X-*' CHOICES.             */

/* Transition from 'Prehistoric' to 'Init'                                   */

/* Transition from 'Terminal' to 'Posthistoric'                              */
hwut_sm_transition_t TM_to2[] = {
   /* Transitions, that DO NOT rely on a 'user condition.'                   */
   { 1, 0, &states[2] }
};

hwut_sm_transition_t TM_to1[] = {
   { 1, /* fail */ 2, &states[1] },
   { 2, /* fail */ 2, &states[1] },
   { 3, /* good */ 1, &states[1] }
};


hwut_sm_stack_frame_t  stack_memory[256];

#include "sm_walker-common.h"

int
main(int argc, char** argv) 
{
    hwut_sm_walker_t  walker;
    hwut_sm_state_t*  init_state = (void*)0;

	hwut_info("State Machine Walker: Callbacks Deactivated;\n");

    hwut_sm_walker_init(&walker, 
                        /* stack size   */ 256, 
                        /* stack memory */ stack_memory); 
    common_setup(&walker);

    init_state = &states[0];
    hwut_sm_state_init(&states[0], "X", 3, TM_to1); 
    hwut_sm_state_init(&states[1], "Y", 1, TM_to2);
    hwut_sm_state_init(&states[2], "Z", 0, (void*)0); 

    printf("Without 'do_init'\n");
    {
        walker.do_init      = (void*)0;
        walker.do_event     = do_event;
        walker.do_condition = do_condition;
        walker.do_terminal  = do_terminal;

        hwut_sm_walker_walk(&walker, init_state, 7);
    }
    printf("Without 'do_event'\n");
    {
        walker.do_init      = do_init;
        walker.do_event     = (void*)0;
        walker.do_condition = do_condition;
        walker.do_terminal  = do_terminal;

        hwut_sm_walker_walk(&walker, init_state, 7);
    }
    printf("Without 'do_condition'\n");
    {
        walker.do_init      = do_init;
        walker.do_event     = do_event;
        walker.do_condition = (void*)0;
        walker.do_terminal  = do_terminal;

        hwut_sm_walker_walk(&walker, init_state, 7);
    }
    printf("Without 'do_terminal'\n");
    {
        walker.do_init      = do_init;
        walker.do_event     = do_event;
        walker.do_condition = do_condition;
        walker.do_terminal  = (void*)0;

        hwut_sm_walker_walk(&walker, init_state, 7);
    }

    return 0;
}
