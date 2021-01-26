Comments and Code
=================

The task of a test is to provide a reliable statement about the robustness and
quality of the unit under test. The reliability of a statement depends on the
trust that one puts in a test. Trust can only emerge where there is
understanding or daze. Understanding as a source of trust does not require
physical intoxicants. So, it has less dependencies and is therefore a
preferable over daze. A key to understanding code are comments. In that sense,
comments are directly linked to test reliability. Comments are essential for the
test to fulfill its purpose. It therefore, makes sense to give comments a high
priority during the testing efforts.

Comments are written in human languages and are not bound to formalism. This
freedom can be used for good and bad. In comments all vocabulary, metaphors,
idioms, poetry and ASCII drawings may be presented to express ideas concisely.
The same linguistic means may be used very efficiently to confuse the reader.
The measure of badness for a comment is the amount of effort required to
understand the test. The value of badness ranges from zero, where things are
immediately clear, to infinity, where the reader is left without any chance at
all.

The initial comment, i.e. the comment located at the head of a test file 
shall focus on the following questions--and not more:

  * What is tested? If its a function, then what does the function do? If its
    a scenario, what happens in the scenario? 

  * What does the test? What inputs are considered? What outputs are 
    observed? What consistency constraints are imposed?

  * Why does the author think that the test is sufficient?

Focussing solely on those three questions protects against causing confusion.
One might review and rewrite the comment a couple of times to make it really
crystal clear.  The end of the initial comment shall be visually clearly
marked, such as by a dashed line, for example. The visual mark signalizes to
the reader that he has only to read until that point to get the essential idea.
There might be more text and poetry following for those who would like to hack
the code or enjoy some fine arts. 

The most adorable comments, though, have little value if they are followed by
chaotic test code. The structure of the test code, again, is best designed with
the test's overall goal in mind: to be reliable. A test verdict is reliable if
there can be no more surprises once all tests have been accomplished. Anything
that influences the functioning must be under control of the test. Any output
of the functioning must be observed, i.e. printed on the standard output. To
support clarity on these issues three types of functions should be in place:

    *  A setup function that makes the test independent from any history
       or external influences.

    *  Stimulating input functions which trigger the functioning of the
       unit.

    *  Print-out functions which print the state of a unit or outputs
       from a test.

    *  A test function which applies inputs and prints outputs.

It is good practise, to name each type of function with a suggestive prefix.
A print function may be prefixed by ``my_print_...`` for example.

With these few basics in mind it is possible to write tests that can be
understood and relied upon. Also, a clear and transparent structure as
mentioned above facilitates the task of reviews and modifications.

