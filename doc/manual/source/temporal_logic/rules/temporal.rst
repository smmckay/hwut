Temporal rules consist of statements that have restricted validity in time. A
temporal rule can be in two states: either it sleeps or is awake. If it sleeps
it does not pose any condition on the current event sequence. If it is awake,
its related condition has to be considered. HWUT allows to awake a temoral
condition and to send it to sleep via conditions of any kind. An awake
condition can be specified following the `from` key word. A sleep condition can
be specified following the `to` keyword.  Such constructs are termed 'time
span' in HWUT's language. For a temporal rule the time span needs to be 
followed by a ':' and a condition that has to hold during the time that the 
rule is awake.

If there is no `from` keyword followed by a condition, it is assumed that the
condition is awake from the beginning. If there is no `to` keyword followed by
a condition it is assumed that the condition is awake until the end of the
test. The total absense of a `from` and `to` keyword means that the condition
is always awake, which means that it is, actually, an absolute condition. Note,
that this case, the ':' is to be omitted and thus it is syntactically identical
to the absolute condition as described in the previous section.

The following example shows a temporal rule that is active from the moment
that the BUTTON event occured to the time that the light switch is turned off.

.. code-block:: cpp

    from BUTTON to LIGHT_SWITCH.state == "off":   $context_switch_n < 13;

The following two examples show rules that only have an awakening condition or
a sleep condition:
 
.. code-block:: cpp

    from $1 > RESET_BUTTON.time + 10.2:       RESTART.count;
    to   INIT_PROCESS.state == "terminated":  SYSTEM_STATE.run_level < 5;

Note in particular, that the condition `RESTART` in the rule section does not make
much sense. As with absolute conditions these conditions are only true at the moment
that the event occurs. The same discussion as for absolute rules holds for the
rule part of temporal rules.


