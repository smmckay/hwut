The temporal logic engine allows for different three different kinds of rules:
absolute rules, temporal rules, implicit statements, and assignments.  An
absolute rule is either true or false for all time. Absolute rule can be
specified in HWUT in a manner similar to C. The line

.. code-block:: cpp

        ERROR.count < 10;

Note, that in rule descriptions no leading `>>>>` string is required.  Rule
files are to be written exclusively for the temporal logic engine. They are not
spit out together with other output in a way similar to what happens to the
events.  tells that the number of ERROR events shall never exceed 10.  Temporal
logic <<cite>> stays abreast of the fact that some rules have a restricted
scope. Imagine, a system where the even X shall only occur in between 5 seconds
after START. In this case, the statement 'X occurs' is correct only from the
moment that START occured to 5 seconds later. HWUT allows to specify such a
rule the following way:

.. code-block:: cpp

        to   START:            not X;
        from START.time + 5.0: not X;

The first line says that from the begin of the test until START appears X is
not to appear. The second line says that from five seconds later to the end of
the test X is not to appear. Imagine a rule that says that between the events
START and END the number of ERROR events shall not be greater than 100. This
could be specified in HWUT by the following rule:
 
.. code-block:: cpp

        from START to END:   ERROR.count < 100;

The conditions restricting the time domain can be of any shape. It is possible
for example to say that if a BUTTON_PRESS event occured twice and the system
has received a LOCK message, then there shall never be a NETWORK_ACCESS until
the nex UNLOCK event arrives and the a ACKNOWLEDGEMENT is granted:

.. code-block:: cpp

        from BUTTON_PRESS.count == 2 and LOCK.count 
        to   UNLOCK.count and ACKNOWLEDGEMENT.count: 
             not NETWORK_ACCESS;

Note, that the `.count` member is not compared with anything.  Any numeric
expression that is unequal to zero is treated as `True`. Any numeric
expression resulting in zero is treated as a `False` condition.
`UNLOCK.count` is therefore equivalent to `UNLOCK.count != 0` which means that
the UNLOCK event has actually occured.  

Additionally, implicit events can be specified. This might simply the
specification of rules. Using '=>' The above condition might be called
BUTTON_WHILE_LOCKED and the above rule can be rewritten as

.. code-block:: cpp

        BUTTON_PRESS.count == 2 and LOCK.count > 0 => BUTTON_WHILE_LOCKED;
        from BUTTON_WHILE_LOCKED : not NETWORK_ACCESS;

Implicit statements allow to simplify conditions. Variables allow
to simplify numeric expressions. A variable `$error_ratio` might
be defined the following way:

.. code-block:: cpp

        $error_ration = ERROR.count / ERROR.time;

telling how many error happend per second such that rules can 
refer to it easily. Note, that variables start with a dollar sign. Events
start with a normal letter. The following rules use the shorthand
of the just defined variable. 

.. code-block:: cpp

        $error_ratio > 0.5 => __WAIT_FOR_REBOOT;
        from __WAIT_FOR_REBOOT to %time == __WAIT_FOR_REBOOT.time + 3.2: REBOOT; 

This says, that as soon as the error ratio becomes greater than 
0.5, i.e. every two seconds one error, then the system has to 
initiate a reboot in less then 3.2 seconds. Scenario constellations
can be effectively tested with `if`-`then` blocks. The RESET rule
for the Control-Alt-Delete Salute can be specified as
 
.. code-block:: cpp

    CONTROL and ALT and DELETE => SALUTE;
    # RESET has to come 100 ms after the ctrl-alt-delete salute.
    if   SALUTE.count and %time > SALUTE.time + 0.100 then RESET.count;
    else                                                   NORMAL_OPERATION;

Rules can be grouped by curly brackets, such that more than one rule
can appear, for example in an `if`-block:

.. code-block:: cpp

        if NO_RESPONSE then { 
                RETRY.count > 3; 
                ERROR.count < 10; 
                (NO_RESPONSE.time - START.time) < 0.5;
        }


