Generators
----------

Generators generate test cases, or instructions that control the flow of a test
experiment. The goal is to cover a large test space by strategic permutations
(*iterators*), walks along paths of a state machine (*sm-walker*), or by
constructing scenarios for racing conditions (*racer*). The actual tests are
performed based on tiny engines written in the test's native language.  Those
engines are fed with data that HWUT provides based on a formal description of
the test space. The brief formal test descriptions are at the same time 
redundancy free expressions of a large test space. The brievity of these
expressions support the transparancy of test descriptions. 

.. note:: 

   When tests expand in larger space

      don't bother writting all by hand.

   With generators right in place

      a smart line hoses all dry land.
    
The following three chapters describe the generator types: 'iterator',
'sm-walker', and 'racer'. They explain their principal ideas and provide 
some basic usage examples.


.. toctree::
   :maxdepth: 2

   iterator.rst
   sm_walker.rst
   racer.rst
