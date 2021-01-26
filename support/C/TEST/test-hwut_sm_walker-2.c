/* State Machine Walker 'hwut_sm_walker'.
 *
 * Consider a state machine consisting of a line of four states. 
 *
 *   .-----.              .-----.              .-----.              .-----.
 *   |  0  |-- event 0 ->-|  1  |-- event 1 ->-|  2  |-- event 2 ->-|  3  |
 *   '-----'              '-----'              '-----'              '-----'
 *
 * Each transition can either be associated with:
 *
 *  'n' for 'no condition'. The transition always passes.
 * 
 *  'g' for 'good condition'. The transition always passes after interacting
 *      with the callback 'do_condition'.
 *
 *  'f' for 'fail condition'. The transition never passes because the callback
 *      'do_condition' returns false.
 *
 * The CHOICES of this test permutate all combinations of 'n', 'g', and 'f'
 * flags for each transition.
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
hwut_sm_transition_t TM_0_n[] = { { 66, 0, &states[1] } }; /* no condition   */
hwut_sm_transition_t TM_0_g[] = { { 66, 1, &states[1] } }; /* good condition */
hwut_sm_transition_t TM_0_f[] = { { 66, 2, &states[1] } }; /* fail condition */

hwut_sm_transition_t TM_1_n[] = { { 66, 0, &states[2] } }; /* no condition   */
hwut_sm_transition_t TM_1_g[] = { { 66, 1, &states[2] } }; /* good condition */
hwut_sm_transition_t TM_1_f[] = { { 66, 2, &states[2] } }; /* fail condition */

hwut_sm_transition_t TM_2_n[] = { { 66, 0, &states[3] } }; /* no condition   */
hwut_sm_transition_t TM_2_g[] = { { 66, 1, &states[3] } }; /* good condition */
hwut_sm_transition_t TM_2_f[] = { { 66, 2, &states[3] } }; /* fail condition */

hwut_sm_stack_frame_t  stack_memory[256];

#include "sm_walker-common.h"

int
main(int argc, char** argv) 
{
    hwut_sm_walker_t  walker;
    int               c[3];

	hwut_info("State Machine Walker: 4 states in line;\n" 
              "CHOICES: "
              "nnn, nng, nnf, ngn, ngg, ngf, nfn, nfg, nff, "
              "gnn, gng, gnf, ggn, ggg, ggf, gfn, gfg, gff, "
              "fnn, fng, fnf, fgn, fgg, fgf, ffn, ffg, fff;\n") 

    c[0] = argv[1][0];
    c[1] = argv[1][1];
    c[2] = argv[1][2];
    
    hwut_sm_walker_init(&walker, 
                        /* stack size   */ 256, 
                        /* stack memory */ stack_memory); 

    common_setup(&walker);

    switch( c[0] ) {
    case 'n': hwut_sm_state_init(&states[0], "Init", 1, TM_0_n); break;
    case 'g': hwut_sm_state_init(&states[0], "Init", 1, TM_0_g); break;
    case 'f': hwut_sm_state_init(&states[0], "Init", 1, TM_0_f); break;
    }

    switch( c[1] ) {
    case 'n': hwut_sm_state_init(&states[1], "1st", 1, TM_1_n); break;
    case 'g': hwut_sm_state_init(&states[1], "1st", 1, TM_1_g); break;
    case 'f': hwut_sm_state_init(&states[1], "1st", 1, TM_1_f); break;
    }

    switch( c[2] ) {
    case 'n': hwut_sm_state_init(&states[2], "2nd", 1, TM_2_n); break;
    case 'g': hwut_sm_state_init(&states[2], "2nd", 1, TM_2_g); break;
    case 'f': hwut_sm_state_init(&states[2], "2nd", 1, TM_2_f); break;
    }

    hwut_sm_state_init(&states[3], "Terminal", 0, (void*)0);

    hwut_sm_walker_walk(&walker, &states[0], 7);

    return 0;
}

