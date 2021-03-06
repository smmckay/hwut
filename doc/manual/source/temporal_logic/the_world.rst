The World and the Court.
========================

The world inside hwut is a database of variables, passed events, functions,
and event handlers. It exists in paralell to the test. It's state is maintained
by events and variables. Events float into the world from the application. Variables
are set and adapted as a consequence of rules. The rules are maintained inside
the court. The rules are defined in a language called 'Joy' which is explained
in the following paragraphs.

In Joy information is processed in terms of objects, operations, and control 
structures. There are two types of objects: Events and variables. Events are
objects that appear at a certain time and trigger a court review. A court
review goes through all active rules and may detect broken rules. Variables
maintain data. The data may be plain passive data such as names or numbers, 
but may also be functions. To help to maintain data, container types for lists
and dictionaries are also available. The following enumeration provides a
short overview over variable types.

.. describe:: Numbers 

    Numbers can be specified in decimal, hexadecimal if preceeded by ``0x``,
    octal if preceeded by ``0o``, or binary if preceeded by ``0b``. Only decimal
    numbers can be used as floating point numbers. Example::

        x = 0b1000.1010;    # Assign 0x8A to variable x
        z = 0o777;          # Assign 0x1FF to variable z
        y = 0x4711;

.. describe:: Boolean

   The keywords ``true`` and ``false`` may be used to describe boolean constants.
   Example::

        x = true;
        y = false;

.. describe:: Strings

   Strings are specified by their traditional quote bracketting, such as in 
   ``"hello world!"``.

        x = "This is a string";

.. decscribe:: Functions

   Functions are defined by the keyword ``function`` followed by an argument
   list in '(' ')' brackets and a function body in '{' '}' brackets. Functions are
   best assigned directly to variables.  Example::

        x = function() {
            print "Hello World";
        };

   Note, that the ';' at the end is necessary, because function definitions are
   considered as normal assigment.

.. describe:: Lists

   A list is a data container that stores objects in a sequence. Objects 
   in the sequence can be addressed only by iteration or (position) index.
   A list is specified by a comma seperated list in '[' ']' brackets. 
   Example::

        x = [1, 2, 3];
        y = [];

   List have member functions which help to operate on them, as they are

        .pop()
        .insert()
        .size()
        .count()
        .delete()

   Elements of lists can be iterated over in 'for in' expressions or accessed
   via the index, such as in 

        x = my_list[23];

   which accesses element '23' in ``my_list``.

.. describe:: Maps

   A map is a data container that can match a string, a boolean, or a number
   to another object. That is, objects are refered to by a key (string, 
   boolean, or number). Example::

        x = { "Otto": 17, "Fritz": 12, };

   Elements in maps can be accessed with the same operator, i.e.::

        x = my_map["Otto"]; 

   catches what is associated with "Otto" from the map.

There are special variables in the world starting with a dollar sign.

.. describe:: $INIT

   ``$INIT`` is the event of initialization. It appears before any other event
   is processed. It is particularily useful to setup an initialization in the 
   rules, such as::

               on $INIT: {
                    my_dict = {};
                    error_n = 0; 
                    ...
               }

   The ``$INIT`` event appears minus one jiffy before zero time. By default   
   this is -10e-6.

.. describe:: $time

    ``$time`` which provides the current time. It may be used for conditions or
    to measure time spans, etc.

.. describe:: $time_alert

   Inside a rule which is subject to 'awake' and 'sleep' the special variable 
   ``$time_alert`` tells for how long the rule has been awake in a row.

Events can be referred to by their plain name. That is, if there is an event X
sent from test application it can be referred to in the world as X.  That is,
if the test application reports an event::

             0.123: TRIGGER;

then this event can be referred in the world as ``TRIGGER``. An expression of
an event name evaluates to ``true`` only at the exact instance when it occurrs.
It evaluates to ``false`` at any other time.  Adornments to events can either
be accessed by indexing or by name. Example:::

             0.123: TRIGGER(x=12, y=13, label="line");

In the world, the adornments or members of TRIGGER can be accesssed by ``.``
followed by a member name. That is, ``TRIGGER.x``, ``TRIGGER.y``, and
``TRIGGER.label`` result in the contents ``12``, ``13``, and ``"line"``. Any
event X in the database has three special members that can be accessed.

.. describe:: X.time()

   delivers the value of ``$time`` at the moment when the event occurred
   the last time.

.. describe:: X.count()

    gives the number of times that the event 'X' has occurred.

.. describe:: X.time_in_state()

   provides the time in seconds since the last state has been entered.

Events can be raised to have the meaning of *state entries*. This happens by
means of the ``state_machine`` keyword, for example::

    state_machine BED, HOME, WORK;

in TheDude example would define the state entries ``BED``, ``HOME``, and
``WORK``. Once, this is done transition events can be referred. That is::

    WORK->HOME;

referres to the instance in time when ``HOME`` is reported after ``WORK``. The
world does not get confused by other events which do not belong to the state
machine, so that an event list reported as::

             ...
             0.123: WORK;
             0.153: COFFEE_SHOP;
             0.231: GAS_STATION;
             0.712: HOME;
             ...

would still trigger the transition event ``WORK->HOME``, because ``COFFEE_SHOP``
and ``GAS_STATION`` do not belong to the same state machine. Behind the scenes
the ``state_machine`` statement constructs an internal state machine, registers
its admissible states and tracks the state transitions.
