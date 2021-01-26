/* State Machine Walker 'hwut_sm_walker'.
 *
 * Consider loops, that is possible iterations over the same states. The
 * simplest case is a single state that iterates on itself:
 *
 *                             .-----.
 *                   --------->|  0  |-- event 0 ---.
 *                             '-----'              |
 *                                '----<------------'
 * 
 * The loop break condition triggers when a state on a path is entered on the 
 * same event a maximum number of times. For two events involved in the 
 * iteration the diagram looks like the following:
 *
 *                                .----- event 1 ---.
 *                             .-----.              |
 *                   --------->|  0  |------>-------.
 *                             '-----'              |
 *                                '----- event 0 ---'
 * CHOICES:
 * 
 * 'loop':        A single state that iterates on itself.
 * 's-loop':      An initial state followed by a state that iterates on itself.
 * 'loop-s':      An iterating state followed by a single state.
 * 'loop2':       A loop over two states.
 *
 * 'butterfly':   Analgous to the 'loop'--only two iterating events.
 * 's-butterfly': 
 * 'butterfly-s':
 * 'butterfly2':
 *
 *
 * (C) Frank-Rene Schaefer
 *___________________________________________________________________________*/
#include "hwut_unit.h"
#include "hwut_sm_walker.h"

#include "stdio.h"
#include "stdarg.h"
#include "assert.h"

hwut_sm_state_t  states[4];

/* Events: Only one event '66' connected to the targets.
 *                                                                           */ 
hwut_sm_transition_t  TM_loop[]          = { { 88, 0, &states[0] } };
                                    
hwut_sm_transition_t  TM_s_loop_0[]      = { { 88, 0, &states[1] }, };
hwut_sm_transition_t  TM_s_loop_1[]      = { { 88, 0, &states[1] }, };
                                    
hwut_sm_transition_t  TM_loop_s_0[]      = { { 88, 0, &states[0] }, { 11, 0, &states[1] }, };
                                    
hwut_sm_transition_t  TM_loop2_0[]       = { { 11, 0, &states[1] }, };
hwut_sm_transition_t  TM_loop2_1[]       = { { 88, 0, &states[0] }, };

hwut_sm_transition_t  TM_butterfly[]     = { { 881, 0, &states[0] }, { 882, 0, &states[0] }, };

hwut_sm_transition_t  TM_s_butterfly_0[] = { { 11,  0, &states[1] }, };
hwut_sm_transition_t  TM_s_butterfly_1[] = { { 881, 0, &states[1] }, { 882, 0, &states[1] }, };
                 
hwut_sm_transition_t  TM_butterfly_s_0[] = { { 881, 0, &states[0] }, { 882, 0, &states[0] }, { 11, 0, &states[1] }, };

hwut_sm_transition_t  TM_butterfly2_0[]  = { { 11,  0, &states[1] }, };
hwut_sm_transition_t  TM_butterfly2_1[]  = { { 881, 0, &states[0] }, { 882, 0, &states[0] }, };


hwut_sm_stack_frame_t  stack_memory[10];

#include "sm_walker-common.h"

int
main(int argc, char** argv) 
{
    hwut_sm_walker_t  walker;
    int               max_loop_n = 2;

	hwut_info("State Machine Walker: Loops;\n" 
              "CHOICES: loop,      s-loop,      loop-s,      loop2, "
              "         butterfly, s-butterfly, butterfly-s, butterfly2;\n")

    hwut_sm_walker_init(&walker, 
                        /* stack size   */ 10, 
                        /* stack memory */ stack_memory); 

    common_setup(&walker);

    hwut_if_choice("loop") {
        hwut_sm_state_init(&states[0], "1st", 1, TM_loop);
        hwut_sm_state_init(&states[1], "2nd", 0, (void*)0);
    }
    hwut_if_choice("s-loop") {
        hwut_sm_state_init(&states[0], "1st", 1, TM_s_loop_0);
        hwut_sm_state_init(&states[1], "2nd", 1, TM_s_loop_1);
    }
    hwut_if_choice("loop-s") {
        hwut_sm_state_init(&states[0], "1st", 2, TM_loop_s_0);
        hwut_sm_state_init(&states[1], "2nd", 0, (void*)0);
    }
    hwut_if_choice("loop2") {
        max_loop_n = 3;
        hwut_sm_state_init(&states[0], "1st", 1, TM_loop2_0);
        hwut_sm_state_init(&states[1], "2nd", 1, TM_loop2_1);
    }
    hwut_if_choice("butterfly") {
        max_loop_n = 1;
        hwut_sm_state_init(&states[0], "1st", 2, TM_butterfly);
        hwut_sm_state_init(&states[1], "2nd", 0, (void*)0);
    }
    hwut_if_choice("s-butterfly") {
        max_loop_n = 1;
        hwut_sm_state_init(&states[0], "1st", 1, TM_s_butterfly_0);
        hwut_sm_state_init(&states[1], "2nd", 2, TM_s_butterfly_1);
    }
    hwut_if_choice("butterfly-s") {
        max_loop_n = 1;
        hwut_sm_state_init(&states[0], "1st", 3, TM_butterfly_s_0);
        hwut_sm_state_init(&states[1], "2nd", 0, (void*)0);
    }
    hwut_if_choice("butterfly2") {
        max_loop_n = 3;
        hwut_sm_state_init(&states[0], "1st", 1, TM_butterfly2_0);
        hwut_sm_state_init(&states[1], "2nd", 2, TM_butterfly2_1);
    }

    hwut_sm_walker_walk(&walker, &states[0], max_loop_n);

    return 0;
}

