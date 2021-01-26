Absolute Rules
==============

A rule that is absolute has to hold at any time. At any event that comes in the
rule is checked and the temporal logic engine notifies an error as soon as it
is broken. Absolute rules are simply states without any `from` or `to`
keywords. They are simply conditions followed by a semi-colon. The following 
lines are example for absolute rules as they might appear in a program:

.. code-block:: cpp

    not SEGMENTATION_FAULT;          # there shall not be any segmentation faults
    START_UP_TERMINATED.time < 20;   # start-up has to be completed in less than 20 seconds
    CACHE_MISS.count / $1 < 100;     # the number of cache misses shall not exceed 100 / sec

If a test application writes to the standard output 

.. code-block:: cpp

    >>>> SEGMENTATION_FAULT(time=3.1243);

The first rule is broken and the test is marked as failed. A similar situation 
occurs when the event {\tt START_UP_TERMINATED} occurs at a time before
20 seconds after test start. Any formula can be constructed in absolute conditions. 
The third condition holds, for example as long as the quotient of the cache miss
events over time (special variable \$1) is less than 100. Absolute conditions describe
general rules that are not directly related to sequences.

Note, that the valid condition `START_UP_EVENT`, for example, does not make
much sense as an absolute rule. This rule is only true at the time, that the
event `START_UP_EVENT` actually arrives--not before and not after. The bank of
rules, though, is checked for any event that comes in. Any event that is
different from `START_UP_EVENT` will break the rule. Thus for any tests 
dealing with more than one event such a rule is simply misplaced.

