#ifndef INCLUDE_GUARD_HWUT_SM_WALKER_H
#define INCLUDE_GUARD_HWUT_SM_WALKER_H
/* vim:setlocal ft=c: 
 *
 * Implementation of a state machine walker 'sm-walker'. The state machine
 * walker contains a description of the state machine with all its states,
 * its events and conditions. Based on that, it determines all possible 
 * paths through the state machine.
 *
 * The state machine walker interacts with the user code through three 
 * function callbacks. When a user is called back with these functions
 * he must controll the state machine under test. 
 * 
 * .do_init(me):
 *
 *      when a new path through the state machine starts. The user must
 *      completely re-initialize his state machine. 
 *
 * .do_condition(me, state, condition_id):
 *
 *      transitions may rely on conditions being true. When this callback
 *      is called, he must determine whether the condition given by 
 *      'condition_id' is true. If so, then 1 must returned. If not, then 
 *      0 must be returned.
 *
 * .do_event(me, state, event_id):
 *
 *      when an event occurred. With the 'state' object the user may
 *      verify, that he is in the correct state. The user must do something
 *      to his state machine which related with the provide event_id.
 *
 * .do_terminal(me):
 *
 *      when the end of a path has been reached. If there is something to
 *      be done upon path termination, then this is the place to do it.
 *      It may be used to do some terminating consistency checks.
 *
 * The state machine walker is initialized with the function
 *
 *      hwut_sm_walker_init(...)
 *
 * which sets up the arrays for states and stack frames. Also, it receives
 * the maximum number of loops, i.e. the maximum number of times a state
 * may be passed in a path.
 *
 * The state machine walker starts its work with 
 *
 *      hwut_sm_walker_walk(...)
 *
 * This function does not return before all paths have been walked along. 
 * During the walk, it calls repeatedly 'do_init()', 'do_event()', and 
 * 'do_terminal()' to interact with the user's code.
 *
 * (C) Frank-Rene Schaefer
 *___________________________________________________________________________*/
#include "assert.h"
#include "stddef.h"

struct hwut_sm_state_t_tag;

typedef struct {
    int                          event_id;
    int                          condition_id;
    struct hwut_sm_state_t_tag*  target_state;
} hwut_sm_transition_t;

typedef struct hwut_sm_state_t_tag {
    int                   id;
    const char*           name;    
    int                   pass_n;
    hwut_sm_transition_t* transitions;
    hwut_sm_transition_t* transitions_end;
} hwut_sm_state_t;

void 
hwut_sm_state_init(hwut_sm_state_t* me, const char* Name, 
                   int N, hwut_sm_transition_t* Transitions);

typedef int   hwut_state_coverage_t;
typedef int   hwut_state_forbidden_t;

typedef struct {
    const hwut_sm_transition_t* transition_p;
} hwut_sm_stack_frame_t;

typedef struct { 
    hwut_sm_stack_frame_t* memory;
    hwut_sm_stack_frame_t* memory_end;
    hwut_sm_stack_frame_t* top;
} hwut_sm_stack_t;

typedef struct {
    const char const**  begin;
    const char const**  end;
} hwut_sm_walker_name_db_t;

typedef enum {
    HWUT_SM_WALKER_CONDITION_NEVER = 0x0,
    HWUT_SM_WALKER_CONDITION_TRUE  = 0x1,    /* 'true' has occurred.         */
    HWUT_SM_WALKER_CONDITION_FALSE = 0x2,    /* 'false' has occurred.        */
    HWUT_SM_WALKER_CONDITION_BOTH  = 0x3,    /* 'true' and 'false' occurred. */
} hwut_sm_condition_coverage_t;

typedef enum {
    HWUT_SM_WALKER_CONDITION_NORM_NONE  = 0x0,      /* can be anything.      */
    HWUT_SM_WALKER_CONDITION_NORM_TRUE  = 0x1,      /* must be 'true'.       */
    HWUT_SM_WALKER_CONDITION_NORM_FALSE = 0x2,      /* must be 'false'.      */
} hwut_sm_condition_norm_t;

typedef struct hwut_sm_walker_aux_t_tag { 
    /* Auxiliary data on a state machine:
     *
     *     .condition.coverage[CN]: array to trace condition coverage.
     *     .condition.norm[CN]:     array to store required conditons.
     *     .state.coverage[SN]:     array to trace state coverage.
     *     .state.forbidden[SN]:    array to store forbidden states.
     *
     * CN = number of conditions; SN = number of states. The arrays themselves
     * are provided by generated code in a derived class' memory section. The
     * derived class MUST set the pointers above to the allocated arrays.
     *
     *     .condition_id_db:        dictionary for condition names.
     *     .event_id_db:            dictionary for event names.                       
     *    
     *     .dummy initial transition.
     *_______________________________________________________________________*/
    struct {                                                               
        int offset_id;                                                     
        int number;                                                        
        /* array[i-offset_id] --> information on condition 'i'.               */    
        hwut_sm_condition_coverage_t* coverage;         /* size = number      */
        hwut_sm_condition_norm_t*     norm;             /* size = number      */
        const char**                  norm_comment;     /* size = number      */
    } condition;

    struct { 
        int              offset_id;
        int              number;

        /* array[i-offset_id] --> information on state 'i'.                   */    
        int*             coverage;                      /* size = number      */
        int*             forbidden;                     /* size = number      */
        const char**     forbidden_comment;             /* size = number      */
    } state;

    hwut_sm_walker_name_db_t  event_id_db;
    hwut_sm_walker_name_db_t  condition_id_db;

    hwut_sm_transition_t      dummy_init_transition;

} hwut_sm_walker_aux_t;

typedef struct hwut_sm_walker_t_tag {
    /* State machine walker. 
     * 
     * Detailed description can be reviewed at entry of this file.
     *_______________________________________________________________________*/
    hwut_sm_stack_t       stack;
    hwut_sm_state_t*      state_db;
    hwut_sm_walker_aux_t  aux;

    void   (*do_init)(struct hwut_sm_walker_t_tag* me);
    int    (*do_condition)(struct hwut_sm_walker_t_tag* me, hwut_sm_state_t* state_p, int ConditionId);
    void   (*do_event)(struct hwut_sm_walker_t_tag* me, hwut_sm_state_t* state_p, int EventId);
    void   (*do_terminal)(struct hwut_sm_walker_t_tag* me, hwut_sm_state_t* state_p);

} hwut_sm_walker_t;

void hwut_sm_walker_init(hwut_sm_walker_t*       me, 
                         int                     StackSize,
                         hwut_sm_stack_frame_t*  StackMemory); 
void hwut_sm_walker_aux_init(hwut_sm_walker_aux_t*         me, 
                             ptrdiff_t StateID_Offset,     size_t StateN,
                             hwut_state_coverage_t*        memory_state_coverage,                  
                             hwut_state_forbidden_t*       memory_state_forbidden,                
                             const char**                  memory_state_forbidden_comment,       
                             ptrdiff_t ConditionID_Offset, size_t ConditionN,
                             hwut_sm_condition_coverage_t* memory_condition_coverage,      
                             hwut_sm_condition_norm_t*     memory_condition_norm,          
                             const char**                  memory_condition_norm_comment, 
                             size_t                        EventIdDb_Size,
                             const char**                  EventIdDb, 
                             size_t                        ConditionIdDb_Size,
                             const char**                  ConditionIdDb);

void hwut_sm_walker_walk(hwut_sm_walker_t* me, 
                         hwut_sm_state_t*  init_state, 
                         const int         MaxLoopN);

int  hwut_sm_state_forbid(hwut_sm_walker_t* me, 
                          int               StateId, 
                          const char*       Comment);
int  hwut_sm_state_allow(hwut_sm_walker_t* me, 
                         int               StateId);
int  hwut_sm_state_allow_all(hwut_sm_walker_t* me);
int  hwut_sm_state_happened(hwut_sm_walker_t* me, int StateId);

hwut_sm_condition_norm_t   
     hwut_sm_condition_impose(hwut_sm_walker_t*        me, 
                              int                      ConditionId, 
                              hwut_sm_condition_norm_t Norm, 
                              const char*              Comment);
int  hwut_sm_condition_release(hwut_sm_walker_t* me, 
                               int               ConditionId);
int  hwut_sm_condition_release_all(hwut_sm_walker_t*);


#if ! defined(HWUT_OPTION_STDIO_FORBIDDEN)

#include "stdio.h"
void hwut_sm_walker_print(FILE* fh, hwut_sm_walker_t* me, int LineWidth);
void hwut_sm_walker_print_plain(FILE* fh, hwut_sm_walker_t* me);
void hwut_sm_walker_print_coverage(FILE*, hwut_sm_walker_t* me); 
void hwut_sm_walker_print_coverage_state(FILE*, hwut_sm_walker_t* me);
void hwut_sm_walker_print_coverage_condition(FILE*, hwut_sm_walker_t* me); 
#endif

#endif /* INCLUDE_GUARD_HWUT_SM_WALKER_H */
