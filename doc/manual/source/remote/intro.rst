Remote Testing
==============

Software is not always run on the system where it is developped. Many factors
may influence the software that is to be run on another target.  In order to
test software on systems that are not the test computer HWUT provides the
ability of 'remote testing'. In this type of test, the test application is run
on a remote platform and communicates with HWUT over a communication protocol
(currently only TCP is supported).  Let the following terms be defined for
clarification:

.. describe:: Host

   The 'host' is the computer on which HWUT runs.

.. describe:: Target

   The 'target' is the platform on which the tests shall be executed.

The target needs to contain the following two entities: 

.. describe:: Agent

   An 'agent' is a piece of software on the target that can receive and 
   execute commands coming from the host. 

.. describe:: Spy 

   A 'spy' has the task to send test application results to the host.

A remote test follows the scheme of normal tests. However, instead of executing
the application in a system call it sends commands to the remote agent. The
commands are the same as the command line arguments passed to test applications
during non-remote tests, i.e. it would send the ASCII character sequence
of "--hwut-info" to the agent in order to get information about the test itself.
The test application answers by using the spy that is able to connect to the
listener on the host and send it the output of the test. This data is the basis
for comparison.

Before this can be done the application needs to be transferred to the remote
platform. All mechanisms of building, transfer and test execution are
controlled by HWUT.  Figure :ref:`fig-remote-testing` shows the interactions to
implement remote tests.

The first step is the build and transfer process. As in non-remote tests the
test application needs to appear in the test returned by the ``hwut-info``
target in the Makefile. Next the build rule for the remote application must
include the build of the test application, the transfer of the test application
to the target, and if necessary the start of the listener on the the target
side. For example

.. code-block:: make

   my_remoty: $(SOURCES)
        # Compile all related sources
        $(CROSS_COMPILER) $(SOURCES) $(HWUT_PATH)/support/remote/hwut_spy.c  -o my_remoty

        # Transfer the application to the target device
        ./my_target-transfer.sh my_remotey  

        # Start our listener on the target
        ./my_target-start_listener.sh
   
Now, HWUT needs to know how to communicate with the target. For this, two it
interviews the make rule ``hwut-remote`` and expects a string that specifies
the spy and the agent on the remote target, e.g.

.. code-block:: make

    hwut-remote:
        @echo "SPY:   TCP;"
        @echo "AGENT: TCP, Adr=192.168.1.11, Path=/host/;"

specifies that both spy and agent on the target communicate over the TCP
protocol. This will activate a special plug-in inside HWUT. After the protocol
specifier a list of assigned parameters can be specified. The following
parameters are valid for all protocols: 

.. describe:: Path

    This parameter defines the path to be prefixed for the remote execution.
    It influences the string that is sent to the target to trigger the 
    test application execution--as will be explained below. This parameter
    makes only sense for the agent.

.. describe:: Terminator

    This string determines what string terminates the report from the spy.
    As soon as the string appears, HWUT considers the test to be terminated.
    The default string is ``<<end>>``. This parameter makes only sense 
    for the spy.
    
Once the test application is built, transferred to the target, and the
communication is set up the tests can be started. This happens by sending
a string to the target. The string send to the target is the same as the
string that would otherwise be applied to the command line, i.e::

       /host/my_remote --hwut-info

will be sent in order to get information about the test, provided that ``Path``
in the above agent parameters was set to ``/host/``. Now, the test application
may respond via the spy with::

       My Remote Application Test;
       CHOICES: None, Some, All;

This is the information that HWUT requires to define the test sequence. It then
sends:: 

       /host/my_remote None

and receives the response from the remote spy, for example::

       This is some test output from IP address 192.168.1.11.
       No input, No output. Test ended.
       <<end>>
  
This response needs to terminate with the a terminating string. As mentioned
above the default string that HWUT expects is ``<<end>>`` but is can be 
modified with the parameter ``Terminator`` for the spy. Once, this string
has been received HWUT compares the accumulated strings that it received
from the target agains the nominal output in the GOOD directory.

TCP Parameters
--------------

.. describe:: Adr

   For the agent this specifies the IP Address of the network node, where it
   resided. For the agent, the specification is mandatory. For the spy it
   specifies the IP Address where HWUT resides and receives messages. The
   spy does not need to specify this, since HWUT listens on all of its 
   interfaces.

.. describe:: Port

   For the agent, it is the port where it receives its commands. For the spy
   it is the port on the host to where it sends its data. By default 
   HWUT uses port number 37773 for both.




