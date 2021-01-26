That is events act like similar to function calls. The first line tells
the temporal logic engine that a START event occured. The second line
notifies about a BOOT event. It is adorned with the parameters
`vga`, `acpi`, and `maxcpu_n`. These paremeters can be used in rules as 
if they were members of the event object, i.e. `BOOT.vga`, `BOOT.acpi`, 
and `BOOT.maxcpu_n`. The `INIT_3` event is adorned with arguments
that have no name. They can be accessed in rules like array elements, i.e.
`INETD[0]`, `INETD[1]`, and `INETD[2]`. Note, that the members of `BOOT`
could have been accessed the same way. More on attributes of events 
is to be discussed in the rules section. 

Events can tell about their origin and the time that they occur. The following
event PRINT tells, that it was triggered from within a file called "hello.c" line 10: 

.. code-block:: cpp

    >>>> "hello.c":10:  PRINT(str="hello world!");
 
Events can also specify a particular time, i.e.

.. code-block:: cpp

    >>>> 0.0014:  PRINT(str="hello world!");
 
would tell the temporal logic engine that the PRINT event happend 0.0014 seconds
after the start of the program. Note, that times need to be continuous and shall
never go backwards. Finally, an event can tell about is position in the source
code and the time it occured at once. In the example:

.. code-block:: cpp

    >>>> "hello.c":10: 0.23:  PRINT(str="hello hwut!");
 
the PRINT event tells that it originates in file `hello.c` line 10 
and that it was trigger 0.23 seconds after program start. For debugging
purposes the output can also contain `log` statements that are 
followed by numeric terms, this will help analysing the inner 
functioning of the engine together with the rule set. The `log`
statement: 

.. code-block:: cpp

    >>>> log BUTTON.count / $1;

will print the ratio of the event that BUTTON occured with respect to the time
that has passed. The special variable $1 represents the current time. The exact
syntax for numeric terms is explained together with the temporal logic rules in
the subsequent section.

Logic statements are usually absolute. A statement is either true or 
false. Absolute statements can be specified in HWUT in a manner
similar to C. The line

.. code-block:: cpp

    ERROR.count < 10;

tells that the number of ERROR events shall never exceed 10.
Temporal logic <<cite>> stays abreast of the fact that some 
rules have a restricted scope. Imagine, a system where the even X
shall only occur in between 5 seconds after START. In this case, 
the statement 'X occurs' is correct only from the moment that 
START occured to 5 seconds later. HWUT allows to specify such 
a rule the following way:

.. code-block:: cpp

    to   START:            not X;
    from START.time + 5.0: not X;

The first line says that from the begin of the test until START appears
X is not to appear. The second line says that from five seconds later
to the end of the test X is not to appear. Imagine a rule that says that
between the events START and END the number of ERROR events shall not be 
greater than 100. This could be specified in HWUT by the following rule:
 
.. code-block:: cpp

    from START to END:   ERROR.count < 100;

The conditions restricting the time domain can be of any shape. It is
possible for example to say that if a BUTTON_PRESS event occured 
twice and the system has received a LOCK message, then there shall 
never be a NETWORK_ACCESS:

.. code-block:: cpp

    from BUTTON_PRESS.count == 2 and LOCK.count > 0 : not NETWORK_ACCESS;

Additionally, implicit events can be specified. This might simply
the specification of rules. Using '=>' The above condition might be called
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

    $error_ratio > 0.5 => WAIT_FOR_REBOOT;
    from WAIT_FOR_REBOOT to WAIT_FOR_REBOOT.time + 3.2: REBOOT; 

This says, that as soon as the error ratio becomes greater than 
0.5, i.e. every two seconds one error, then the system has to 
initiate a reboot in less then 3.2 seconds. Scenario constellations
can be effectively tested with `if`-`then` blocks. The RESET rule
for the Control-Alt-Delete Salute can be specified as
 
.. code-block:: cpp

    if CONTROL and ALT and DELETE then RESET;
    else                               NORMAL_OPERATION;

Rules can be grouped by curly brackes, such that more than one rule
can appear, for example in an `if`-block:

.. code-block:: cpp

    if NO_RESPONSE then { 
            RETRY.count > 3; 
            ERROR.count < 10; 
            (NO_RESPONSE.time - START.time) < 0.5;
    }


