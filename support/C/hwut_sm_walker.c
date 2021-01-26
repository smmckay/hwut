#include <hwut_sm_walker.h>
#include <hwut_unit.h>
static void                               self_walk_path_again(hwut_sm_walker_t* me);
static const hwut_sm_transition_t*        self_get_next_transition(hwut_sm_walker_t* me); 

static void  self_aux_reset(hwut_sm_walker_aux_t* me);
static int   self_aux_state_register(hwut_sm_walker_aux_t*   me, 
                                     const hwut_sm_state_t*  StateP);
static int   self_aux_condition_register(hwut_sm_walker_aux_t* me, 
                                         int                   ConditionId, 
                                         int                   Value);

static void  self_call_do_init(hwut_sm_walker_t* me); 
static void  self_call_do_event(hwut_sm_walker_t* me, int EventId);
static int   self_call_do_condition(hwut_sm_walker_t* me, int ConditionId);
static void  self_call_do_terminal(hwut_sm_walker_t* me);

static int   self_max_number_of_passes(hwut_sm_stack_t*            me, 
                                       const hwut_sm_transition_t* transition_p, 
                                       int                         MaxLoopN);

static void  self_condition_double_check(hwut_sm_walker_t* me, 
                                         int               ConditionId);

static void             self_stack_init(hwut_sm_walker_t* me, 
                                        hwut_sm_state_t*  init_state);
static void             self_stack_push(hwut_sm_walker_t*       me, 
                                        const hwut_sm_state_t*  state_p); 
static int              self_stack_pop_done_frames(hwut_sm_stack_t* me);
static hwut_sm_state_t* self_stack_current_state(hwut_sm_stack_t* me);

static void             self_on_bad_state(hwut_sm_walker_t* me, const hwut_sm_state_t* StateP);
static void             self_on_bad_condition(hwut_sm_walker_t* me, int ConditionId, int Value);

void
hwut_sm_walker_init(hwut_sm_walker_t*       me, 
                    int                     StackSize,
                    hwut_sm_stack_frame_t*  StackMemory) 
/* Initialize the state machine walker:
 *
 * -- Set the user's data. This data can then be referred to in the callbacks.
 * -- Define the initial state from which any event path shall begin. 
 * -- Define the stack and its size. This defines at the same time the maximum
 *    path length.
 * -- Specify the maximum number of times a single state can be passed in a
 *    single path. This limits the number of loops that can be made.         */
{
    me->stack.memory     = StackMemory;
    me->stack.memory_end = StackMemory + StackSize;
    me->stack.top        = StackMemory;

    /* By default, all callbacks are disabled.                               */
    me->do_init      = (void*)0;
    me->do_event     = (void*)0;
    me->do_condition = (void*)0;
    me->do_terminal  = (void*)0;

    /* Derived class must set the 'aux' element. Implicitly, here: 
     *        
     *         me->aux.state.number = me->aux.condition.number = 0 
     *        
     * Which makes it safe to call 'self_aux_reset()', event if the derived
     * class missed to initialize the '.aux' member.                         */
    memset((void*)&me->aux, 0, sizeof(me->aux));
    me->state_db = (void*)0; 
}

void
hwut_sm_walker_aux_init(hwut_sm_walker_aux_t*         me, 
                        ptrdiff_t                     StateID_Offset,
                        size_t                        StateN,
                        hwut_state_coverage_t*        memory_state_coverage,                  
                        hwut_state_forbidden_t*       memory_state_forbidden,                
                        const char**                  memory_state_forbidden_comment,       
                        ptrdiff_t                     ConditionID_Offset,
                        size_t                        ConditionN,
                        hwut_sm_condition_coverage_t* memory_condition_coverage,      
                        hwut_sm_condition_norm_t*     memory_condition_norm,          
                        const char**                  memory_condition_norm_comment, 
                        size_t                        EventIdDb_Size,
                        const char**                  EventIdDb, 
                        size_t                        ConditionIdDb_Size,
                        const char**                  ConditionIdDb)
{
    ptrdiff_t i = 0;

    me->state.offset_id = StateID_Offset;
    me->state.number    = StateN;

    me->state.coverage          = memory_state_coverage;
    me->state.forbidden         = memory_state_forbidden;
    me->state.forbidden_comment = memory_state_forbidden_comment;

    me->condition.offset_id = ConditionID_Offset;
    me->condition.number    = ConditionN;

    me->condition.coverage      = memory_condition_coverage;
    me->condition.norm          = memory_condition_norm;
    me->condition.norm_comment  = memory_condition_norm_comment;

    /* Conditions: never, true happened, false happened, both happened.      
     * (Cannot use 'memset' here, because this would be bytewise).           */
    for(i=0; i != ConditionN ; ++i) {
        me->condition.coverage[i] = HWUT_SM_WALKER_CONDITION_NEVER;
    } 

    /* States: 0 -- state has been passed, 1 -- state was never passed.      */
    memset(me->state.coverage, 0, 
           me->state.number * sizeof(hwut_state_coverage_t));

    me->event_id_db.begin     = EventIdDb;
    me->event_id_db.end       = EventIdDb + EventIdDb_Size;
    me->condition_id_db.begin = ConditionIdDb;
    me->condition_id_db.end   = ConditionIdDb + ConditionIdDb_Size;

    /* The coverage data is NOT reset in 'self_aux_reset()' since it must 
     * collect data over all walks. It is ONLY reset upon experiment start.  */
    self_aux_reset(me);
}
        

void
hwut_sm_walker_walk(hwut_sm_walker_t* me, 
                    hwut_sm_state_t*  init_state, 
                    const int         MaxLoopN)
/* Walk paths until an end is reached, then send the events as they are stored
 * in the state-stack to the state machine.                                  */
{
    const hwut_sm_transition_t*   transition_p = (void*)0;
    int                           new_branch_f = 0; 

    self_stack_init(me, init_state); 
    self_walk_path_again(me);

    while( 1 + 1 == 2 ) {
        transition_p = self_get_next_transition(me);
        if( transition_p == (void*)0 ) {
            self_call_do_terminal(me);
            if( ! self_stack_pop_done_frames(&me->stack) ) {
                return;
            }
            new_branch_f = 1;
            continue;
        }
        if( new_branch_f ) {
            self_aux_reset(&me->aux);
            self_walk_path_again(me);
            new_branch_f = 0;
        }
        assert(transition_p->target_state != (void*)0);

        if( ! self_call_do_condition(me, transition_p->condition_id) ) {
            continue;
        }

        self_call_do_event(me, transition_p->event_id);

        self_stack_push(me, transition_p->target_state);

        /* Has target state been reached the same time too often?            */
        if( self_max_number_of_passes(&me->stack, transition_p, MaxLoopN) ) {
            me->stack.top->transition_p = self_stack_current_state(&me->stack)->transitions_end - 1;
        }
        /* 'me->stack.top->transitions_p' points to the next transitions.    */
    } 
}

static const hwut_sm_transition_t*
self_get_next_transition(hwut_sm_walker_t* me)
/* A transition on an event may be related to multiple conditions. However, 
 * only one target state can be entered upon the event. So, this function
 * first determines which of the relevant conditions are met. If there is 
 * more than one condition which is met, this is an error: ambiguity!
 *
 * This function iterates over all conditions for a given event in a given
 * state. 
 *  
 * RETURNS:
 *
 * Pointer to transition -- If a single transition can be identified.
 * (void*)0              -- If no condition is met.
 * 
 * If 'ambiguity' is detected, the 'on_ambiguous_transition' callback is called. 
 *                                                                           */ 
{
    hwut_sm_stack_frame_t*  top = me->stack.top;

    if( me->stack.top == me->stack.memory_end - 1 ) {
        return (void*)0;
    }
    else if( top->transition_p == self_stack_current_state(&me->stack)->transitions_end - 1 ) {
        return (void*)0;
    }
    else {
        assert(top->transition_p >= &(self_stack_current_state(&me->stack)->transitions[-1]));
        assert(top->transition_p <    self_stack_current_state(&me->stack)->transitions_end - 1);
        return ++(top->transition_p);
    }
}

static void
self_stack_init(hwut_sm_walker_t*  walker, hwut_sm_state_t* init_state)
/* Initialize the stack:
 *
 *  -- stack.top         = begin of stack.
 *  -- stack.top.state_p = intitial state.
 *              .transition_p = first transition of init state.                   */
{
    hwut_sm_stack_t*  me = &walker->stack;

    assert(me->memory_end - &me->memory[0] >= 2);

    walker->aux.dummy_init_transition.target_state = init_state;
    walker->aux.dummy_init_transition.condition_id = 0;
    walker->aux.dummy_init_transition.event_id     = 0;

    me->top = &me->memory[0];
    me->top->transition_p = &walker->aux.dummy_init_transition;
    ++(me->top);
    me->top->transition_p = &self_stack_current_state(me)->transitions[-1];

    if( ! self_aux_state_register(&walker->aux, init_state) ) {
        self_on_bad_state(walker, init_state);
    }
}

static void
self_stack_push(hwut_sm_walker_t*      me, 
                const hwut_sm_state_t* state_p) 
/* Generate new frame on the stack for the given state. Frame contains the
 * 'next_state' and the 'transition_p' set to the first transition.               */
{
    hwut_sm_stack_t*  stack = &me->stack;
    assert(stack->top->transition_p->target_state == state_p);

    ++(stack->top);

    /* 'self_get_next_transition()' will increment 'transition_p', so initialize
     * it to the position right before the first.                                */
    stack->top->transition_p = &state_p->transitions[-1];
    assert(self_stack_current_state(&me->stack) != (void*)0);

    ++(self_stack_current_state(stack)->pass_n);

    if( ! self_aux_state_register(&me->aux, state_p) ) {
        self_on_bad_state(me, state_p);
    }
}

static int
self_stack_pop_done_frames(hwut_sm_stack_t* me)
/* Close all frames on the stack wherer there is no more to do. 'No more to do'
 * means that all transitions are considered. When, after popping, a frame is 
 * found which does still contain unconsidered transitions, then the function 
 * stops.
 *
 * RETURNS: 1 -- if there is still stuff to do. 'stack->top' contains the 
 *               frame of concern.
 *          0 -- absolutely nothing left to be done.                         
 *
 * For nesting frames, 'transition_p' has already been considered, when diving
 * further into the tree. So, one must required that 'transition_p + 1' is 
 * something to consider. Otherwise, the frame needs to be closed.           */
{
    do {
        if( me->top == &me->memory[1] ) {
            return 0;
        }
        --(self_stack_current_state(me)->pass_n);
        me->top->transition_p = (void*)0; /* violation => segm. fault       */
        --(me->top);
    } while( me->top->transition_p == self_stack_current_state(me)->transitions_end - 1 );

    return 1;
}

static hwut_sm_state_t* 
self_stack_current_state(hwut_sm_stack_t* me)
/* top[-1].transition_p --> transition that guided to state '0'.             */
{
    return me->top[-1].transition_p->target_state;
}

void
hwut_sm_state_init(hwut_sm_state_t* me, const char* Name, 
                   int N, hwut_sm_transition_t* Transitions)
{
    me->name            = Name;
    me->transitions     = Transitions;
    me->transitions_end = Transitions + N;
}

static int  
self_max_number_of_passes(hwut_sm_stack_t*            me, 
                          const hwut_sm_transition_t* transition_p, 
                          int                         MaxLoopN)
/* Checks the number of passes through 'transition_p->target_state'. For that
 * it counts the number of times that the state has been entered through the
 * same transition. 
 * 
 * RETURNS: 0 -- if the max. number of passes throug the target state
 *               has not yet been reached.
 *          1 -- max. number of passes has been reached.                     */
{
    hwut_sm_stack_frame_t*        it  = (void*)0;
    const hwut_sm_stack_frame_t*  End = &me->top[-1];
    int                           n   = 0;
    
    /* memory[0] is a dummy transition containing only the init state.       */
    assert(me->top != &me->memory[0]);
    /* the state has been entered, thus pass_n == 0 is impossible.           */
    assert(transition_p->target_state->pass_n != 0);

    if( transition_p->target_state->pass_n == 1 ) {
        return 0;
    }

    for(it = &me->memory[1]; it != End ; ++it) {
        /* A transition_p belongs to a 'from state'. It is 1:1 associated with
         * a condition and an event and a 'to state'.
         * => If the transition_p is the same, it means, that exactly the same
         *    transition has been done before.                               */
        if( transition_p != it->transition_p ) { 
            continue;
        }
        else if( ++n == MaxLoopN ) {
            return 1;
        }
    }

    /* Max number of passes has not been reached.                            */
    return 0;
}

static int
self_call_do_condition(hwut_sm_walker_t* me, int ConditionId)
/* Calls 'me->do_condition' if it is defined. The callback tells whether the 
 * condition for the current transition is met or not. 
 * 
 * RETURNS: 1 -- Transition of 'me->stack.top->transition_p' can be performed.
 *          0 -- Condition for the transition has not been met.              */
{
    int abs_condition_id = ConditionId < 0 ? - ConditionId : ConditionId;
    int result           = 0;

    if( me->do_condition == (void*)0 ) {
        /* User does not tell, so assume the condition is met.              
         * For X == true, it must be X == true.                    
         * For not X == true, it must be X == false.                        */
        result = (int)(ConditionId >= 0);
    }
    else {
        /* ConditionId == 0 --> Always Ok. But still call the user's 
         *                      condition. This way the user can break-up  
         *                      diving further.                              */
        result = me->do_condition(me, self_stack_current_state(&me->stack), 
                                  abs_condition_id);
    }
    if( ! self_aux_condition_register(&me->aux, abs_condition_id, result) ) {
        self_on_bad_condition(me, abs_condition_id, result);
    }

    /* ConditionId < 0  --> not abs(ConditionId)                             */
    return ConditionId < 0 ? (0 == result) : result;
}

static void
self_call_do_event(hwut_sm_walker_t* me, int EventId)
/* Calls 'me->do_event' if it is defined.                                    */
{
    if( me->do_event != (void*)0 ) {
        me->do_event(me, self_stack_current_state(&me->stack), EventId);
    }
}

static void
self_walk_path_again(hwut_sm_walker_t* me)
/* Run through the transitions mentioned in the stack again. This happens, 
 * when one branch has been walked to the end and another branch is to be
 * considered.                                                               */
{
    hwut_sm_stack_frame_t* it         = (void*)0;
    hwut_sm_stack_frame_t* backup_top = (void*)me->stack.top;

    /* Ensure, that the path is properly setup in 'do_init', 'do_condition' 
     * and 'do_event'. That is 'stack.top' must point to current place.      */
    it = &(me->stack.memory[1]);
    me->stack.top = it;

    self_call_do_init(me);

    /* Do not send the event of the last frame, because this is to be called 
     * as selected by 'self_get_transition()'.                               */
    for(; it != backup_top; ++it) {
        assert(it->transition_p >= &(it[-1].transition_p->target_state->transitions[0]));
        assert(it->transition_p <    it[-1].transition_p->target_state->transitions_end);

        /* The 'stack' or path's top needs to be adapted, so that the correct
         * path is reflected. In 'hwut_sm_walker_print()', for example, the 
         * printed path would differ otherwise.                             */
        me->stack.top = it;
        self_condition_double_check(me, it->transition_p->condition_id);
        self_call_do_event(me, it->transition_p->event_id);
    }
    me->stack.top = backup_top;
}

static void
self_call_do_init(hwut_sm_walker_t* me) 
/* Calls 'me->do_init' if it is defined.                                    */
{
    if( me->do_init != (void*)0 ) {
        me->do_init(me);
    }
}

static void
self_call_do_terminal(hwut_sm_walker_t* me) 
/* Calls 'me->do_terminal' if it is defined.                                 */
{
    if( me->do_terminal != (void*)0 ) {
        me->do_terminal(me, self_stack_current_state(&me->stack));
    }
}

static void
self_aux_reset(hwut_sm_walker_aux_t* me)
{
    ptrdiff_t i = 0;

    /* Cannot use 'memset()', because this would be bytewise.                */
    for(i=0; i < me->condition.number; ++i) {
        me->condition.norm[i] = HWUT_SM_WALKER_CONDITION_NORM_NONE;
    }
    memset(me->condition.norm_comment, 0, 
           me->condition.number * sizeof(const char*));
    memset(me->state.forbidden, 0, 
           me->state.number * sizeof(hwut_state_forbidden_t));
    memset(me->state.forbidden_comment, 0, 
           me->state.number * sizeof(const char*));
}

int  
hwut_sm_state_forbid(hwut_sm_walker_t* me, 
                     int               StateId, 
                     const char*       Comment)
/* Forbids the state given by 'StateId' from further occurrence on the current
 * path. If it occurrs while being forbidden, the 'Comment' is printed in 
 * addition to the standard error message. 
 *
 * RETURNS: 1 -- if the state was forbidden before. 
 *          0 -- if not.                                                     */
{
    const int NormSi   = StateId - me->aux.state.offset_id;
    const int Previous = me->aux.state.forbidden[NormSi];

    assert(NormSi >= 0 && NormSi < me->aux.state.number);

    me->aux.state.forbidden[NormSi] = 1;
    if( Comment != (void*)0 ) {
        me->aux.state.forbidden_comment[NormSi] = Comment;
    }
    return Previous;
}

int  
hwut_sm_state_allow(hwut_sm_walker_t* me, 
                    int               StateId)
/* Allows the state given by 'StateId' for further on the current path.
 *
 * RETURNS: 1 -- if the state was forbidden before. 
 *          0 -- if not.                                                     */
{
    const int NormSi   = StateId - me->aux.state.offset_id;
    const int Previous = me->aux.state.forbidden[NormSi];

    assert(NormSi >= 0 && NormSi < me->aux.state.number);

    me->aux.state.forbidden[NormSi]         = 0;
    me->aux.state.forbidden_comment[NormSi] = (void*)0;
    return Previous;
}

int  
hwut_sm_state_allow_all(hwut_sm_walker_t* me)
/* Allow all states to occur on the current path. 
 * 
 * RETURNS: N -- the number of states that were forbidden.                   */
{
    int i   = 0;
    int sum = 0;

    for(i=0; i != me->aux.state.number; ++i) {
        if( me->aux.state.forbidden[i] ) {
            sum += 1;
        }
        me->aux.state.forbidden[i]         = 0;
        me->aux.state.forbidden_comment[i] = (void*)0;
    }
    return sum;
}

int  
hwut_sm_state_happened(hwut_sm_walker_t* me, int StateId)
/* RETURNS: 1 -- if the state given by 'StateId' appeared on the path before.
 *          0 -- if the state did not occurr yet on the current path.        */
   
{
    hwut_sm_stack_frame_t* p = (void*)0;

    for(p = &me->stack.memory[0]; p != &me->stack.top[-1]; ++p) {
        if( p->transition_p->target_state->id == StateId ) {
            return 1;
        }
    }
    return 0;
}

hwut_sm_condition_norm_t  
hwut_sm_condition_impose(hwut_sm_walker_t*        me, 
                         int                      ConditionId, 
                         hwut_sm_condition_norm_t Norm, 
                         const char*              Comment)
/* Imposes the 'Norm' as required for the condition given by 'ConditionId'.
 * That is, whenever the condition appears it must follow the given norm.
 * A norm can be one of:
 *
 *       HWUT_SM_WALKER_CONDITION_NORM_NONE, i.e. can be anything.      
 *       HWUT_SM_WALKER_CONDITION_NORM_TRUE, i.e. must be 'true'.     
 *       HWUT_SM_WALKER_CONDITION_NORM_FALSE, i.e. must be 'false'.    
 *
 * RETURNS: The previous condition norm.                                     */
{
    ptrdiff_t                      NormCi   = ConditionId == 0 ? 0 : ConditionId - me->aux.condition.offset_id;
    const hwut_sm_condition_norm_t Previous = me->aux.condition.norm[NormCi];

    assert(NormCi >= 0 && NormCi < me->aux.condition.number);

    me->aux.condition.norm[NormCi] = Norm;
    if( Comment != (void*)0 ) {
        me->aux.condition.norm_comment[NormCi] = Comment;
    }
    return Previous;
}

int  
hwut_sm_condition_release(hwut_sm_walker_t* me, 
                          int               ConditionId)
/* Releases any norm currently imposed on the given condition. 
 *
 * RETURNS: The previous condition norm.                                     */
{
    return hwut_sm_condition_impose(me, ConditionId, 
                                    HWUT_SM_WALKER_CONDITION_NORM_NONE, 
                                    (void*)0);
}

int  
hwut_sm_condition_release_all(hwut_sm_walker_t* me)
/* Releases all condition norms set for any condition. 
 *
 * RETURNS: Number of norms (not NONE) which were imposed before.            */
{
    int i   = 0;
    int sum = 0;

    for(i=0; i != me->aux.condition.number; ++i) {
        if( me->aux.condition.norm[i] ) {
            sum += 1;
        }
        me->aux.condition.norm[i]         = HWUT_SM_WALKER_CONDITION_NORM_NONE;
        me->aux.condition.norm_comment[i] = (void*)0;
    }
    return sum;
}

static int
self_aux_state_register(hwut_sm_walker_aux_t*  me, 
                        const hwut_sm_state_t* StateP) 
/* RETURNS: 1 -- if the state is OK
 *          0 -- if the state is not supposed to happen.                     */
{
    int NormSi = StateP->id - me->state.offset_id;

    assert(NormSi >= 0 && NormSi < me->state.number);

    /* Mark the state as being passed.                                       */
    me->state.coverage[NormSi] = 1;
    
    /* Check admissibility.                                                  */
    return me->state.forbidden[NormSi] == 0;
}

static int
self_aux_condition_register(hwut_sm_walker_aux_t* me, 
                            int                   ConditionId, 
                            int                   Value) 
/* RETURNS: 1 -- if the condition is OK
 *          0 -- if the condition is not supposed to happen.                 */
{
    int NormCi = ConditionId == 0 ? 0 : ConditionId - me->condition.offset_id;

    assert(NormCi >= 0 && NormCi < me->condition.number);

    /* Mark the condition as being occurred.                                 */
    if( Value ) {
        me->condition.coverage[NormCi] |= HWUT_SM_WALKER_CONDITION_TRUE; 
    } 
    else { 
        me->condition.coverage[NormCi] |= HWUT_SM_WALKER_CONDITION_FALSE; 
    }
    
    /* Check admissibility.                                                  */
    switch( me->condition.norm[NormCi] ) {
    case HWUT_SM_WALKER_CONDITION_NORM_NONE:  return 1;
    case HWUT_SM_WALKER_CONDITION_NORM_TRUE:  return 1 == Value; 
    case HWUT_SM_WALKER_CONDITION_NORM_FALSE: return 0 == Value; 
    default:                                  return 1;
    }
}

#if ! defined(HWUT_OPTION_STDIO_FORBIDDEN)
#include <string.h>

static int
self_print_newline(FILE* fh, int column_i)
{
    fprintf(fh, ".\n .");
    for(column_i -= 2; column_i > 0; --column_i) {
        fprintf(fh, "-");
    }
    fprintf(fh, "'\n");
    return column_i;
}

static int
self_print_newline_maybe(FILE* fh, int column_i, int ToBeAdded, int LineWidth)
{
    if( column_i + ToBeAdded > LineWidth) {
        return self_print_newline(fh, column_i);
    }
    return column_i;
}

static int
self_print_append_state(FILE* fh, int column_i, int LineWidth, const char* Name)
{
    int length = strlen(Name) + 7;
    column_i = self_print_newline_maybe(fh, column_i, length, LineWidth);
    fprintf(fh, " %s -->--", Name);
    return column_i + length;
}

static int
self_print_append_name(FILE* fh, int column_i, int LineWidth,
                       hwut_sm_walker_name_db_t* name_db, 
                       int                       Index, 
                       char*                     brackets)
{
    int         length = 0;
    int         abs_index = Index >= 0 ? Index : - Index;
    const char* not_str   = Index >= 0 ? ""    : "not ";

    assert(name_db->begin != (void*)0);

    length   = strlen(name_db->begin[abs_index]);
    column_i = self_print_newline_maybe(fh, column_i, length + 6, LineWidth);
    fprintf(fh, "%c %s%s %c--", brackets[0], not_str, name_db->begin[abs_index], brackets[1]);

    return column_i + length + (Index >= 0 ? 6 : 10);
}


void
hwut_sm_walker_print(FILE* fh, hwut_sm_walker_t* me, int LineWidth)
/* Prints the current path of the state machine walker. The print-out is 
 * limitted to the given line width.                                         */
{
    int                    column_i = 0;
    hwut_sm_stack_frame_t* it       = (void*)0;

    /* memory[0] is a dummy frame containing the init state.                 */
    assert(me->stack.top                 != &me->stack.memory[0]);
    assert(me->aux.condition_id_db.begin != (void*)0);
    assert(me->aux.event_id_db.begin     != (void*)0);

    fprintf(fh, "[[BEGIN]]--.\n");
    fprintf(fh, " .---------'\n");

    /* Do not send the event of the last frame, because this is to be called 
     * as selected by 'self_get_transition()'.                               */
    for(it = &(me->stack.memory[1]); it != me->stack.top; ++it) {
        column_i = self_print_append_state(fh, column_i, LineWidth, 
                                           it[-1].transition_p->target_state->name);
        if( it->transition_p->condition_id != 0 ) {
            column_i = self_print_append_name(fh, column_i, LineWidth, 
                                              &me->aux.condition_id_db, 
                                              it->transition_p->condition_id, "||");
        }
        if( it->transition_p->event_id != 0 ) {
            column_i = self_print_append_name(fh, column_i, LineWidth, 
                                              &me->aux.event_id_db, 
                                              it->transition_p->event_id, "()");
        }
    }
    self_print_newline(fh, column_i);
    fprintf(fh, " %s\n", it[-1].transition_p->target_state->name);
}

void
hwut_sm_walker_print_plain(FILE* fh, hwut_sm_walker_t* me)
{
    hwut_sm_stack_frame_t* it = (void*)0;
    int                    x = 0;

    for(it = &(me->stack.memory[1]); it != me->stack.top; ++it) {
        fprintf(fh, "S:%s;", it[-1].transition_p->target_state->name);
        if( it->transition_p->condition_id != 0 ) {
            x = it->transition_p->condition_id;
            fprintf(fh, "C:%s%s;", 
                    x < 0 ? "not " : "",
                    me->aux.condition_id_db.begin[x >= 0 ? x : -x]);
        }
        if( it->transition_p->event_id != 0 ) {
            fprintf(fh, "E:%s;", 
                    me->aux.event_id_db.begin[it->transition_p->event_id]);
        }
    }
    fprintf(fh, "S:%s;\n", it[-1].transition_p->target_state->name);
}

static const char*
self_get_state_name(hwut_sm_walker_t* me, int InternStateIndex)
{
    ptrdiff_t offset_id = me->aux.state.offset_id; 

    if(    me->state_db != (void*)0 
        && me->state_db[offset_id + InternStateIndex].name != (void*)0 ) {
        return me->state_db[offset_id + InternStateIndex].name;
    }
    else {
        return "<no name>";
    }
}

static const char*
self_get_condition_name(hwut_sm_walker_t* me, int InternConditionIndex)
{
    ptrdiff_t offset_id = me->aux.condition.offset_id;

    if(    me->state_db != (void*)0 
        && me->aux.condition_id_db.begin[offset_id + InternConditionIndex] != (void*)0 ) {
        return me->aux.condition_id_db.begin[offset_id + InternConditionIndex]; 
    }
    else {
        return "<no name>";
    }
}

static void 
self_print_space(const char* name, const int MaxL)
{
    int k = 0;
    for(k=strlen(name); k < MaxL; ++k) {
        printf(".");
    }
}

void 
hwut_sm_walker_print_coverage_state(FILE* fh, hwut_sm_walker_t* me)
/* Prints information about states which have never been passed during
 * the experiments. 
 * 
 * ASSUMES: '.state_db' must have been set by the derived class.             */
{
    int         i          = 0; 
    int         length     = 0; 
    int         max_length = 30; 
    const char* state_name = (void*)0;

    /* Get max name length, for later pretty printing.                      */
    for(i=0; i != me->aux.state.number; ++i) {
        length = strlen(self_get_state_name(me, i));
        if( length > max_length ) {
            max_length = length;
        }
    }

    fprintf(fh, "\n  STATES:\n");
    for(i=0; i != me->aux.state.number; ++i) {
        state_name = self_get_state_name(me, i);
        fprintf(fh, "    %s .", state_name); 
        self_print_space(state_name, max_length);
        fprintf(fh, "%s\n", me->aux.state.coverage[i] ? "........ [OK]" : 
                                                        ". [UNTOUCHED]");
    }
}

void 
hwut_sm_walker_print_coverage_condition(FILE* fh, hwut_sm_walker_t* me)
/* Prints information about conditions settings which never occurred during
 * the experiments. 
 * 
 * ASSUMES: '.state_db' must have been set by the derived class.             */
{
    int                          i              = 0; 
    int                          max_length     = 27;
    int                          length         = 0;
    const char*                  condition_name = (void*)0;
    hwut_sm_condition_coverage_t coverage       = (hwut_sm_condition_coverage_t)0; 

    /* Get max name length, for later pretty printing.                      */
    for(i=0; i != me->aux.condition.number; ++i) {
        length = strlen(self_get_condition_name(me, i));
        if( length > max_length ) {
            max_length = length;
        }
    }

    fprintf(fh, "\n  CONDITIONS:\n");
    for(i=0; i != me->aux.condition.number; ++i) {
        condition_name = self_get_condition_name(me, i);
        fprintf(fh, "    %s .", condition_name); 
        self_print_space(condition_name, max_length);
        coverage = me->aux.condition.coverage[i];
        fprintf(fh, ". [%s] [%s]\n", 
                coverage & HWUT_SM_WALKER_CONDITION_TRUE  ? "TRUE" : "    ",
                coverage & HWUT_SM_WALKER_CONDITION_FALSE ? "FALSE" : "     ");
    }
}

void 
hwut_sm_walker_print_coverage(FILE* fh, hwut_sm_walker_t* me) 
/* Prints information about state and condition coverage using the functions
 * mentioned below. See detailed comments at their entry.                    */
{
    hwut_sm_walker_print_coverage_state(fh, me);
    hwut_sm_walker_print_coverage_condition(fh, me);
}

static void
self_condition_double_check(hwut_sm_walker_t* me, 
                            int               ConditionId)
/* This function is used to double check the correctness of a condition. 
 * It is assumed that the same path has been walked along before and the 
 * condition was true (otherwise one would not have gone any further. 
 *
 * During a second walk along the transitions the same condition must 
 * hold. Otherwise, the state machine is not consistently managed from 
 * 'do_init()' along the event chains.                                       
 *
 * ABORTS: If the condition is not true.                                     */
{
    int abs_index = ConditionId >= 0 ? ConditionId : - ConditionId;

    if( self_call_do_condition(me, ConditionId) ) {
        return;
    }
    hwut_sm_walker_print(stdout, me, 80);
    hwut_printf("\nInconsistent state machine behavior! Starting with 'do_init()' followed\n"
                "by the same sequence of events, a condition differs.\n");
    hwut_printf("'%s'", me->aux.condition_id_db.begin[abs_index]);
    hwut_printf(" is now '%s'; earlier on same path it was different.\n", 
                ConditionId >= 0 ? "false" : "true");
    hwut_exit();
}

static void
self_aux_print_comment(const char** CommentArray, int Index)
{
    if( CommentArray == (void*)0 ) {
        return;
    } 
    else if( CommentArray[Index] == (void*)0 ) {
        return;
    }
    hwut_printf("Comment: \"%s\"\n", CommentArray[Index]);
}

static void
self_on_bad_state(hwut_sm_walker_t* me, const hwut_sm_state_t* StateP)
{
    int NormSi = StateP->id - me->aux.state.offset_id;

    assert(NormSi >= 0 && NormSi < me->aux.state.number);

    hwut_sm_walker_print(stdout, me, 80);
    hwut_printf("\nForbidden state '%s' has been entered.\n", StateP->name); 
    self_aux_print_comment(me->aux.state.forbidden_comment, NormSi);
    hwut_exit();
}

static void
self_on_bad_condition(hwut_sm_walker_t* me, int ConditionId, int Value)
{
    int NormCi = ConditionId == 0 ? 0 : ConditionId - me->aux.condition.offset_id;
    assert(NormCi >= 0 && NormCi < me->aux.condition.number);

    hwut_sm_walker_print(stdout, me, 80);
    hwut_printf("\nForbidden value '%s' for condition '%s'.\n",
                Value ? "true" : "false", 
                me->aux.condition_id_db.begin[ConditionId]);
    self_aux_print_comment(me->aux.condition.norm_comment, NormCi);
    hwut_exit();
}
#else
static void
self_on_bad_state(hwut_sm_walker_t* me, const hwut_sm_state_t* StateP)
{ hwut_exit(); }

static void
self_on_bad_condition(hwut_sm_walker_t* me, int ConditionId, int Value)
{ hwut_exit(); }
#endif /* not HWUT_OPTION_STDIO_FORBIDDEN */
