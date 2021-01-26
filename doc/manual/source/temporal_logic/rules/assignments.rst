Assignments
===========

Assignments are intended to provide a means for abbreviations of numeric
terms. Assignments assign a numeric term to a variable. Variable names
in HWUT's temporal logic engine start with a \$ sign and consist of 
a sequence of letters and possibly underscore. Assignments can contain
other variables and even the name of the variable itself. Assignments
can be used to 

- clarify the program code,
- minimize typing efforts, and to
- store attribute values and management information.

For example the code fragment:

.. code-block:: perl

    START => { 
        $error_n          = 0;
        $first_start_time = START.time;
    }

    from START to END : {
        ERROR => $error_n = $error_n + 1;

        $time_delta  = $1 - START.time;
        $error_ratio = $error_n / $time_delta;

        $error_ratio < 13.5;
        
        if $1 > $first_start_time then not START;
    }


The variable `$error_n` shall count the number of errors from the moment that
`START` arrives to the moment that `END` arrives. The event `ERROR` could
theoretically also arrive before `START` so `EVENT.count` is not appropriate.
The implicit rule based on the `START` event, though, resets the error counter
as soon as it arrives. Then, when the rule is awake, the error counter is
incremented with any occurence of the `ERROR` event. Now, using the two
variables `$time_delta` and `$error_ratio` allows to describe the underlying
thought briefly and clear: there shall not be more than 13 errors per second
from the `START` to the `END` event.  The variable `$first_start_time` helps to
prevent that a `START` event occurs twice or more before the `END` event. The
last code line in the example says: for any time \$1 that is greater than the
time where `START` appears first, there shall not occur another `START` event.
