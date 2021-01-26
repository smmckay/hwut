Rules
=====

Rules result in verdicts and trigger changes to the world. Verdicts are a
result of conditions and changes in the world are result of commands. This
section first discusses the syntax of conditions and commands. Rules can be
constraint in different ways by other condition which are discussed in section
XXX. To collect rules in manageable units they can be located in name spaces
which can be frozen and unfrozen. Name spaces are discussed in section YYY.
To write more sophisticated tests HWUT provides data structures such as
dictionaries and lists. The data structures together with functions are
discussed in section ZZZ.

.. admonition:: Condition

   A condition maps the setting of variables of the world to a truth
   value of 'true' or 'false'. 

The syntax of conditions is oriented towards traditional conventions as they
are set by C, Java and the like. That is, the operators ``>`` and ``>=`` stand
for 'greater' and 'greater or equal', ``<`` and ``<=`` represent 'lesser' and
'lesser or equal'. ``==`` stands for 'is equal and ``!=`` stands for not equal.
Conditions can be grouped by the normal brackets ``(`` and ``)``.  Mathematical
operators such as ``+``, ``-``, ``*``, ``/``, and ``%`` (modulo) may be used at
ease.  The binary operators ``<<`` and ``>>`` perform a left and right shift
operation.  ``x**y`` stands for x power y. ``++x`` and ``x++`` pre and post
increment while ``--x`` ``x--`` pre and post decrement.

Not so traditional, is the negation of a condition done by a prefix of ``not``.
Conditions can be combined by the boolean operators ``and`` and ``or``.  An
expression ``A in B``, where ``B`` is a list, is true if and only if ``A`` is
an element of the list. If ``B`` is a dictionary, then the expression is true
if and only if ``A`` is a key into the dictionary. A more deliberate discussion
on lists and dictionaries in a later section.  The ``and``, ``or``, ``not``,
and the ``in`` operator are in the style of Python. 

The following shows a condition that combines some comparison operators in
grouped conditions containing also the ``not`` and ``in`` operators.::

      (x % 2 == 0) or (x in exceptions and not (name in ["Otto", "Fritz]))

An event name by itself means that the event has occurred. 
This condition is true if ``x`` is even (remainder of ``x/2`` = 0), or it is in the
list of exceptions and lesser than ``db_size``. A condition is already a rule and 
produces a verdict of true or false. A single awake rule producing a verdict
of false lets the test fail. 

.. admonition:: Command

   A command sends an event to the world, changes the setting of its variables
   or writes some logging output.

The syntax to send an event, is simple. It requires the keyword ``send``
followed by the event description as explained in the previous section. For 
example::

        send BUTTON(state="up", color="red");

sends an event called ``BUTTON`` along with its state variables ``state`` set
to 'up' and ``color`` set to 'red'. Another useful command is the ``print``
command. By means of this command additional information may be printed 
which may help to analyze why certain rules triggered or how they derived
their verdict. For example::

        print "slept_hour_n = ", slept_hour_n

will print the term ``slept_hour_n`` together with its value and a terminating
``!`` to the trace, such as

    ...
    53.000: << slept_hour_n = 4! >>
    ...

The ``print`` function cannot handle format strings. It is kept rather simple.
Its purpose is to support debugging by the display of values which may be relevant
to rules.

Scalar variables may be set or modified by the assignment operator ``=`` or its
variants ``+=``, ``-=``, ``*=``, ``/=``, ``<<=`` assign left shifted, ``>>=``
assign right shifted, ``&=`` for assign logical and, ``|=`` for assign logical
or, and ``^=`` assign logical exclusive or. The following fragment shows some
examples.::

        x     = 0;
        y    += y + (0x21 << 1);
        speed = acceleration * (t**2);

Let us now define a first couple of rules for TheDude. For that, some syntax
knowledge is pre-fetched, while its detailed discussion follows in later
chapters. First, by using ``on`` we can constrain rules to the moment 
when an event occurs. Second, with ``once`` rules can be constraint to 
the moment when a condition becomes true. The ``if`` keyword signalizes
an *implication*. That is, its consequences are executed if and only if its
condition is true.

Let us assume, that TheDude should work at least five but never more than nine
hours.  His work place is only open from 7am to 5pm. Thus, TheDude shall not be
in the state of ``WORK`` beyond these hours. We define::

        on WORK: {
            WORK.w >= 5 and WORK.w <= 9;              # work 5 to 9 hours    
            ($time % 24 >= 7) and ($time % 24 <= 17); # office open: 7am-5pm 
        }

The curly brackets define a list of conditions. Since it follows ``on WORK:``
it  is only evaluated at the moment when the event ``WORK`` appears. Then, this
fragment checks whether the accumulated amount of work complies to its limits and 
if the global time is in the borders of the office time. The ``%`` operator is
used to get the time in the frame of one day. Let us now specify that TheDude
shall sleep at least 5 hours each night.::

       once $time % 24 > 7: {       # Night is over.              
           print "7o'clock: slept_hour_n = ", slept_hour_n, ";";
           slept_hour_n >= 6;       # He must have slept 5 hours. 
           slept_hour_n  = 0;       # Reset                       
       }

       once $time % 6 == 0:
          # Every six hours print the day time.                    
          print "Day time = ", $time % 24, ";";

       on BED: 
            if ($time % 24 > 20) or ($time % 24 < 7):    # Night   
                slept_hour_n += 1;

That is, when it is seven o'clock in the morning, we check whether five hours
of sleep have been accumulated.  During the night, from 8pm to 7pm in the
morning each hour the ``slept_hour_n`` is incremented by one when TheDude is in
``BED``. 

Rules are totally independent of the programming language of the unit under
test. It is HWUT's own little language to describe temporal logic rules.
Assumed that the former rules are stored in ``dude.tlr`` (extension '.tlr'
for temporal logic rules) the first HWUT test file can be finalized.  The
example usage program must be extended with a response to ``--hwut-info`` as a
command line argument. The Perl test program becomes

.. code-block:: perl

    #! /usr/bin/env perl
    use TheDude;

    if( "--hwut-info" == shift ) {
        printf("TheDude: Temporal Logic Tests;\n");
        printf("LOGIC:   dude.tlr;\n");
        exit;
    }

    $joe = TheDude::new();
    for($time=0; $time < 1000; ++$time) {
        if( TheDude::on_clock($joe, $time) ) {
            printf("%02i: BUZZ!\n", $time % 24);
        }
        printf("%02i: %s(nfs=%0.1f, w=%s);\n", $time % 24, 
               $joe->{state}, $joe->{need_for_sleep}, $joe->{work_time}); 
    }

If the test is stored in ``test.pl``, a call on the command line

    > hwut ld test.pl

lets HWUT perform its temporal logic test and display the traces on the
screen. The above example, delivers::

    0.000000: BED(nfs=4.0, w=0.0)
    0.000000: << Day time = 0.0; slept_hour_n = 1.0; >>
    1.000000: BED(nfs=3.0, w=0.0)
    2.000000: BED(nfs=2.0, w=0.0)
    3.000000: BED(nfs=1.0, w=0.0)
    4.000000: BED(nfs=0.0, w=0.0)
    5.000000: BED(nfs=-1.0, w=0.0)
    6.000000: BUZZ
    6.000000: << Day time = 6.0; slept_hour_n = 6.0; >>
    6.000000: HOME(nfs=0.0, w=0.0)
    7.000000: BUZZ
    7.000000: << 7'oclock: slept_hour_n = 6.0; >>
    7.000000: WORK(nfs=0.5, w=0.0)
    8.000000: WORK(nfs=1.5, w=1.0)
    ...

With the current rule set no errors appear. Adding the constraint that at 
work the need for sleep shall not be greater than 9, i.e.::

    on WORK:
        WORK.nfs < 9;

results in a broken rules which is then reported in the trace::

    ...
    35.000000: WORK(nfs=6.0, w=4.0)
    36.000000: WORK(nfs=7.0, w=5.0)
    36.000000: << Day time = 12.0; slept_hour_n = 0.0; >>
    37.000000: WORK(nfs=8.0, w=6.0)
    38.000000: WORK(nfs=9.0, w=7.0)
    dude.tlr:14: rule broken.
    OUT/test.pl.txt:44: at this point.
    ...

HWUT reports the location of the broken rule in a 'gcc' compiler output format,
so that editors can jump onto it by a click and/or a push of return. Further,
it documents that the error occured at line 44 of the list of events.



