Generators
==========

The purpose of these modules is to provide generators for users so that they
can iterate over larger set of parameter combinations. The generators are
described very concisely by means of 'selections', 'ranges', and 'focus
ranges'. The heart of every iterator is a 'cursor'. That is is vector of
integers where every element c[i] = 0 ... (N-1) when N is the number of
possible values for parameter 'i'. 

                  cursor
                  .---.
                  | 1 |  c[0] --> take 2nd value of parameter 0
                  +---+ 
                  | 2 |  c[1] --> take 3rd value of parameter 1
                  +---+ 
                  | 0 |  c[2] --> take 1st value of parameter 2
                  +---+
                  | 2 |  c[3] --> take 3rd value of parameter 3
                  '---'

There are three ways how a cursor index can be mapped to a parameter value:

  (1) Selections: c[i] selects the value from a given list for 
                  parameter i.

  (2) Range: parameter i is computed by 'front + c[i] * step_size'.

  (3) Focus Range: parameter i is computed similar to 'Range' but around
                   another parameter or arithmetic expression.

The set of possible combinations of value combinations is given parameterized
by the possible settings of the cursor.
