Deterministic Tests
-------------------

*Deterministic tests* in the frame of the HWUT software test are tests where
the output happen in a fixed manner in terms of *what* is printed on the
standard output and *when* it is printed ont the standard output. While
tolerances about the *what* can be implemented effectively with deterministic
tests, tolerance about the sequential order, the *when*, can only be 
tested by means of temporal logic. 

This section discusses the development if tests that judge the output to be
failed if they differ, even only in one character, from the reference output.
In a first subsection, it is discussed how HWUT determines the list of test
applications inside a TEST directory. The second section discusses the 
interaction of HWUT with a test application. 

TODO: Mention TIME-OUT and OVERSIZE and the command line responses that control it!


.. toctree::
   :maxdepth: 3

   test_application_list.rst 
   interview.rst 
   view.rst
   choices.rst 
   comments.rst
