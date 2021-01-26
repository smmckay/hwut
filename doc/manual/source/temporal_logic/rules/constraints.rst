Constraints
###########

This section focusses on the usage of constraints for rules.  The temporal
logic distinguishes itself from from first-order logic by the derivation of
verdicts from temporal sequences. A first order rule would be::

         X is equal to Y

The verdict derived from that statement can be evaluated independent of the
point in time when it appears and independent from what events occur. The 
rule::

         from the time that A occurred until B occurs X is equal to Y

This statement 'awakens' the rule ``X is equal to Y`` by the event 'A'
and sets it to sleep by the event 'B'. This statement is significantly
different from an implication in first order logic, such as::

         if A is true and B is not true then X is equal to Y

The 'A' in temporal logic may become false and the rule ``X is equal to Y`` is
still alert. In the first order logic rule the equality condition is inactive
as soon as A is false.

Implications
############

Implications are means to constraint conditions by first order logic.  The
syntax is the pythonic version of the traditional 'if/else' block. For
example::

    if A.same_f: A.x == A.y;
    else:        A.x == A.y; 

tells that if the '.same_f' flag is set in an event, then both members '.x' and
'.y' must be the same, else they must be different. This rule must hold during
the whole experiment at every instance. Also pythonic is the syntax for the 
'else if' condition: ``elif``. An arbitrary sequence of ``elif`` conditions 
may follow an ``if`` statement, and they can be followed by an unconditional
``else``. The sequence in which they appear corresponds to the sequence in 
which they are evaluated. In the sequence::

    if   not A.correct_f: A.x == 0 and A.y == 0;
    elif A.same_f:        A.x == A.y;
    elif A.enabled_f:     A.x > 0 and A.y > 0;
    else:                 A.x == A.y; 

It is first checked whether ``A.correct_f`` is true. If it is not, then both
members must be zero. In the same sense, the '.same_f' is checked, then the
'.enabled_f' and if nothing triggers the rule ``A.x == A.y`` is considered.

A not-so pythonic variation of the 'if/else' block is the 'switch' statement.
If many conditions apply on a single value, then that's a case for it. For 
example.::

      switch A.length: {
      == 0:       A.database_size == 0;
      == 1:       A.database_size == 0;
      < MaxSize:  A.database_size == A.length - 1;
      else:       A.database_size == -1;
      }

What follows the ``switch`` statement is an expression which is to be
considered in the subsequent cases. Any case starts with a comparator.  The
above statement tells that if ``A.length`` is zero or one than
``A.database_size`` is zero. Only when it is greater than 1, the size of the
database shall be its length - 1. If the MaxSize is exceeded the database size
shall be reported as ``-1``.

At the time of this writing, the specification of the 'switch' statement is 
somewhat novel. However, the semantic constructs are nothing new. The only
difference to classical programming languages is that the leaves of the 
program text are not commands, but conditions. Their task is to fire a
failure notification in case that they are violated.

All implications imply that some condition R1 is considered if and only if
another condition R1 is true. This can be expressed in a truth diagram::


   R0  
       true               ===========            ==========
                         |           |          |          |
       false  ===========.............==========............==========

   R1
       alert              ===========            ==========
                         |           |          |          |
       asleep ===========.............==========............==========

An implication constraint the TheDude would be.::

   if ($time % 24 > 10) or ($time % 24 < 15): 
        not HOME and not BED;

which means that during the day time from 10am to 3pm TheDude is not supposed
to be in BED nor shall he be at HOME. Note, when events are mentioned in
conditions they produce a verdict of 'true' ony at the exact moment when they
appear. 

Implicated and rules without temporal constrains are always alert. Too many
of them may drain on the computing performance. 


Temporal Constraints
####################

Temporal rules are activated an deactivated by events or conditions becoming
true or false. An instantaneous alert can be specified using the ``on``
keyword. For example::

     on BOOT, RESET, IDLE->LOAD:
        up_time_ms > 3000;

The above statement says, that when a ``BOOT`` a ``RESET``, or a transition
from ``IDLE`` to ``LOAD`` occurs, then the uptime must have been at least 3000
(ms). Any number of events greater or equal one may be specified as trigger of
an instantaneous alert. The truth of the condition is not checked except at the
instances when those events occur. With E0 being a triggering event and R1 the
rule of concern, a truth-diagram looks like the following.::

   E0  
       true                                                 
                         |           |          |          |
       false  ===========.===========.==========.==========.==========

   R1
       alert                                                
                         |           |          |          |
       asleep ===========.===========.==========.==========.==========

In TheDude example, there was already an instantaneous alert based on the 
``WORK`` event. When it occured it was required that the need for sleep
is not higher than 9.::

    on WORK:
        WORK.nfs < 9;

The counterpart for conditions is implemented by ``once`` statements. It
appeared already in TheDude example tests.  There, it was checked whether 7
o'clock has been reached and if so, it was required that TheDude has slept at
least six hours.::

    once $time % 24 >= 7: {       
        ...
        slept_hour_n >= 6;
        ...
    }

A true condition in a ``once`` statement must first become false, before it can
trigger an alert again. With C0 as a 'once' condition and R1 as an associated
rule, the truth-diagram looks the following.:: 

   E0  
       true               ===========            ========== 
                         |           |          |          |
       false  ===========.............==========............==========

   R1
       alert                                                
                         |                      |            
       asleep ===========.======================.=====================

..note:: Difference between ``on`` and ``once`` and ``if``. 

   The behavior of the three rules::

          on   EVENT: print "triggered";
          once EVENT: print "triggered";
          if   EVENT: print "triggered";

   is exactly the same, because of the special nature of events. Events are 
   true only exactly at the instance when they occur an false otherwise. This
   may require some clarification.

   ``on`` followed by a comma separated list of events defines an event
    handler.  An event's handler is quickly identified at the moment when an
    it occurs. ``on`` can *only* be defined for events. It *cannot* be defined 
    for conditions. It is the fastest way to specify a reaction to event.

    ``once`` and ``if`` consider both conditions. ``once C`` and ``if C`` are
    equivalent if and only if all verdicts of ``C`` are directly controlled by 
    events. In the example::

           once EVENT or n == 1: print "A";
           if   EVENT or n == 1: print "B";

    the string ``"A"`` is printed whenever the ``EVENT`` occurs and at the 
    instances when ``n`` *becomes*  1. The string ``"B"`` is triggered whenever 
    ``EVENT`` occurs and while ``n`` *remains* 1.

Alertness of some longer extend as a consequence of an event can be specified
by the ``from`` and ``to`` keywords. By means of those two keywords it can be
specified from when and/or until when conditions have to be checked. For
example, the rule that before the memory is initialized, no memory should be
allocated may be expressed as::

     to MEMORY_INIT_DONE:  not MEMORY_ALLOCATION;

To the contrary, one might require that the network manager must be active
as soon as one of the applications started.::

     from APP_DISPLAY or APP_RADIO or APP_CLIMATE:
          NETWORK_MANAGER.status == "active";

With C0 as the condition and R1 as the associated rule, the truth diagram for
the ``from`` statement is the following.::

   E0
       true                                                 
                         |                                   
       false  ===========.============================================

   R1  
       alert              ============================================
                         |                                        
       asleep ===========.............................................

However short E0 may be true, it will trigger the alertness of the rules R0. R0
will remain alert until the end of the experiment.  The correspondent
truth-diagram of the ``to`` statement is::

   E0
       true                                                 
                                                  |                                   
       false  ====================================.===================

   R1  
       alert  ====================================                    
                                                  |               
       asleep .....................................===================

As soon as E0 becomes true, however short the time may be, it stops the
alertness of R1. A time span may be defined by using ``from`` and ``to`` in a
single statement. For example.::

    from INIT_DONE to TERMINATION: not SEGMENTATION_FAULT;

says that from the event of INIT_DONE to the event of TERMINATION the event
SEGMENTATION_FAULT has not to occur. With E0 being the 'from condition', E1
being to 'to condition', and R0 being the associated rule, the truth diagram
looks is::

   E0
       true                                                 
                         |   |   |                 |         
       false  ===========.===.===.=================.==================

   E1
       true                                                 
                                    |    |   |                                        
       false  ======================.====.===.========================

   R1  
       alert              ==========                ==================
                         |          |              |                
       asleep ===========............==============...................


R1 becomes alert as soon as E0 is true and it becomes asleep as soon as E1
becomes true. Once it is asleep again it may be activated again by a transition
of E0 from false to true. 

A constraint for TheDude's buzzer could be that the BUZZ event shall not occur
from the time that TheDude comes home until he goes to bed. The ``not BUZZ``
rule shall therefore be alert as in the following diagram::

   not BUZZ;

       alert                                     ========               
                                                |        |         
       asleep ==================================..........=============

   TheDude
               BED       HOME        WORK       HOME     BED
             ..|.........|...........|..........|........|.............


Note, however, that the following code does not do the work::

    from HOME to BED: not BUZZ;

because HOME is true *whenever* HOME is entered. So, when TheDude gets up in the
morning the ``not BUZZ`` rule becomes alert the whole day until TheDude 
enters finally the ``BED``. ::

   not BUZZ;

       alert              ==============================               
                         |                              |         
       asleep ===========................................=============

   TheDude
               BED       HOME        WORK       HOME     BED
             ..|.........|...........|..........|........|.............


This is clearly, not what was ment. To specified the desired behavior, the
declaration of a state machine comes handy.::

    state_machine HOME, WORK, BED;

    from (WORK->HOME) to BED: not BUZZ;

Here, the ``not BUZZ`` rules starts triggering after the transition from WORK
to HOME. The rule mentioned before would trigger upon any occurrence of HOME.
Note, that a state can only belong to one state machine. States in different
state machines must be named differently.

Precisely, the statement ``WORK->HOME`` means that the state machine related to
``WORK`` and ``HOME`` transits from ``WORK`` to ``HOME``. 
