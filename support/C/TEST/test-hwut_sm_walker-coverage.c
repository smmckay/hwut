/* State Machine Walker 'hwut_sm_walker'.
 *
 * Print the condition and state coverage. This is done at any state
 * along the state machine. Use a linear state machine:
 *                                                                  
 *   .-----.             .-----.             .-----.             .-----.
 *   |  0  |-- cond 0 -->|  1  |-- cond 1 -->|  2  |-- cond 2 -->|  3  |
 *   '-----'             '-----'             '-----'             '-----'
 * 
 * Step through all states inside the state machine and print the coverage
 * information.
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
#define self_condition_n 3
static hwut_sm_state_t   states[self_state_n];

hwut_sm_transition_t TM_0[] = { { 0,  1, &states[1] } }; 
hwut_sm_transition_t TM_1[] = { { 1, -2, &states[2] } };
hwut_sm_transition_t TM_2[] = { { 2,  3, &states[3] } };

hwut_sm_stack_frame_t  stack_memory[256];

static hwut_sm_state_t  states[4] = {
   { 0, "Zero",           0, &TM_0[0], &TM_0[1] },
   { 1, "One",            0, &TM_1[0], &TM_1[1] },
   { 2, "Two",            0, &TM_2[0], &TM_2[1] },
   { 3, "Four minus One", 0, (void*)0, (void*)0, },
};

#include "sm_walker-common.h"

static void my_do_event(hwut_sm_walker_t* me, hwut_sm_state_t* StateP, int ConditionId);
static int  my_do_condition(hwut_sm_walker_t* me, hwut_sm_state_t* StateP, int ConditionId);
static void my_do_terminal(hwut_sm_walker_t* me, hwut_sm_state_t* StateP);

static void my_init(hwut_sm_walker_t* walker);

int
main(int argc, char** argv) 
{
    hwut_sm_walker_t  walker;

	hwut_info("State Machine Walker: State and Condition Coverage;\n"); 

    my_init(&walker);
    hwut_sm_walker_walk(&walker, &states[0], 7);

    return 0;
}

static int 
my_do_condition(hwut_sm_walker_t* me, hwut_sm_state_t* StateP, int ConditionId)
{
    switch( ConditionId ) {
    case 1:  return 1; 
    case 2:  return 0; 
    case 3:  return 1; 
    default: assert(0);
    }
}

static void 
my_do_event(hwut_sm_walker_t* me, hwut_sm_state_t* StateP, int EventId)
{
    printf("\nstate[%i].my_do_event %i\n", StateP->id, EventId);
    hwut_sm_walker_print_coverage(stdout, me);
}

static void 
my_do_terminal(hwut_sm_walker_t* me, hwut_sm_state_t* StateP)
{
    printf("\nstate[%i].my_do_terminal\n", StateP->id);
    hwut_sm_walker_print_coverage(stdout, me);
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

    walker->state_db     = &states[0];

    walker->do_init      = (void*)0;
    walker->do_condition = my_do_condition;
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

