/* State Machine Walker 'hwut_sm_walker'.
 *
 * Reach the maximum number of path elements. Setup a simple four state
 * state machine. 
 *
 *   .-----.              .-----.              .-----.              .-----.
 *   |  0  |-- event 0 ->-|  1  |-- event 1 ->-|  2  |-- event 2 ->-|  3  |
 *   '-----'              '-----'              '-----'              '-----'
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

hwut_sm_state_t  states[4];

/* Targets: '0' -- no condition
 *          '1' -- callback 'do_condition' will reply 'OK'
 *          '2' -- callback 'do_condition' will reply 'FAIL'
 *                                                                           */ 

/* Events: Only one event '66' connected to the targets.
 *                                                                           */ 
hwut_sm_transition_t TM_0_loop[] = { { 66, 0, &states[0] } };
hwut_sm_transition_t TM_0[] = { { 66, 0, &states[1] } };  
hwut_sm_transition_t TM_1[] = { { 66, 0, &states[2] } }; 
hwut_sm_transition_t TM_2[] = { { 66, 0, &states[3] } };

hwut_sm_stack_frame_t  stack_memory[256];

#include "sm_walker-common.h"

static void  test();

int
main(int argc, char** argv) 
{
	hwut_info("State Machine Walker: Max. number of path elements;\n"
              "CHOICES: linear, loop;");

    hwut_if_choice("linear") {
        hwut_sm_state_init(&states[0], "Init",     1, TM_0);
        hwut_sm_state_init(&states[1], "1st",      1, TM_1);
        hwut_sm_state_init(&states[2], "2nd",      1, TM_2);
        hwut_sm_state_init(&states[3], "Terminal", 0, (void*)0);
    }
    hwut_if_choice("loop") {
        hwut_sm_state_init(&states[0], "Init",     1, TM_0_loop);
    }

    test();

    return 0;
}

static void
test()
{
    hwut_sm_walker_t  walker;
    int               max_depth = 0;

    for(max_depth=3; max_depth != 7; ++max_depth) {
        printf("Max. Depth: %i\n\n", max_depth);

        /* Write something in the stack to make sure it it not overwritten. */
        stack_memory[max_depth].transition_p = (void*)0xC0FFEEBA;

        hwut_sm_walker_init(&walker, 
                            /* stack size   */ max_depth, 
                            /* stack memory */ stack_memory); 

        common_setup(&walker);

        hwut_sm_walker_walk(&walker, &states[0], 256);

        assert(stack_memory[max_depth].transition_p == (void*)0xC0FFEEBA);
    }
}

