Formal Explanation
==================

Where the previous section introduced how rules can be specified to the
temporal logic engine, this section focusses on the detailes of syntax and
underlying mechanisms. It is essential to understand that the set of all 
rules is applied on the appearance of each single event. There are three
basic event specifics that can appear in conditions of rules:

EVENT_NAME::

    If an event-name occurs in as a condition it considered to be `True`
    exactly at the time it occurs and `False` at any time else. The assignment
    of `$base_count` in the rule

    .. code-block:: cpp
            if POWER_ON then $base_count = 0;

    happens only at the time when the POWER_ON event occurs. Note, that `POWER_ON`
    has appeared some time before. Thus combining such conditions might result 
    in unwanted behavior. For example in the following rule

    .. code-block:: cpp
            CD_INSERTED and POWER_ON => START_PLAY;

    The user might want to specify that the as soon as the CD is inserted and the power
    is on, the implicit event `START_PLAY` is to be produced. An event sequent such 
    as 

    .. code-block:: cpp
            >>>> 0.001:  POWER_ON;
            ....
            >>>> 12.041: CD_INSERTED;

    will _not_ trigger the implicit event. This is so for the simple reason that `CD_INSERTED`
    and `POWER_ON` do not appear at the same point in time. `POWER_ON` is only true at time
    0.001 seconds, and `CD_INSERTED` is only true at 12.041 seconds. In order to express the 
    desired behavior, the following would have to be specified:

    .. code-block:: cpp
            CD_INSERTED.count and POWER_ON.count => START_PLAY;

EVENT_NAME.count::

    The number of times that the event has occured. It is zero as long as the event
    has never occured.

EVENT_NAME.time::

    The time when the event has occured the last time.

Additionally, the special variable `%time0` represents the time when a condition
awake.  The special variable `%time` represent the current time.  A condition can
consist of a numeric term, a comparison, or an event name. The operators `and`
and `or` enable combinations of conditions, the comparators `<`, `>`, `>=`,
`<=`, `==`, and `!=` can be used for comparison of two numeric terms in the
usual C-style. A `not` in front of a condition stands for negation. Conditions
can be bracketed in order to group conditions different from the usual
precedence of `and` over `or`.  As mentioned earlier, there are four basic
types of rules in HWUT's temporal logic engine. In the subsequent sections
absolute rules, temporal rules, assignemments and implicit statements are
explained.


Temporal Rules::

    Temporal rules are rules that _sleep_ and _awake_. This means that there are conditions
    for them to enter an awake state and conditions on which they enter a sleep state. In the
    awake state there related rules are active and have to be true. In the sleep state 
    all related rules are ignored.

Assignments::

    For the sake of elegance, HWUT allows to specify variables that can be assigned some
    numeric terms. Assignments do not result in a truth value, nor do they judge anything.
    Assignments produce placeholders for numeric terms. A variable $avrg_size might
    for example compute the avarage size of objects that were allocated (provided that
    at each allocation an `OBJECT` event is sent.):

    [cpp]
    source~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    $avrg_size = OBJECT.size / OBJECT.count;
    source~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    
Implicit Statements::

    Implicit statements are also means to simplify the expression of rules.
    They allow to trigger events that do not come from the test application.
    Implicit statements produce placeholders for conditions. A placeholder
    `SYSTEM_FAILURE` for the condition that a segmentation fault occured during the
    sanity check might look like this:

    [cpp]
    source~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    SANITY_CHECK.active == "Yes" and SEGMENTATION_FAULT  => SYSTEM_FAILURE;
    source~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Other rules can then determine whether a system failure occured and when it occured
    by looking at the `.count` and `.time` members of the event `SYSTEM_FAILURE`.


