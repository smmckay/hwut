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
 * The test checks paths of a single step:
 *
 *   (1) Path with an unconditional single step.
 *   (2) Path where the conditional step is acknowledged.
 *   (3) Path where the condition is denied.
 *
 *                       ,----- event 1 --->----.
 *                 .-----.                     .-----.
 *                 |  0  |----- event 2 ---> --|  1  |
 *                 '-----'                     '-----'
 *                       '----- event 3 --->----'
 *
 * CHOICES: X-*   =>  They differ only in the initial transition from init 
 *                    state to the '0' state.
 *
 *                                      ,----- event 1 --->----.
 *   .-----.                      .-----.                     .-----.
 *   |  2  |------ event 0 --->---|  0  |----- event 2 ---> --|  1  |
 *   '-----'                      '-----'                     '-----'
 *                                      '----- event 3 --->----'
 *
 * CHOICES: Y-*   =>  They differ only in the initial transition from init 
 *                    state to the '0' state.
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
hwut_sm_transition_t TM_pre[] = {
   /* Transitions, that DO NOT rely on a 'user condition.'                   */
   { 1, 0, &states[0] }
};

/* Transition from 'Terminal' to 'Posthistoric'                              */
hwut_sm_transition_t TM_post[] = {
   /* Transitions, that DO NOT rely on a 'user condition.'                   */
   { 1, 0, &states[2] }
};

/* Transitions from 'Init' to 'Terminal'                                     */
hwut_sm_transition_t TM_woc[] = {
   /* Transitions, that DO NOT rely on a 'user condition.'                   */
   { 1, 0, &states[1] },
   { 2, 0, &states[1] },
   { 3, 0, &states[1] }
};

hwut_sm_transition_t TM_wcg[] = {
   /* Transitions, that DO rely on a 'user condition.' Condition is OK.      */
   { 1, 1, &states[1] },
   { 2, 1, &states[1] },
   { 3, 1, &states[1] }
};

hwut_sm_transition_t TM_wcf[] = {
   /* Transitions, that DO rely on a 'user condition.' Condition is FAIL.    */
   { 1, 2, &states[1] },
   { 2, 2, &states[1] },
   { 3, 2, &states[1] }
};

hwut_sm_transition_t TM_1stg[] = {
   { 1, /* good */ 1, &states[1] },
   { 2, /* fail */ 2, &states[1] },
   { 3, /* fail */ 2, &states[1] }
};

hwut_sm_transition_t TM_2stg[] = {
   { 1, /* fail */ 2, &states[1] },
   { 2, /* good */ 1, &states[1] },
   { 3, /* fail */ 2, &states[1] }
};

hwut_sm_transition_t TM_3stg[] = {
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

	hwut_info("State Machine Walker: 1 step;\n" 
              "CHOICES: "
              "without-condition,     condition-fail,   condition-good,   first-good,   second-good,   third-good, "
              "X-without-condition, X-condition-fail, X-condition-good, X-first-good, X-second-good, X-third-good, "
              "Y-without-condition, Y-condition-fail, Y-condition-good, Y-first-good, Y-second-good, Y-third-good;");

    hwut_sm_walker_init(&walker, 
                        /* stack size   */ 256, 
                        /* stack memory */ stack_memory); 
    common_setup(&walker);

    hwut_if_choice("without-condition") {
        init_state = &states[0];
        hwut_sm_state_init(&states[0], "Init",     3, TM_woc); 
        hwut_sm_state_init(&states[1], "Terminal", 0, (void*)0); 
    }
    hwut_if_choice("condition-good") {
        init_state = &states[0];
        hwut_sm_state_init(&states[0], "Init",     3, TM_wcg); 
        hwut_sm_state_init(&states[1], "Terminal", 0, (void*)0); 
    }

    hwut_if_choice("condition-fail") {
        init_state = &states[0];
        hwut_sm_state_init(&states[0], "Init",     3, TM_wcf); 
        hwut_sm_state_init(&states[1], "Terminal", 0, (void*)0); 
    }
    hwut_if_choice("first-good") {
        init_state = &states[0];
        hwut_sm_state_init(&states[0], "Init",     3, TM_1stg); 
        hwut_sm_state_init(&states[1], "Terminal", 0, (void*)0); 
    }
    hwut_if_choice("second-good") {
        init_state = &states[0];
        hwut_sm_state_init(&states[0], "Init",     3, TM_2stg); 
        hwut_sm_state_init(&states[1], "Terminal", 0, (void*)0); 
    }
    hwut_if_choice("third-good") {
        init_state = &states[0];
        hwut_sm_state_init(&states[0], "Init",     3, TM_3stg); 
        hwut_sm_state_init(&states[1], "Terminal", 0, (void*)0); 
    }

    hwut_if_choice("X-without-condition") {
        init_state = &states[2];
        hwut_sm_state_init(&states[2], "Prehistoric", 1, TM_pre); 
        hwut_sm_state_init(&states[0], "Init",        3, TM_woc); 
        hwut_sm_state_init(&states[1], "Terminal",    0, (void*)0); 
    }
    hwut_if_choice("X-condition-good") {
        init_state = &states[2];
        hwut_sm_state_init(&states[2], "Prehistoric", 1, TM_pre); 
        hwut_sm_state_init(&states[0], "Init",        3, TM_wcg); 
        hwut_sm_state_init(&states[1], "Terminal",    0, (void*)0); 
    }

    hwut_if_choice("X-condition-fail") {
        init_state = &states[2];
        hwut_sm_state_init(&states[2], "Prehistoric", 1, TM_pre); 
        hwut_sm_state_init(&states[0], "Init",        3, TM_wcf); 
        hwut_sm_state_init(&states[1], "Terminal",    0, (void*)0); 
    }
    hwut_if_choice("X-first-good") {
        init_state = &states[2];
        hwut_sm_state_init(&states[2], "Prehistoric", 1, TM_pre); 
        hwut_sm_state_init(&states[0], "Init",        3, TM_1stg); 
        hwut_sm_state_init(&states[1], "Terminal",    0, (void*)0); 
    }
    hwut_if_choice("X-second-good") {
        init_state = &states[2];
        hwut_sm_state_init(&states[2], "Prehistoric", 1, TM_pre); 
        hwut_sm_state_init(&states[0], "Init",        3, TM_2stg); 
        hwut_sm_state_init(&states[1], "Terminal",    0, (void*)0); 
    }
    hwut_if_choice("X-third-good") {
        init_state = &states[2];
        hwut_sm_state_init(&states[2], "Prehistoric", 1, TM_pre); 
        hwut_sm_state_init(&states[0], "Init",        3, TM_3stg); 
        hwut_sm_state_init(&states[1], "Terminal",    0, (void*)0); 
    }

    hwut_if_choice("Y-without-condition") {
        init_state = &states[0];
        hwut_sm_state_init(&states[0], "Init",         3, TM_woc); 
        hwut_sm_state_init(&states[1], "Terminal",     1, TM_post);
        hwut_sm_state_init(&states[2], "Posthistoric", 0, (void*)0); 
    }
    hwut_if_choice("Y-condition-good") {
        init_state = &states[0];
        hwut_sm_state_init(&states[0], "Init",         3, TM_wcg); 
        hwut_sm_state_init(&states[1], "Terminal",     1, TM_post);
        hwut_sm_state_init(&states[2], "Posthistoric", 0, (void*)0); 
    }

    hwut_if_choice("Y-condition-fail") {
        init_state = &states[0];
        hwut_sm_state_init(&states[0], "Init",         3, TM_wcf); 
        hwut_sm_state_init(&states[1], "Terminal",     1, TM_post);
        hwut_sm_state_init(&states[2], "Posthistoric", 0, (void*)0); 
    }
    hwut_if_choice("Y-first-good") {
        init_state = &states[0];
        hwut_sm_state_init(&states[0], "Init",         3, TM_1stg); 
        hwut_sm_state_init(&states[1], "Terminal",     1, TM_post);
        hwut_sm_state_init(&states[2], "Posthistoric", 0, (void*)0); 
    }
    hwut_if_choice("Y-second-good") {
        init_state = &states[0];
        hwut_sm_state_init(&states[0], "Init",         3, TM_2stg); 
        hwut_sm_state_init(&states[1], "Terminal",     1, TM_post);
        hwut_sm_state_init(&states[2], "Posthistoric", 0, (void*)0); 
    }
    hwut_if_choice("Y-third-good") {
        init_state = &states[0];
        hwut_sm_state_init(&states[0], "Init",         3, TM_3stg); 
        hwut_sm_state_init(&states[1], "Terminal",     1, TM_post);
        hwut_sm_state_init(&states[2], "Posthistoric", 0, (void*)0); 
    }


    hwut_sm_walker_walk(&walker, init_state, 7);

    return 0;
}
