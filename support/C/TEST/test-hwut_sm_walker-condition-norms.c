/* State Machine Walker 'hwut_sm_walker'.
 *
 * Checks on the forbidding and allowing on states on the path. That is, 
 * the following API is tested:
 *
 *    hwut_sm_condition_impose(...)
 *    hwut_sm_condition_release(...)
 *    hwut_sm_condition_release_all(...)
 *
 * Use a linear state machine:
 *                                                                  
 *   .-----.             .-----.             .-----.             .-----.
 *   |  0  |-- cond 0 -->|  1  |-- cond 1 -->|  2  |-- cond 2 -->|  3  |
 *   '-----'             '-----'             '-----'             '-----'
 * 
 * A 'hwut_sm_condition_norm_t' can be: -- Must be true
 *                                      -- Must be false
 *                                      -- Can be anything
 *
 * (1) OK tests:
 *
 *   (1a) Set all condition norms to 'true' and let all conditions respond
 *        with 'true'.
 *   (1b) Set all condition norms to 'false' and let all conditions respond
 *        with 'false'.
 *   (1c) Set all condition norms to 'any' and let all conditions respond
 *        with 'false', then let all conditions respond with 'true'.
 *
 *   In all cases the state machine walker is supposed to run until the end.
 *
 * (2) FAIL tests:
 *
 *   (2a) Set condition 1 to true, then respond with false.
 *   (2b) Set condition 1 to false, then respond with false.
 *   (2c) Set condition 2 to true, then respond with false.
 *   (2d) Set condition 2 to false, then respond with false.
 *   (2e) Set condition 3 to true, then respond with false.
 *   (2f) Set condition d to false, then respond with false.
 *
 * (3) Release Tests
 *
 *   Set condition 1 to true, release all, respond with false.
 *   Set condition 1 to false, release all, respond with true.
 *   Set condition 2 to true, release all, respond with false.
 *   Set condition 2 to false, release all, respond with true.
 *   Set condition 3 to true, release all, respond with false.
 *   Set condition 3 to false, release all, respond with true.
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

hwut_sm_transition_t TM_0[] = { { 0, 1, &states[1] } }; 
hwut_sm_transition_t TM_1[] = { { 1, 2, &states[2] } };
hwut_sm_transition_t TM_2[] = { { 2, 3, &states[3] } };

hwut_sm_stack_frame_t  stack_memory[256];

static hwut_sm_state_t  states[4] = {
   { 0, "0", 0, &TM_0[0], &TM_0[1] },
   { 1, "1", 0, &TM_1[0], &TM_1[1] },
   { 2, "2", 0, &TM_2[0], &TM_2[1] },
   { 3, "3", 0, (void*)0, (void*)0, },
};

#include "sm_walker-common.h"

static void my_do_init(hwut_sm_walker_t* me);
static int  my_do_condition(hwut_sm_walker_t* me, hwut_sm_state_t* StateP, int ConditionId);
static void my_do_terminal(hwut_sm_walker_t* me, hwut_sm_state_t* StateP);

static int                       my_do_init_impose_condition_id = 0x5A;
static hwut_sm_condition_norm_t  my_do_init_impose_norm         = HWUT_SM_WALKER_CONDITION_NORM_NONE;

static int  my_do_condition_respond[4] = { 0x5A, 0xA5, 0x5A, 0xA5 };
static void my_do_condition_respond_set(int Index, int Value);



static void my_init(hwut_sm_walker_t* walker);

static void self_check_bad(hwut_sm_walker_t* walker, int ConditionId, hwut_sm_condition_norm_t Norm);
static void self_check_bad2(hwut_sm_walker_t* walker, int ConditionId, hwut_sm_condition_norm_t Norm);


int
main(int argc, char** argv) 
{
    hwut_sm_walker_t  walker;

	hwut_info("State Machine Walker: Condition Norms (positive conditions);\n" 
              "CHOICES: 1, 2a, 2b, 2c, 2d, 2e, 2f, 3a, 3b, 3c, 3d, 3e, 3f;\n")

    my_init(&walker);

    hwut_if_choice("1") {
        printf("(*) Impose 'true' and be 'true'\n");
        my_init(&walker);
        hwut_sm_condition_impose(&walker, 1, HWUT_SM_WALKER_CONDITION_NORM_TRUE, "One   == True");
        hwut_sm_condition_impose(&walker, 2, HWUT_SM_WALKER_CONDITION_NORM_TRUE, "Two   == True");
        hwut_sm_condition_impose(&walker, 3, HWUT_SM_WALKER_CONDITION_NORM_TRUE, "Three == True");
        my_do_condition_respond_set(-1, 1); 
        hwut_sm_walker_walk(&walker, &states[0], 7);

        printf("(*) Impose 'false' and be 'false'\n");
        my_init(&walker);
        hwut_sm_condition_impose(&walker, 1, HWUT_SM_WALKER_CONDITION_NORM_FALSE, "One   == False");
        hwut_sm_condition_impose(&walker, 2, HWUT_SM_WALKER_CONDITION_NORM_FALSE, "Two   == False");
        hwut_sm_condition_impose(&walker, 3, HWUT_SM_WALKER_CONDITION_NORM_FALSE, "Three == False");
        my_do_condition_respond_set(-1, 0); 
        hwut_sm_walker_walk(&walker, &states[0], 7);

        printf("(*) Impose 'any' and be 'true'\n");
        my_init(&walker);
        hwut_sm_condition_impose(&walker, 1, HWUT_SM_WALKER_CONDITION_NORM_NONE, "One   == Any");
        hwut_sm_condition_impose(&walker, 2, HWUT_SM_WALKER_CONDITION_NORM_NONE, "Two   == Any");
        hwut_sm_condition_impose(&walker, 3, HWUT_SM_WALKER_CONDITION_NORM_NONE, "Three == Any");
        my_do_condition_respond_set(-1, 1); 
        hwut_sm_walker_walk(&walker, &states[0], 7);

        printf("(*) Impose 'any' and be 'false'\n");
        my_init(&walker);
        hwut_sm_condition_impose(&walker, 1, HWUT_SM_WALKER_CONDITION_NORM_NONE, "One   == Any");
        hwut_sm_condition_impose(&walker, 2, HWUT_SM_WALKER_CONDITION_NORM_NONE, "Two   == Any");
        hwut_sm_condition_impose(&walker, 3, HWUT_SM_WALKER_CONDITION_NORM_NONE, "Three == Any");
        my_do_condition_respond_set(-1, 0); 
        hwut_sm_walker_walk(&walker, &states[0], 7);
    }
    hwut_if_choice("2a") { self_check_bad(&walker, 1, HWUT_SM_WALKER_CONDITION_NORM_TRUE); }
    hwut_if_choice("2b") { self_check_bad(&walker, 1, HWUT_SM_WALKER_CONDITION_NORM_FALSE); }
    hwut_if_choice("2c") { self_check_bad(&walker, 2, HWUT_SM_WALKER_CONDITION_NORM_TRUE); }
    hwut_if_choice("2d") { self_check_bad(&walker, 2, HWUT_SM_WALKER_CONDITION_NORM_FALSE); }
    hwut_if_choice("2e") { self_check_bad(&walker, 3, HWUT_SM_WALKER_CONDITION_NORM_TRUE); }
    hwut_if_choice("2f") { self_check_bad(&walker, 3, HWUT_SM_WALKER_CONDITION_NORM_FALSE); }

    hwut_if_choice("3a") { self_check_bad2(&walker, 1, HWUT_SM_WALKER_CONDITION_NORM_TRUE); }
    hwut_if_choice("3b") { self_check_bad2(&walker, 1, HWUT_SM_WALKER_CONDITION_NORM_FALSE); }
    hwut_if_choice("3c") { self_check_bad2(&walker, 2, HWUT_SM_WALKER_CONDITION_NORM_TRUE); }
    hwut_if_choice("3d") { self_check_bad2(&walker, 2, HWUT_SM_WALKER_CONDITION_NORM_FALSE); }
    hwut_if_choice("3e") { self_check_bad2(&walker, 3, HWUT_SM_WALKER_CONDITION_NORM_TRUE); }
    hwut_if_choice("3f") { self_check_bad2(&walker, 3, HWUT_SM_WALKER_CONDITION_NORM_FALSE); }
    return 0;
}

static void  
my_do_init(hwut_sm_walker_t* me)
/* CONTROLLED BY: -- 'my_do_init_impose_condition_id' 
 *                -- 'my_do_init_impose_norm'.                               */
{
    if( my_do_init_impose_condition_id == 0x5A ) return;

    hwut_sm_condition_impose(me, 
         my_do_init_impose_condition_id, 
         my_do_init_impose_norm, 
           my_do_init_impose_norm == HWUT_SM_WALKER_CONDITION_NORM_TRUE  ? "must be true"
         : my_do_init_impose_norm == HWUT_SM_WALKER_CONDITION_NORM_FALSE ? "must be false"
         :                                                                 "can be whatsoever");
}

static void  
my_do_init2(hwut_sm_walker_t* me)
/* CONTROLLED BY: -- 'my_do_init_impose_condition_id' 
 *                -- 'my_do_init_impose_norm'.                               */
{
    if( my_do_init_impose_condition_id == 0x5A ) return;

    hwut_sm_condition_impose(me, 
         my_do_init_impose_condition_id, 
         my_do_init_impose_norm, 
           my_do_init_impose_norm == HWUT_SM_WALKER_CONDITION_NORM_TRUE  ? "must be true"
         : my_do_init_impose_norm == HWUT_SM_WALKER_CONDITION_NORM_FALSE ? "must be false"
         :                                                                 "can be whatsoever");
    hwut_sm_condition_release_all(me);
}

static int 
my_do_condition(hwut_sm_walker_t* me, hwut_sm_state_t* StateP, int ConditionId)
{
    printf("state[%i].my_do_condition %i: %x\n", StateP->id, ConditionId, 
           my_do_condition_respond[ConditionId]);
    return my_do_condition_respond[ConditionId];
}

static void 
my_do_terminal(hwut_sm_walker_t* me, hwut_sm_state_t* StateP) 
{
    printf("state[%i].my_do_terminal\n", StateP->id);
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

    walker->do_init      = my_do_init;
    walker->do_condition = my_do_condition;
    walker->do_event     = (void*)0;
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

static void  
my_do_condition_respond_set(int Index, int Value)
{
    int i = 0;
    for(i=0; i<4; ++i) 
    {
        if( Index == -1 || Index == i ) my_do_condition_respond[i] = Value;
    }
}

static void 
self_check_bad(hwut_sm_walker_t*        walker, 
               int                      ConditionId,
               hwut_sm_condition_norm_t Norm)
{
    my_do_init_impose_condition_id = ConditionId; 
    my_do_init_impose_norm         = Norm;

    my_do_condition_respond_set(-1, 1); 
    /* Do the contrary of the norm */
    my_do_condition_respond_set(ConditionId, 
                                Norm == HWUT_SM_WALKER_CONDITION_NORM_TRUE ? 0 : 1); 

    my_do_init(walker);
    hwut_sm_walker_walk(walker, &states[0], 7);
}

static void 
self_check_bad2(hwut_sm_walker_t*        walker, 
                int                      ConditionId,
                hwut_sm_condition_norm_t Norm)
/* Same as 'self_check_bad()', only that the conditions are ALL released after
 * they are set. This happens in 'my_do_init2()'.                            */
{
    my_do_init_impose_condition_id = ConditionId; 
    my_do_init_impose_norm         = Norm;

    my_do_condition_respond_set(-1, HWUT_SM_WALKER_CONDITION_NORM_TRUE); 
    /* Do the contrary of the norm */
    my_do_condition_respond_set(ConditionId, 
                                Norm == HWUT_SM_WALKER_CONDITION_NORM_TRUE ? 0 : 1); 

    walker->do_init = my_do_init2;
    my_do_init2(walker);
    hwut_sm_walker_walk(walker, &states[0], 7);
}
