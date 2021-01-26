State Machine Walkers
----------------------

A *state machine* is an abstract machine. At one specific time it can only be
in one state of a finite set of states.  A *state* describes the waiting to
execute a transition. A *transition* is a set of actions to be executed when a
*condition* is fulfilled or when an *event* is received. Actions may be performed
on *entry* or on *exit* of a state. With the aforementioned concepts and an
*initial state* the behavior of the abstract machine is distinctly described. 

In HWUT events and conditions are defined as follows.

.. describe:: Condition

    The evaluation of a condition is a passive act of *observeration or
    reading*. It does neither influence the state machine nor any other tracing
    component.  Its result is a boolean statement, true or false, telling whether
    the condition holds or not. It virtually happens in no-time.

.. describe:: Event

   An event potentially *changes or writes content*. Upon an event *exit* actions 
   upon leaving a state and *entry* actions upon entry into a state
   may be performed. Also, other components such as tracing components
   or supported hardware maybe influenced. It potentially consumes time.

A transition in the above sense can be modelled by the following
sequence--given in HWUT's syntax::

      STATE_A ----| CONDITION |-----( EVENT )----> STATE_B

That is, for a given state ``STATE_A`` a transition is only considered after 
checking the ``CONDITION``. The checking is a pure *read* operation and does
not change any thing. If the condition holds an ``EVENT`` can be received, 
i.e. something can be *written* and the state ``STATE_B`` is entered.

The correctness of state machines can hardly be specified in terms of causal
relations described in tables for input and expected output.  The determination
of possible paths through state machines is a non-trivial task for the human
operator. HWUT state machine walkers are designed to help sampling the space of
possible paths through a state machine.

Based on a description of the state machine HWUT can produce code of a state
machine walker. A state machine walker is a program which walks along possible
paths of the state machine. On its way it interacts with the user's test
program so that the subject can be initiated to transit through the same states
in parallel. A very basic test would verify whether the subject's state is the
same as the state which the state machine walker thinks it is.

The following code fragment shows some example code in C using a state machine 
walker. 

.. code-block:: cpp

    ...
    myWalker_t  me;
    my_data_t   my_data;
    ...

    myWalker_execute(&me, &my_data, do_init, do_terminal);
    ...

That is, one has to create an object of the state machine walker and the data
which is to be investigated. A call to an execution function initiates the
complete test. During execution the state machine walker runs through all
states and interacts with the callbacks ``do_init`` and ``do_terminal`` with
the user code.

Events and conditions are described in small code fragments. This way larger
lists of events and conditions can be kept very transparent. 

The following sections show first, how state machines are describes, explain
how the state machine walker interacts with the test code, and finally 
provide a minimalist example which is intended to explain all mentioned
concepts.

Note, that the interface that triggers the state machine walk does not contain
an initial state. This has been done by purpose. It is assumed that the 
state machine is initialized towards a specific initial state. From there
on the state machine can be held responsible to maintain its data consistent.

State Machine Description
=========================

State machines can be described by means of HWUT's scripting language Smih
(for 'state machines in hwut').  For example, the following code describes a
password-secured door opener.::

          SLEEP --------------------( ACTIVATE )------ LISTEN
            
          LISTEN -------------------( PW_WRONG )------ SLEEP
              '-----| CLEARANCE |---( PW_CORRECT )---- OPEN

          OPEN ---------------------( CLOSED )-------- SLEEP
 
As can be seen, the syntax of is very close to the graphics description of a
state machine. It is intuitively clear what the states are and how they transit
to each other. In the above example, the event ``ACTIVATE`` causes a transition
from ``SLEEP`` to ``LISTEN``. Once, the state machine is listening the event
``PW_CORRECT`` may report the receiption of the correct password. Then, if the
condition ``CLEARANCE`` is fulfilled, it transits from ``LISTEN`` to
``OPEN``, etc.

While the description is transparent and intuitive, it is at the same time
formal. That is, it distinctly describes a state machine. The basic element of
the syntax is a transition. A transition *must* contain an event or a
condition. A minimal transition would be the transition::

         START ---( EVENT )------- TARGET

or::

         START ---| CONDITION |--- TARGET

A condition may be prefixed by a ``not`` stating that the transition shall
only happen if the condition fails, i.e.::

         START ---| not CONDITION |--- TARGET

Conditions and events, can of course appear in on transition::

         START ---| CONDITION |---( EVENT )--- TARGET

Formally, the transition description starts with an identifier for the start
state. It is followed by an arbitrarily long list of '-' signs. Then follows
the specification of a condition and an event, or only an event. A condition
specification is an identifier bracketed by '|'. An event specification is an
identifier bracketed by an opening '(' and a closing ')'. Between the
specifications there might be an arbitrary amount of '-' signs indicating
lines. At the end of the line comes the identifier for the target state. 

Using ' and . the description can be made clearer and easier to read. 
The ' at the beginning of the line refers to the last mentioned start
state. At the end of a line it refers to the last mentioned target 
state. Thus,::

         START ---| COLD |---( RING )--- TARGET
           '------| HOT |----( RING )------'    

is equivalent to::

         START ---| COLD |---( RING )--- TARGET
         START ---| HOT |----( RING )--- TARGET 

The . may be used to refer to the next specified start and target state. 
Thus the aforementioned example may be specified also by::

           .------| COLD |---( RING )------.    
         START ---| HOT |----( RING )--- TARGET 

The reference may span multiple lines, so that a list of transition 
descriptions as in::

           .------| COLD |---( RING )------.    
           .-----------------( RESET )----- TARGET
         START ---| ICY |----( RING )--------'  
           .-----------------( BUZZ )--------'
         SLEEP --------------( BUZZ )--------'
          
is perfectly reasonable. Next, it must be specified what events and
conditions actually mean. For this ``EVENTS`` and ``CONDITIONS``
sections need to be introduced.::

    ---// EVENTS //-------------------

            RING  { my_thing_ring(&self.bell); }
            RESET { reboot(&self.main_process, 10 /* ms */); }
            BUZZ  { send_watchdog_request(); }

    ---// CONDITIONS //-------------------

            COLD  { return self.get_temperature() <  36; }
            ICY   { return self.get_temperature() <= 0; }

The code inside the curly braces is code of the target language. In this 
case it is C-code. Inside those brackets the following objects are
available. 

 .. describe:: myWalker_t* me

    A pointer to the state machine walker object. The type name consists
    of the walker's name plus ``_t`` suffix.

 .. describe:: userData_t  self

    This is a reference to the user's data. It is a small shortcut for 
    ``*(me->subject)`` which makes the code much more readable.

 .. describe:: hwut_sm_state_t* state

    A pointer to the current state. 

For events the the ``EventId`` is provided. It is of type
``myWalker_event_id_t``.  For conditions the ``ConditionId`` of type
``myWalker_condition_id_t`` holds the condition under concern. In bother
handlers, ``EVENTS`` and ``CONDITIONS``, the sections for what happens at
begin and at end can be defined by definitions of ``@begin { ... }`` and
``@end { ... }``. This is helpful for things that happen at every event
or every condition check. 

Imagine, for example, when working in a multi-thread environment where the
state machine under inverstigation runs in a separate thread. For the
state machine walker it is essential that its states are aligned with the 
ones of its subject. Then, the ``@end`` section may be used to wait for
the state machine entering in its subsequent state, something like

.. code-block:: cpp

    ---// EVENTS //-------------------
        @begin { 
            state_machine_event_id_t event; 
        }
        ...
        ALERT { event = SM_EVENT_ALERT; }
        BUZZ  { event = SM_EVENT_BUZZ; }
        ...
        @end {
            state_machine_receive_event(&self.sm, event);
            while( ! state_machine_receive_stable_state(&self.sm) ) {
                sleep(1);
            }
        }

The above example also uses the ``@begin`` keyword to define the 
variable ``event`` which is used in the event handlers. The actual
event then sent to the state machine in the ``@end`` fragment, where
one waits for the state machine to reach its subsequent stable state.

A special kind of event is a 'joker'. This event does precisely nothing. A
joker stands for a state transition without external influence. An event name
in the ``EVENTS`` section with a ``*`` suffix is considered to be a joker.  For
those events neither ``@begin`` nor ``@end`` is executed. Empty event handlers
still execute ``@begin`` and ``@end``. Thus a definition

     @begin  { printf("begin,\\n"); }
     JOKER   * 
     IDLE    {}
     @end    { printf("end.\\n"); }

will print ``begin,end.`` when an ``IDLE`` event occurrs, but it will 
print nothing upon the execution of ``JOKER``.

The ``@begin`` section comes particularily handy in cases that a deviation
between the state machine walker's state and the subject's state has been
detected. In such cases, diving further does not make sense. The further diving
into the state machine can be prevented by returning '0' at this point in time
in a code similar to the following:

.. code-block:: cpp 

    ---// CONDITIONS //-------------------

        @begin { 
            if( ! self_match(state->id, self.state_id) ) {
                hwut_sm_walker_print(&me->base);
                return 0;   /* Deviation => do not dive any further. */
            }
        }
    

State Machine Walker Interaction
================================

A state machine walker tells the test program what to do with the subject
and queries about its condition. The tester must provide callbacks to the
state machine walker which handle those tasks. Each of the callbacks
receives a pointer to the state machine walker as first argument. Inside
the state machine walker, there is a member ``subject`` which points 
to the user's data. The following callbacks must be provided.

.. describe: do_init(walker)

   When this function is called the subject state machine needs to be
   initialized.  This happens each time the state machine walker starts a new
   path. Moreover, all resources which are initially required must be allocated.
   This may mean, for example, that files need to be opened, network connections
   must be established, or some memory needs to be allocated.

.. describe: do_terminal(walker, state)

   A call to this callback signalizes that the path walker has reached an
   end. There are three possible termination conditions:

      -- A dead end has been reached without any further possible transition. 

      -- The maximum path length has been reached. 

      -- A maximum loop number has been exceeeded.

With these handlers in place the state machine walker's execute function 
can be called. In any place the current path can be printed using 

.. code-block:: cpp

      hwut_sm_walker_print(stdout, &walker);

which results in pretty prints of conditions, events, and states on the
current path, e.g.::

    [[BEGIN]]--.
     .---------'
     STATE_A -->--( MESSAGE )-- STATE_B -->--| HOT |--.
     .------------------------------------------------'
    ( BUZZ )-- STATE_C -->--| COLD |--( BUZZ )--.
     .------------------------------------------'
     STATE_D

For this to be available, the header ``hwut_unit.h`` must be included. If it is
supposed to be called from event or comments, it must actually be specified
inside the source code paste section, i.e. between the dashed lines.  These
printouts are intended to facilitate the reflection on what happend in case of
unexpected behavior. With the macro ``hwut_verify_verbose_walk(...)`` the print of the
path in case of error is implemented.

A less elegant, but more consise print-out of the curent path can is done
using the function.

.. c:function:: void hwut_sm_walker_print_plain(FILE* fh, hwut_sm_walker_t* me)

This function prints exactly one line for one path. Printing a list of paths
from within the 'on_terminal' handler allows to review the set of walked
through pathes.

Minimalist Example
##################

In this example, the previously mentioned example of the password protected
door opener is used. Let the following header describe its interface and let 
it be stored in a file ``door-opener.h``

.. code-block:: cpp

    enum { MODE_OFF, MODE_IDLE, MODE_RUNNING }     DoorOpener_mode_id_t;
    enum { STATE_SLEEP, STATE_LISTEN, STATE_OPEN } DoorOpener_state_id_t; 

    typedef struct {
       DoorOpener_mode_id_t  mode;
       DoorOpener_state_id_t state; 
    } DoorOpener_t;

    enum { EVENT_ACTIVATE, 
           EVENT_WRONG_PASSWORD, 
           EVENT_CORRECT_PASSWORD, 
           EVENT_DOOR_SNAPPED_CLOSED 
    };

    void DoorOpener_init(DoorOpener_t* me);
    void DoorOpener_destruct(DoorOpener_t* me);
    void DoorOpener_clearance(DoorOpener_t* me);
    void DoorOpener_handle_event(DoorOpener_t* me, int TheEvent);

    void DoorOpener_get_state_name(DoorOpener_state_id_t);

This example lacks the definition of the ``DoorOpener_t`` state machine which
is left as an exercise.  As with iterators, a state machine walker is framed by
tags and dashed lines, as can be seen below.

.. code-block:: cpp

    /*
    <<hwut-sm_walker:  myWalker DoorOpener_t 256 10>> 
    ------------------------------------------------------------------------
    #include "door-opener.h"    
    #include "hwut_unit.h"       /* We want hwut_verify_verbose_walk() in EVENTS. */

    struct myWalker_t_tag;
    void assert_match(myWalker_t_tag* walker, hwut_sm_state_t* state);

    ------------------------------------------------------------------------
          SLEEP --------------------( ACTIVATE )------ LISTEN
            
          LISTEN -------------------( PW_WRONG )------ SLEEP
              '-----| CLEARANCE |---( PW_CORRECT )---- OPEN

          OPEN -----| AWAKE |-------( CLOSED )-------- SLEEP
    ...

In the arguments following the ``hwut-sm_walker`` basic parameters of the
walker are the defined. The first argument defines the walker's type name (here
``myWalker``).  In the source code, this name appears with a ``_t`` appended.
Then the subject's type is defined (here ``DoorOpener_t``). The third argument
defines the maximum path length (here ``256``) and the forth argument defines
the maximum loop number (here ``4``). The maximum loop number defines how many
times the same state can be entered under the same condition with the same
event before the path will be broken up. 

As with generators, the output is generated into a .c and .h file according
to what is specified by the ``-o file-stem`` command line option.

The source code paste section includes the header file of the door opener 
and the 'hwut_unit.h' file which comes handy many places. The function 
``assert_match`` is also defined here, so that the event handlers and the
condition handlers may use it. Note, that the state machine walker's struct
must be referred to by forward declaration ``struct myWalker_t_tag``. Once 
the struct is defined it is identical to ``myWalker_t``.

What follows the first dash line is the source code required for the state
machine walker implementation. In this case, a simple inclusion of the door
opener's header does the job. What follows the second dashed line is the
definition of the state machine in the aforementioned format.

Now, it must be specified what those events actually mean. Inside a dashed line
with a ``EVENTS`` title bracketed by ``//`` those events are defined. The two
special sections ``@begin`` and ``@end`` define what has to happen at the
beginning and the end of each condition handling.

In our example, the function ``DoorOpener_handle_event`` shall be called with
event ids which map the events from the state machine.

.. code-block:: cpp

    ...
    -----// EVENTS //-------------------------------------------------------

        @begin {
            DoorOpener_event_id_t  event_id = EVENT_VOID; 
            assert_match(walker, state);
        }

        ACTIVATE   { event_id = EVENT_ACTIVATE;  }       
        PW_WRONG   { event_id = EVENT_WRONG_PASSWORD;  }  
        PW_CORRECT { event_id = EVENT_CORRECT_PASSWORD; }  
        CLOSED     { event_id = EVENT_DOOR_SNAPPED_CLOSED; }
        
        @end { 
            DoorOpener_handle_event(&self, event_id);
        }
    ...

Conditions work in a very similar fashion, only that they may return an integer
of ``1`` for true or ``0`` for wrong. 

.. code-block:: cpp

    ...
    -----// CONDITIONS //---------------------------------------------------

          CLEARANCE  { return DoorOpener_clearance(&self) > 0; }
          AWAKE      { return self.mode != MODE_OFF; }
    ------------------------------------------------------------------------
    */

Then, in the same file the test setup can follow. As mentioned earlier the ``self``
inside the condition or event specifications relate to the 'subject' under test
which has been passed to the state machine walker. Once the state machine has
been defined, the actual testing code becomes close to trivial. 

.. code-block:: cpp

    #include "hwut_unit.h"
    #include "myWalker.h"

    static void   do_init(myWalker_t* me);
    static void   do_terminal(myWalker_t* me, hwut_sm_state_t* state);

    int main(int argc, char** argv) 
    {
        myWalker_t   walker;
        DoorOpener_t subject;

        hwut_info("Walk along a state machine;");

        myWalker_execute(&walker, &subject, do_init, do_terminal);
    }

All that remains is the definition of the ``do_init`` and ``do_terminal`` needs
to be defined.  First, upon initialization the door opener needs to be
initialized. It has been passed as the second argument to ``myWalker_execute``
and is nested inside the walker as ``subject``.

.. code-block:: cpp

    static void   
    do_init(myWalker_t* me)
    {
        DoorOpener_init(me->subject);
    }

When the end of a path is reached, the door opener needs to release all
resources which it has required. For example, memory, file handles, and
network connections are typical candidates of what may need to be 
freed. Usually, there is a destructor or 'uninitialize' function that
does the job. The resource-freeing happens in the callback ``do_terminal``
when the state walker has reached the end of a path. For the door 
opener the following may be appropriate:

.. code-block:: cpp

    static void   
    do_terminal(myWalker_t* me, hwut_sm_state_t* state) {
        DoorOpener_destruct(me->subject);
    }
   
What remains is a tiny function which should help to see whether the 
state of the subject matches the state which the state machine walker
thinks he is in.

.. code-block:: cpp

   void
   assert_match(myWalker_t* walker, hwut_sm_state_t* state) 
   {
       switch( state->id ) {
       case myWalker_SLEEP:   expected_state_id = STATE_SLEEP; break;
       case myWalker_LISTEN:  expected_state_id = STATE_LISTEN; break;
       case myWalker_OPEN:    expected_state_id = STATE_OPEN; break;
       }
       hwut_verify_verbose_walk_silent(walker, 
                               walker->subject->state_id == expected_state_id);
   }

Tips and Tricks
===============

The HWUT model implements the very basic ideas of a state machine rigidly. This
may lead to some questions as to how to implement scenarios which appear in 
real-life applications. In this section, some of those cases are discussed and
how they might have to treated.

Transitions Without Events
##########################

There might be state transitions without any (external) event. In HWUT 
such transition sequences may be implemented by 'jokers'. Jokers are events
which do not do anything but transiting to a subsequent state. For example
the code fragment::

     BOOT  --------( STEP )-----> MMU_SETUP
     MMU_SETUP ----( STEP )-----> NETWORK_INIT
     NETWORK_INIT--( STEP )-----> LOGIN_USER_INTERFACE

describes a sequence of states where there is no user interaction when the
state machine transitions from ``BOOT`` to ``LOGIN_USER_INTERFACE``. The name ``STEP``
has been named arbitrarily to specify an event that does nothing. The ``EVENTS``
section shall either not contain any definition of ``STEP``, or a definition
by a single ``*`` as discussed before.


Post Conditions
###############

Another, more subtle issue occurs if a state machine contains a condition
*after* an event. This breaks with a fundamental idea. Events are associated
with *state change* and *write access*. Conditions *only read*. They do not
change anything. Setting the condition before the event implements an 'examining
before doing' or 'watching before stepping' pattern. In such an environment,
any change to the state machine is reflected in an explicit state transition--
which may be a transition on the state itself. Intuitively, descriptions that
follow this pattern support robustness and transparency.

A condition after an event means that things may be done before things are
examined. Moreover, hidden state variables may be modified from inside
the event, but then a condition may prevent a state transition. Changes
may happend beyond the scope of transitions. Intuitively, such post
conditions oscure state machine descriptions. 

From the discussion above, post conditions are best avoided. Fact is however,
that post conditions are used in may state machines. For those who follow the
philosophy of the author of this text, any difficulty to express a state
machine in HWUT signalizes a required design change. Design changes are not
always feasible. In order to help with existing state machines, HWUT allows
post conditions, but implements them internally with an intermediate step.
Thus, it maintains internally the 'watching before stepping' pattern. 
For example a transition::

    A  ---( STEP )---| WATCH |--- B

is translated into::

    A  ---( STEP )------- A0
    A0 ---| WATCH |------ B
    A0 ---| not WATCH |-- B

There is no correspondent state ``A0`` in the real state machine. Thus, 
whenever the reported 'state' is considered it makes sense to check whether
it is real. For that, the function ``*_state_is_real()`` may be used. 
Example:

.. code-block:: cpp

   -----// EVENTS //-------------------------------------------------------

   @begin {
       if( myWalker_state_is_real(state) ) {
           assert_match(walker, state);
       }
   }

The above example only checks a state match in case that the considered state
is 'real', not a intermediate state which has been created by HWUT.  The check
for being real is implemented as a single comparision of the state's id with a
limit value.  Thus, this check does not have a significant impact on
performance.

Asserts
=======

HWUT supports the specification of assumptions on states and conditions. For
example, one might want to specify that an event may require that a certain 
state cannot be reached or a condition must hold. Or, it may be required
that a certain state must have been passed or a condition must have held
when a certain state is reached. Such assumptions can be specified by the
generate HWUT state machine walker interface:

.. c:function:: int hwut_sm_state_forbid(hwut_sm_walker_t* me, int StateId, const char* Comment);

   This function forbids a state to occur on the current path. If it occurs, 
   then the ``Comment`` and the path is printed and the program exists. 

   RETURNS: 1 if the state was forbidden before; 0 else.

.. c:function:: int hwut_sm_state_allow(hwut_sm_walker_t* me, int StateId);

   This function allows a possibly forbidden state to occur on the current path. 

.. c:function:: int hwut_sm_state_allow_all(hwut_sm_walker_t* me);

   This function allows a all states to occur.

.. c:function:: int hwut_sm_state_happened(hwut_sm_walker_t* me, int StateId);

   This function returns ``1`` if the state given by ``StateId`` has 
   been passed before on the current path. It returns ``0`` if this is 
   not the case. The current state is not included in the consideration.

Any pointer to a generated state machine walker can be safely passed to this 
functions, but to highlight the inheritance relationship the pointer to the
base may be passed explicitly. The code fragment

.. code-block:: cpp

    hwut_sm_walker_state_forbid(&walker->base, myWalker_IDLE, "Cannot happen");

is an appropriate way to forbid a state ``IDLE`` in state machine walker as it
is referenced in an event, for example. For conditions there is a similar 
interface:

.. c:function:: int hwut_sm_condition_impose(hwut_sm_walker_t* me, int ConditionId, int Value, const char* Comment);

    When this function is called a condition it is assumed that a
    condition given by ``ConditionId`` will have the value ``Value``.
    The condition's value can only be ``0`` for false or ``1`` for true.
    If sometime later the requirement does not hold, then the ``Comment``
    and the path is printed and the program exits.

.. c:function:: int hwut_sm_condition_release(hwut_sm_walker_t* me, int ConditionId);

    When this function is called any requirement on the given ``ConditionId``
    is released.

.. c:function:: int hwut_sm_condition_release_all(hwut_sm_walker_t*);

    When this function is called all requirements on any condition is released.

.. note::

    If asserts on states or conditions are supposed to active from the very
    start, then they *must* be setup in the 'do_init()' procedure. Otherwise,
    they will not be active as soon as the second path through the state 
    machine is walked along. 

    This is so, since whenever a path is started the state machine and the
    walker are reset. The reset of the walker includes a reset of the assertions. 
    The 'do_init()' function is called after those resets.

Coverage
========

While walking along all paths, the state machine walker keeps track of the
states that have been passed and the conditions that occurred. Handy functions
allows to write a short coverage report at the end of the experiment. This
report exposes states which have never been passed and condition results that
never appeared. The functions signature is as follows:

.. c:function:: void hwut_sm_walker_print_coverage_state(FILE* fh, hwut_sm_walker_t* me);

   Prints state coverage, only. Each state that has not been passed is reported by a 
   line as::
        
       STATES:
        Awake .................................. [OK]
        Idle ............................ [UNTOUCHED]
        Panik .................................. [OK]
        Network Shutdown ................ [UNTOUCHED]


.. c:function:: void hwut_sm_walker_print_coverage_condition(FILE* fh, hwut_sm_walker_t* me); 

   Prints condition coverage, only. For a condition setting that never appeared 
   a line such as one of the following is printed.::

       CONDITIONS:
         Warm ......................... [TRUE] [     ]
         Icy .......................... [    ] [FALSE]
         Cold ......................... [TRUE] [FALSE]

.. c:function:: void hwut_sm_walker_print_coverage(FILE* fh, hwut_sm_walker_t* me); 

   Prints both, state and condition coverage in the format pinpointed above.

