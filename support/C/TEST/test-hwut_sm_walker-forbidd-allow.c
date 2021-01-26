/* State Machine Walker 'hwut_sm_walker'.
 *
 * Checks on the forbidding and allowing on states on the path. That is, 
 * the following API is tested:
 *
 *         hwut_sm_state_forbid(me, StateId, Comment);
 *         hwut_sm_state_allow(me, StateId);
 *         hwut_sm_state_allow_all(me);
 *         hwut_sm_state_happened(me, StateId);
 *
 * Use a linear state machine:
 *                                                                  
 *   .-----.              .-----.              .-----.              .-----.
 *   |  0  |-- event 0 -->|  1  |-- event 1 -->|  2  |-- event 2 -->|  3  |
 *   '-----'              '-----'              '-----'              '-----'
 *
 * (1) 4 tests:  Before starting forbid state 'N' from {0, 1, 2, 3}. Then,
 *               run until the assert is hit.
 *
 * (2) 4 tests:  Before starting forbid state 'N' from {0, 1, 2, 3}. Then,
 *               allow the forbidden state. Run and make sure that end has 
 *               been reached. 
 *
 * (3) 16 tests: Forbid any combination of tests. Allow all, and make sure the
 *               tests run through. 
 *
 * The function 'hwut_sm_state_happened()' is checked at any event step through
 * the state machine. It checks on all states which happend before. For that, 
 * a dedicated 'do_event' function is defined.
 *                                                                   
 * (C) Frank-Rene Schaefer
 *___________________________________________________________________________*/
#include "hwut_unit.h"
#include "hwut_sm_walker.h"

#include "stdbool.h"
#include "stdio.h"
#include "stdarg.h"
#include "assert.h"

#define self_state_n     4
#define self_condition_n 1
static hwut_sm_state_t   states[self_state_n];

hwut_sm_transition_t TM_0[] = { { 0, 0, &states[1] } }; /* no condition   */
hwut_sm_transition_t TM_1[] = { { 1, 0, &states[2] } }; /* no condition   */
hwut_sm_transition_t TM_2[] = { { 2, 0, &states[3] } }; /* no condition   */

hwut_sm_stack_frame_t  stack_memory[256];

static hwut_sm_state_t  states[4] = {
   { 0, "0", 0, &TM_0[0], &TM_0[1] },
   { 1, "1", 0, &TM_1[0], &TM_1[1] },
   { 2, "2", 0, &TM_2[0], &TM_2[1] },
   { 3, "3", 0, (void*)0, (void*)0, },
};

#include "sm_walker-common.h"

static void my_do_event(hwut_sm_walker_t* me, hwut_sm_state_t* StateP, int EventId);
static void my_do_terminal(hwut_sm_walker_t* me, hwut_sm_state_t* StateP);
static void my_init(hwut_sm_walker_t* walker);

int
main(int argc, char** argv) 
{
    hwut_sm_walker_t  walker;
    int               i=0;
    int               bitmask=0;

	hwut_info("State Machine Walker: Forbid and allow states;\n" 
              "CHOICES: 1a, 1b, 1c, 1d, 2, 3;\n")

    my_init(&walker);

    hwut_if_choice("1a") {
        hwut_sm_state_forbid(&walker, 0, "state zero bad!");
        hwut_sm_walker_walk(&walker, &states[0], 7);
    }
    hwut_if_choice("1b") {
        hwut_sm_state_forbid(&walker, 1, "state one bad!");
        hwut_sm_walker_walk(&walker, &states[0], 7);
    }
    hwut_if_choice("1c") {
        hwut_sm_state_forbid(&walker, 2, "state two bad!");
        hwut_sm_walker_walk(&walker, &states[0], 7);
    }
    hwut_if_choice("1d") {
        hwut_sm_state_forbid(&walker, 3, "state three bad!");
        hwut_sm_walker_walk(&walker, &states[0], 7);
    }

    hwut_if_choice("2") {
        for(i=0; i<4; ++i) {
            printf("-- forbid and allow %i --\n", i);
            hwut_sm_state_forbid(&walker, i, "bad state!");
            hwut_sm_state_allow(&walker, i);
            hwut_sm_walker_walk(&walker, &states[0], 7);
        }
    }
    hwut_if_choice("3") {
        for(bitmask=0; bitmask<16; ++bitmask) {
            /* Apply any combination of forbidden states. Use a bitmask to
             * iterate over combinations.                                    */
            printf("-- forbid and allow ");
            for(i=0; i<4; ++i) {
                if( (1<<i) & bitmask ) {
                    printf("%i ", i);
                    hwut_sm_state_forbid(&walker, i, "bad state!");
                }
            }
            printf("--\n");
            /* Allow everything. */
            hwut_sm_state_allow_all(&walker);
            /* Walk freely. */
            hwut_sm_walker_walk(&walker, &states[0], 7);
        }
    }
    return 0;
}

static void 
my_do_event(hwut_sm_walker_t* me, hwut_sm_state_t* StateP, int EventId)
{
    printf("state[%i].my_do_event\n", StateP->id);
    /* Check whether all previous states have 'happend'. */
    switch(StateP->id) {
    case 0: 
        hwut_verify(false == hwut_sm_state_happened(me, 0));
        hwut_verify(false == hwut_sm_state_happened(me, 1));
        hwut_verify(false == hwut_sm_state_happened(me, 2));
        hwut_verify(false == hwut_sm_state_happened(me, 3));
        break;
    case 1: 
        hwut_verify(true == hwut_sm_state_happened(me, 0));
        hwut_verify(false == hwut_sm_state_happened(me, 1));
        hwut_verify(false == hwut_sm_state_happened(me, 2));
        hwut_verify(false == hwut_sm_state_happened(me, 3));
        break;
    case 2: 
        hwut_verify(true == hwut_sm_state_happened(me, 0));
        hwut_verify(true == hwut_sm_state_happened(me, 1));
        hwut_verify(false == hwut_sm_state_happened(me, 2));
        hwut_verify(false == hwut_sm_state_happened(me, 3));
        break;
    default:
        hwut_verify(false);
    }
}

static void 
my_do_terminal(hwut_sm_walker_t* me, hwut_sm_state_t* StateP) 
{
    printf("state[%i].my_do_terminal\n", StateP->id);
    hwut_verify(true  == hwut_sm_state_happened(me, 0));
    hwut_verify(true  == hwut_sm_state_happened(me, 1));
    hwut_verify(true  == hwut_sm_state_happened(me, 2));
    hwut_verify(false == hwut_sm_state_happened(me, 3));
}

static void
my_init(hwut_sm_walker_t* walker)
{
    static struct { 
        hwut_sm_condition_coverage_t  condition_coverage[self_condition_n]; 
        hwut_sm_condition_norm_t      condition_norm[self_condition_n];
        const char*                   condition_norm_comment[self_condition_n];

        int          state_coverage[self_state_n]; 
        int          state_forbidden[self_state_n];
        const char*  state_forbidden_comment[self_state_n];
    } memory;

    static const char* (event_id_db[]) = {
        "Event0", "Event1", "Event2", "Event3"
    };
    static const char* (condition_id_db[]) = {
        "Cond0", "Cond1", "Cond2", "Cond3"
    };

    hwut_sm_walker_init(walker, 
                        /* stack size   */ 256, 
                        /* stack memory */ stack_memory); 

    common_setup(walker);

    walker->do_init      = (void*)0;
    walker->do_condition = (void*)0;
    walker->do_event     = my_do_event;
    walker->do_terminal  = my_do_terminal;

    hwut_sm_walker_aux_init(&walker->aux, 
                            /* State index offset */0, self_state_n,
                            &memory.state_coverage[0],                  
                            &memory.state_forbidden[0],                  
                            &memory.state_forbidden_comment[0],                  
                            /* Condition id offset */1, self_condition_n,
                            &memory.condition_coverage[0],      
                            &memory.condition_norm[0],      
                            &memory.condition_norm_comment[0], 
                            4, &event_id_db[0], 
                            4, &condition_id_db[0]);
}
