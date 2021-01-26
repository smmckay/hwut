Formal Description
==================

This section discusses the precise format of events as they have to be printed
by the test application. As mentioned earlier, only lines that start with
`>>>>` are considered by the temporal logic engine. A `statement` a test
application is a notification that one or more events occured. The only thing
that a test application has to do is to print such statements to the standard
output. Statements consists of two parts

Origin::

  The test application can tell in what file and what line the event happend.
  Additionally, it can report about the time of the occurence.

Event description::

  In the simplest case, this consist of a single name, i.e. the name of the 
  event. Additionally, the event can be adorned with attributes in brackets.
  Multiple events can be spefied for one single origin.

Any statement must be terminated by a semi-colon, except that it contains an
event list which is explained downwards.  A position in the source code is to
be specified with a string in quotes, followed by a colon, a number, and a
colon. If it is desired to specify a time, it has to be followed by a floating
point number indicating the current time in seconds. If it is not desired to
specify a source code position, just the time is to be mentioned.  Origin
specifications do not necessarily have to be followed by event descriptions.

.. code-block:: cpp

    >>>> "hello.c":10: 0.45;         # source code position and time [sec].
    >>>> "hello.c":21;               # only source code position.
    >>>> 1.25;                       # only time [sec].

Any event following an origin is considered to be originated from the given source
code position and happening at the given time. The simplest event description
is a name consisting out of a sequence of characters including the `_` underscore
sign. An event name can be followed by attributes in brackets. If more than
one attribute is mentioned, they need to be separated by commas. Attributes can 
be either named or unnamed. A named attribute consists of a name followed
by a `=` sign and a value that the attribute shall take. Note, that events
do not necessarily be prefixed by origins. The following shows examples
for events:

.. code-block:: cpp

    >>>> START;
    >>>> MAIN(5, "--run", "--crc", mode=34);

Events that occur without an origin are related to the last origin that has
been specified.  Events, though, can be specified together with origins. In
this case the origin needs to be followed by a colon. The following shows
examples where origins and events appear together in one statement:

.. code-block:: cpp

    >>>> "hello.c":10: 0.45 : PRINT("hello");   
    >>>> "hello.c":21       : PRINT("world");              
    >>>> 1.25                 EXIT;               

Events can be combined to event lists by bracketting via curly backets. The output
of a test application like this

.. code-block:: cpp

    >>>> "hello.c":10: 0.72 : { PRINT("Who are you?\n"); 
    >>>>                        USER_INPUT("Bill"); 
    >>>>                        PRINT("Hello Bill"); }

notifies the temporal logic engine that the two PRINT events and the user
interaction happened at time 0.72 seconds in line 10 of file `hello.c`. The only 
command remaining to be explained is the `log` command. It is followed by 
numeric expressions which are explained in detail in the section about rules.



