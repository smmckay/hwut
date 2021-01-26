HWUT's way of looking at things
===============================

HWUT's decision of a test being 'OK' or 'FAIL' depends on a textual comparison
of output that a test application delivers with a nominal text. The nominal
text has been stored some time earlier when the application was considered
functional. 

Textual comparisons are very strict. A slight change from Unix newlines 0x0A
to DOS newlines 0x0D, 0x0A already breaks a plain textual comparison. Similar
things such as one additional whitespace or tabulator are equally prone to
break strict equality while the semantics would still fit. Fortunately, 
HWUT is not that strict. 

.. note::

   | The smallest tiniest deviation 
   |
   |  might bring a hyperventilation. 
   |
   | Wherelse, you calmy hibernate 
   |
   |  if you know what you tolerate. 

HWUT's way of looking at things lets the user control the level of 
tolerance. By this means, the effort to adapt unit tests upon software 
changes and platform migrations shall be omitted or at least minimalized.
The 'cockpit' of tolerance control is composed of several easy-peasy concepts.
The subsequent sections explain how they work and how they are supposed to
be applied.

Empty Lines, Whitespace, and Slashes
####################################

Any empty line appearing in the output is treated as if it was not there.  It
is not subject to comparison. Newlines of the DOS style are internally
transformed (0x0D, 0x0A) into newlines of the Unix style (0x0A). Thus, both are
equivalent. Tabulators (0x09) are replaced by a single space (0x20). Any number
of adjacent spaces are replaced by a single space. Whitespace at the beginning
of a line and the end of the line is omitted. 

As a result, the following two texts are equal in the way that HWUT is looking
at things. The two types of newlines are made visible by ``\n`` (0x0A) and 
``\r\n`` (0x0D, 0x0A). Tabulators are represented by ``\t``. 

First: ::

    The Cro-Magnons\tshared the European landscape\r\n
    \n
       with Neanderthals for 10,000 years.  \n

Second: ::

    The Cro-Magnons shared  the  European landscape\n
    with    Neanderthals    for    10,000    years.\n


Whitespace shrinking can be disabled using response options. When ``NO-SHRINK;``
is responded whitespace shrinking is totally disabled. With ``NO-SHRINK-SPACE;``
the shrinking of spaces and tabulators is disabled. With ``NO-SHRINK-EL;`` the
shrinking of empty lines is disabled.

The differing file path format on different operating systems may cause a major
inconvenience. If tests output filenames, then the path string may look
differently depending on the platform where the test is run. To avoid nuisance,
HWUT treats backslashes ``\\`` and slashes ``/`` the same.  Further, ``./``,
but not ``../`` is equal to the empty string. The multi-slash such as ``//`` is
treated as a single ``/``.  In that sense, the following two outputs are the
same. 

First: ::

         Found something at './data/field///test.c' line 12.

Second: ::

         Found something at 'data\field\test.c' line 12.


If this is not desired the option 'NO-BACKSLASH-IS-SLASH' must be defined.

Comments
########

Comments which are not subject to the test but explain the output may be
specified in 'comments'. A 'comment' is a line that starts with ``##`` or ends
with ``##``. Such lines are ignored and not subject to comparison. Example: ::

    ## Algo determines human species'names, shared content,\n
    ## and the amount of time they were living together.\n
    The Cro-Magnons shared the Antartica landscape\n
    with Grimaldi Men for 21 seconds.\n
    \n
    12 March, 2014 -- state of science.##\n

The above output might cause a FAIL message--most likely. But the lines
starting or ending with ``##`` are not the reason.

Analogies
#########

Sometimes, the change of things cannot be controlled. By means of analogies
HWUT can still check whether the changes happen consistently. For example, the
exact address of a pointer, a process id of an observer application, time
stamps, and the like are candidates for analogies. The following,
fragment defines an analogy::

                         ((Fritz))

Each analogy must match consistently with the same counterpart. So, if an
analogy ``((Fritz))`` was matched with ``((Kermit))`` then it must
do so for all occurencies. Consider the following two fragments which are
considered equal in the way that HWUT is looking at things.

First: ::

    Einst wandelte ((Heidi)) mit ihrem Ehegatten ((Fritz)) durch 
    die sonnigen Gaerten von ((Pforzheim)). Da kam ein ((Drache)) und frass
    ((Fritz)) und ((Heidi)) und die ganze Stadt ((Pforzheim)) schaute zu.

Second: ::

    Einst wandelte ((Peggy)) mit ihrem Ehegatten ((Kermit)) durch 
    die sonnigen Gaerten von ((Bronx)). Da kam ein ((Storch)) und frass 
    ((Kermit)) und ((Peggy)) und die ganze Stadt ((Bronx)) schaute zu.

Both fragments are equal, because ``Peggy`` is a consistent analogy for
``Heidi``, ``Kermit`` consistently appears instead of ``Fritz``, and ``Bronx``
consistently appears in the place of ``Pforzheim``. The analogy ``Drache``
appears only once. It does not impose any constraints.  Since it appears only
once it acts like a wildcard. 

Analogies not only support fairy tails. In real-world applications, pointers
into memory are, for example, depend on the underlying memory allocation
system. While precise values of pointers may change each time an application is
executed, the role of each remains the same. A list of pointers may be built
sequentially and finally all pointers must be present in the list.::

         added: ((0x80FE2123))
         added: ((0x80FE3831))
         added: ((0x80FE3781))
         added: ((0x80FE2654))

         list content: ((0x80FE2654))
                       ((0x80FE3781))
                       ((0x80FE3831))
                       ((0x80FE2123))

In this example, the concrete value of a pointer is unimportant. It is
verified, however, that is appears consistently. The shape of analogies can be
defined by the user in response options to ``--hwut-info``. If a python 
script responds the following manner.

Analogies are by default bracketted in ``((`` and ``))`` markers. The response
option ``ANALOGY`` allows the user to define a customized brackets. Firt the
opening bracket, then the closing bracket is to be specified. Example in
Python:

.. code-block:: Python

   ...
   if "--hwut-info" in sys.argv:
        print "This is my test;"
        print "ANALOGY:  <<, >>;"

The above example specifies ``<<`` for the opener of an analogy and ``>>`` as a
closer. 

Happy Patterns
##############

Sometimes, the precise shape of things cannot be determined but their outline
can. Fuzzy outlines can be caught by *happy patterns*. A happy pattern that
matches in a line requires only that the counterpart matches at the same
position. It is no longer required that the line matches strictly.  Those
patterns are called 'happy patterns' because two lines which might trigger a
*FAIL* due to their textual differences, might actually be *OK* because they
matched a happy pattern.

Example: A test procedure supervises searches for the appearance of some macros
in source code. The content of the lines is known, but the line numbers are
subject to frequent change. Such an output might look as follows. ::

    simple.c:312: #define GROMBORZ_OPTION_FLOAT true
    main.c:12:    #define GROMBORZ_OPTION_FLOAT false
    control.c:62: #define GROMBORZ_OPTION_FLOAT true

At some point later in time, the output might look like::

    simple.c:331: #define GROMBORZ_OPTION_FLOAT true
    main.c:12:    #define GROMBORZ_OPTION_FLOAT false
    control.c:65: #define GROMBORZ_OPTION_FLOAT true

because some people edited the files ``simepl.c`` and ``control.c``. The output
is still totally *OK*, but a textual comparison would fail. Using a happy pattern
such as the following helps. ::

              .c:[0-9]+:

This pattern matches an extension '.c', followed by a number in colons. If a
pattern matches in the good file's line at a position x, then it must match the
output file's line at the same position x.  But, it does not have to be
textually the same. 

With the happy pattern defined, the second output is *OK*.  ``.c:331:``
appears in the place of ``.c:312:`` and matches the happy pattern. Also,
the matching ``.c:65:`` appears in the place of ``.c:62:``. 

If the values of ``true`` and ``false`` are equally subject to change but not 
subject to test, then another happy pattern makes the test even more
robust. ::

               (true|false)$

The dollar sign at the end tells that the pattern must match at the end of a line. Now,
even the following output is considered to match the first.::

    simple.c:331: #define GROMBORZ_OPTION_FLOAT false
    main.c:12:    #define GROMBORZ_OPTION_FLOAT true
    control.c:65: #define GROMBORZ_OPTION_FLOAT false

Whenever ``false`` or ``true`` appears at the end of the line they differ from
the original. But they match a happy pattern, and thus each line is fine. 

.. note:: Happy Pattern Interference

    Some patterns sparkle happyness, 
 
    while hords of them can cause a mess. 

    What words may mean might not be clear, 

    if too much patterns interfere.

Multiple happy patterns may appear in a single line. But there is danger of
*interference*. In such cases, patterns must be defined carefully, so that they
cannot interfere.  Staying with the previous example, a file name pattern can
be defined::

                      [a-z]+.c 

and a pattern to appear some later in a line::

                      true|false

Both are prone to interfere. An output line::

    obstruent.c:4711: #define GROMBORZ_OPTION_FLOAT true 

triggers a *FAIL* event. This is so, since the file name ``obstruent.c``
contains ``true`` as a substring. Since it does not appear in the position of
the other ``true`` it fails. Using line and word boundaries and concentrating
on the element of change are key strategies to avoid interference. Defining the
latter pattern as::

                      \b(true|false)\b

i.e. requiring word boundaries arround the boolean expressions avoids such
interference.  The ``^`` requiring the beginning of a line and ``$`` requiring
the end of a line are equally good candidates to rescue.
    
Happy patterns are defined has response options by means of the ``HAPPY`` keyword.
For example, a bash script requires the happy patterns ``.c:[0-9]+:`` and 
``(true|false)$`` the following way 

.. code-block:: bash

    if [ "--hwut-info"="$1" ]; then
        echo "My Test;"
        echo "HAPPY: .c:[0-9]+:;"
        echo "HAPPY: (true|false)$;"
    fi

The semi-colon is a delimter for response options. If it is supposed to appear
in happy patterns, than it must be preceeded by a backslash, i.e. it is specified
as ``\;``.

Potpourri
#########

In situations where the sequence of things can hardly be determined the
potpourri feature comes to rescue. If a list of lines is framed by ``||||`` and
``||||`` markers, then its particular sequence is unimportant.

Consider, for example, a simple implementation of a name container in absence of
a sort function. All that can be said is that certain names shall
be there. It is likely that the internal representation may change and
therefore the sequence might change. A *potpourri* region can now be used to
implement a test which checks only for the presence of a set of names but not
for the sequence. The following two outputs are considered equal.

First: ::

    Name List:
    ||||
        Don Quichote.
        Alfred the Great.
        Edward the Elder.
        Otto Walkes.
        Walter von der Vogelweide.
    ||||


Second: ::

    Name List:
    ||||
        Walter von der Vogelweide.
        Alfred the Great.
        Otto Walkes.
        Edward the Elder.
        Don Quichote.
    ||||


Note, that analogies have no matching effect inside potpourri sections.

.. note:: No Analogies and Potpourri

    The wise man does not try to see
  
    analogies in potpourri. 

Blocks which are supposed to belong together can either be built using 
the ``----`` markers for begin and end. The following two definitions are
equivalent as in the following example::

    Name List:
    ||||
    ----
        Alfred the Great. 
        Edward the Elder.
    ----
    ----
        Walter von der Vogelweide.
        Otto Walkes.
        Don Quichote.
    ----
    ||||


Summary
#######

HWUT's view on things is much smarter than pure textual comparison.

.. describe:: NO-SHRINK;

.. describe:: NO-BACKSLASH-IS-SLASH;

.. describe:: NO-SHRINK-SPACE;

.. describe:: NO-SHRINK-EL;

.. describe:: HAPPY:   pattern;

.. describe:: ANALOGY: open, close;

.. describe:: NO-ANALOGY;

.. describe:: NO-TIME-OUT;  ... must be documented also.


.. describe:: NO-POTPOURRI;
