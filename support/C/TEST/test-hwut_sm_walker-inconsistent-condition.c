/* State Machine Walker 'hwut_sm_walker'.
 *
 * When the state machine walker branches from a certain node, it goes back
 * to the beginning of the state machine and walks the same path again. If 
 * the state machine behaves consistently, then the conditions must be the same
 * as they were when walking along the path. 
 *
 * This function checks whether inconsistent condition responses are detected.
 *
 * Setup: 
 *                                                      .-----. 
 *                                          ,---  E0 ---|  3  | 
 *   .-----.          .-----.          .-----.          '-----'
 *   |  0  |--- C0 ---|  1  |--- C1 ---|  2  |
 *   '-----'          '-----'          '-----'          .-----.
 *                                          '---  E1 ---|  4  |
 *                                                      '-----'
 *
 * The fork at the end forces the state machine walker to re-run on the states
 * 0 to 2. On that way two conditions are checked. 
 * 
 * CHOICES: possitive-* -- all conditions are 'possitive'.
 *          negative-*  -- all conditions are 'not'.
 *
 * where * is 1 means that the first condition behaves inconsistently.
 *       * is 2 means that the second does so.
 *
 * (C) Frank-Rene Schaefer
 *___________________________________________________________________________*/
#include "hwut_unit.h"
#include "hwut_sm_walker.h"

#include "stdio.h"
#include "stdarg.h"
#include "assert.h"

hwut_sm_state_t  states[5];
/* states[0] -- Init State 
 * states[1] -- Terminal
 * states[2] -- Prehistoric (state before init in 'X-*' CHOICES.             */

/* Transition from 'Prehistoric' to 'Init'                                   */
hwut_sm_transition_t TM_0[] = {
   /* Transitions, that DO NOT rely on a 'user condition.'                   */
   { 0, 1, &states[1] }
};

/* Transition from 'Terminal' to 'Posthistoric'                              */
hwut_sm_transition_t TM_1[] = {
   /* Transitions, that DO NOT rely on a 'user condition.'                   */
   { 0, 2, &states[2] }
};

/* Transitions from 'Init' to 'Terminal'                                     */
hwut_sm_transition_t TM_2[] = {
   /* Transitions, that DO NOT rely on a 'user condition.'                   */
   { 1, 0, &states[3] },
   { 2, 0, &states[4] },
};

hwut_sm_stack_frame_t  stack_memory[256];

#include "sm_walker-common.h"

int condition_return[3] = { 
    1, /* unimportant */
    0, /* return value for 'ConditionId == 1' */
    0, /* return value for 'ConditionId == 2' */
};

int switch_condition_id = -1;

static int 
do_my_condition(hwut_sm_walker_t* me, hwut_sm_state_t* StateP, int ConditionId) 
{ 
    printf("Condition: %i: %i;\n", ConditionId, condition_return[ConditionId]);
    return condition_return[ConditionId];
}

static void 
do_my_terminal(hwut_sm_walker_t* me, hwut_sm_state_t* state) 
{
    condition_return[switch_condition_id] = ! condition_return[switch_condition_id];
    printf("\n");
}

int
main(int argc, char** argv) 
{
    hwut_sm_walker_t  walker;
    const char*       condition_id_db[3] = { "none", "first", "second" };

	hwut_info("State Machine Walker: Detect inconsistent conditions;\n" 
              "CHOICES: pos-1, pos-2, neg-1, neg-2;");

    hwut_sm_walker_init(&walker, 
                        /* stack size   */ 256, 
                        /* stack memory */ stack_memory); 
    common_setup(&walker);

    hwut_sm_state_init(&states[0], "0", 1, TM_0); 
    hwut_sm_state_init(&states[1], "1", 1, TM_1); 
    hwut_sm_state_init(&states[2], "2", 2, TM_2); 
    hwut_sm_state_init(&states[3], "3", 0, (void*)0); 
    hwut_sm_state_init(&states[4], "4", 0, (void*)0); 

    hwut_if_choice("pos-1") {
        condition_return[1] = 1; 
        condition_return[2] = 1; 
        switch_condition_id = 1;
    }
    hwut_if_choice("pos-2") {
        condition_return[1] = 1; 
        condition_return[2] = 1; 
        switch_condition_id = 2;
    }
    hwut_if_choice("neg-1") {
        condition_return[1] = 0; 
        condition_return[2] = 0; 
        switch_condition_id = 1;
        TM_0[0].condition_id = - TM_0[0].condition_id;
        TM_1[0].condition_id = - TM_1[0].condition_id;
    }
    hwut_if_choice("neg-2") {
        condition_return[1] = 0; 
        condition_return[2] = 0; 
        switch_condition_id = 2;
        TM_0[0].condition_id = - TM_0[0].condition_id;
        TM_1[0].condition_id = - TM_1[0].condition_id;
    }

    walker.do_event     = (void*)0;
    walker.do_condition = do_my_condition;
    walker.do_terminal  = do_my_terminal;
    walker.aux.condition_id_db.begin = &condition_id_db[0];

    hwut_sm_walker_walk(&walker, &states[0], 7);

    return 0;
}
