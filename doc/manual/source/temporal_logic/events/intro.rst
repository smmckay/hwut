Events
======

Events are the only thing that the test application communicates to HWUT during
test execution. They inform about what happend, and possibly when and where it
happend. While in classical HWUT tests the user is totally free in the design
of the test application output, the output for events *must* follow a pattern.
The very minimum for an event is the name of the event itself followed by a
semi-colon as shown below.::

     BEGIN;

Time can optionally be reported by a number at the beginning of a line followed
by a colon such as in::

   0.001:  BEGIN;
   0.002:  DATABASE_INIT;
           DATABASE_CLEARED;
   ...

When time is omitted, it is assumed that the event occurred at the same time
when the last time has been reported.

.. admonition:: Time

   Time is unit-less. It's value is a scalar number and it is monotoneously 
   increasing with the number of events.

The source code position may also be reported by a preceeding 
file name followed by a colon followed by a line number. ::

    "hello.c":12:  CALL_STDIO_PRINT;

And, of course, time and source code position may be reported at the 
same time. This is done by specification of the time value after the
source code position as in the example below.::

    "hello.c":12: 0.21:  CALL_STDIO_PRINT;

Events can be adorned, that is additional information which is related to the
event itself. This data can be either provided nameless or named. That is, 
it is possible to write::

   BEGIN("off", 15, 0xFFFF, 192.168.32.1);

or name all arguments::

   BEGIN(light="off", usb_port_n=15, bit_mask=0xFFFF, ip="192.168.32.1");

or even mix named and unnamed arguments::

   BEGIN("off", usb_port_n=15, 0xFFFF, ip="192.168.32.1");

The difference is that named arguments are made accessible in the world by
their names. In the above example, The first and third argument are only
accessed by their index, i.e. by ``BEGIN[0]`` and ``BEGIN[2]``. Named arguments
are accessible by name and index. That is, the ip-address is accessed as
``BEGIN.ip`` *and* ``BEGIN[4]``. 

Returning to the example, a first test written in Perl can be programmed using
``TheDude.pm``.

.. code-block:: perl
  
    use TheDude;

    $joe = TheDude::new();
    for($time=0; $time < 24; ++$time) {
        if( TheDude::on_clock($joe, $time) ) {
            printf("%02i: BUZZ!\n", $time % 24);
        }
        printf("%02i: %s(nfs=%0.1f, w=%s);\n", $time % 24, 
               $joe->{state}, $joe->{need_for_sleep}, $joe->{work_time}); 
    }

This prints the current time and the states of TheDude to the standard output.
Since the need for sleep and the work time are attributes of TheDude, it makes
sense to report them too. 

It is essential to think in terms of events since events are the only thing
reported to the HWUT logic analyzer. The print-out of the state X corresponds
to the event 'one hour passed and state was X'.  The test application above produces
the following content on the standard output.::

    00: BED(nfs=4.0, w=0);
    01: BED(nfs=3.0, w=0);
    ...
    05: BED(nfs=-1.0, w=0);
    06: BUZZ!
    06: HOME(nfs=0.0, w=0);
    07: BUZZ!
    07: WORK(nfs=0.5, w=0);
    08: WORK(nfs=1.5, w=1);
    ...
    15: WORK(nfs=8.5, w=8);
    16: BUZZ!
    16: HOME(nfs=9.5, w=9);
    ...
    19: HOME(nfs=11.0, w=0);
    20: BED(nfs=11.5, w=0);
    ...
    21: BED(nfs=10.5, w=0);
    ...

Some influences of TheDude's behavior is evident. For example, at the buzzing
hours, the ``on_buzz`` handler is called and sets the next state, i.e.  from
``BED`` to ``WORK`` to ``HOME``. When the need for sleep becomes greater than
11, then TheDude goes to ``BED``. But, there are rules whose influence is hard
to oversee. Some of the open questions are: Does TheDude always get enough
sleep?  Does he not leave work too often as a result of tiredness? Does he keep
his minimum and maximum working hours per week? Such constraints can be placed
by temporal logic rules which are explained in the section to come.




