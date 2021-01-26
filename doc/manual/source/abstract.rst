Abstract
========

HWUT is a tool for software tests during the development phases.  The
abbreviation H.W.U.T. stands for 'Hello Worldler's Unit Test'. As the name
insinuates, the program should not demand more knowledge than what is required
in order to get a 'hello world' program to run. It is built on a very simple
principle but its applications span further than many unit test or even system
test tools. HWUT relies on the test programs output and a nominal output. This
way, HWUT is operating system and programming language independent. At the same
time tests can be setup literally in minutes. 

HWUT tests can run in two different modes. The first mode is for strict
*deterministic testing*, where the program under test always produces the same
output. Such tests are written in a very short time and do virtually not
require any preliminaries. The second mode is based on *temporal logic*. It is
appropriate to test in environments where the program behaves not strictly
deterministic, e.g. in multi-threading applications. Such tests require the
user to learn a small language that allows to describe rules for events. In
most practical applications the quick-and-easy deterministic mode is
sufficient.
