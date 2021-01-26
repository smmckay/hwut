SEQUENCES:

    [ 1, 2, 3, 4 ] --> fixed order sequence
    < 1, 3, 4, 5 > --> sequence where order needs to be shuffled

    < A, B > generates:

       [ A, B ]
       [ B, A ]

       A  +  B     --> append A and B

     A + <B, C> generates:

       [ A, B, C ]
       [ A, C, B ]
       
       A  x B      --> interleave A and B

     [A, B] x [C, D] generates:

       [A, B, C, D]   # Note, that A is always before B
       [A, C, B, D]   # and C is always before D.
       [A, C, D, B]
       [C, A, B, D]
       [C, A, D, B]
       [C, D, A, B]


EVENT ISNTANTATION:

    A     -- instance / call to 'A'
    A#10  -- generates 10 calls to 'A' where index=0..9;

    [ A#2, B#2 ] generates:

          [ A(0), B(0) ]
          [ A(0), B(1) ] 
          [ A(1), B(0) ]
          [ A(1), B(1) ]

    < A#2, B#2 > generates:

          [ A(0), B(0) ]
          [ A(0), B(1) ] 
          [ A(1), B(0) ]
          [ A(1), B(1) ]
          [ B(0), A(0) ]
          [ B(0), A(1) ] 
          [ B(1), A(0) ]
          [ B(1), A(1) ]


    EXAMPLE:

      [ BOOT INIT <X11 NETWORK HARDDISK> RESET ]
      
      [ CONNECT, SEND, RECEIVE, CLOSE ]
                   x 
      [ CONNECT SEND RECEIVE CLOSE ]

   

       [ACTOR]               [ACTOR2]
          |                     |
      ACTION_1               ACTION_2
      ACTION_1               ACTION_2
      ACTION_1               ACTION_2

       [ACTOR]               [ACTOR2]
          |                     |
        .==.
      ACTION_1               ACTION_2
      ACTION_1               ACTION_2
      ACTION_1               ACTION_2
        '=='
 

/* SEQUENCE:     Fixed sequence, i.e. set of elements with definite order.
 * SEQUENCE_GEN: Something one can iterate through which produces a fixed 
 *               sequence on each step.
 * SELM:         Sequence element.
 * SELM_GEN:     Something that can generate a sequence element. That is, 
 *               there are multiple possible instances of it.
 *
 * Specifications:
 *
 *    { A; B; C; }   --> sequence: order is fixed.
 *    [ A; B; C; ]   --> set:      order is arbitrary --> permutations.
 *
 *    // { A; B; } { D; E; } // --> interleave: iterate over orders
 *                                              of inner elements.
 *
 * On the highest level we have an iterator, which is asked with '.next()' to
 * deliver the next fixed sequence from the set of possible sequences. If it
 * returns 0, all existing fixed sequences must have been iterated through, 
 * and the iteration stops.
 *
 * Sequence Iterator Expression:
 *
 * EXAMPLE: { A; [ B; C; ] } indicates a set of sequences that begin with 'A' 
 *          and end with permutations of 'B' and 'C'. The internal array of 
 *          iterators looks as follows:
 *
 *             [ 0 ] --> { A; } 
 *             [ 1 ] --> [ B; C; ]
 *
 *         The permutation iterator for 'B' and 'C' looks like:
 *
 *             [ 0 ] --> [ B; C; ]
               
 *                                                                          
 * Two types of expression elements: 
 *   
 *   'terminals' are fixed consist of a sequence of events.
 *               next function pointer == NULL
 *   'generators' which describe a set of possible sequences, they are iterated.
 *               next function pointer != NULL
 *
 *
 *
 *                                                                          */
typedef self_interleave_iterator_t {
};

typedef struct self_iterator_t { 
    self_event_id_t* array;
    size_t           max_array_size;

    int              (*next_sequence)(self_expression_element_t* me);
};
typedef struct self_permutation_iterator_t {
    self_expression_element_t base;
    size_t                   *p;
    ptrdiff_t                i;
};
        
typedef struct self_place_iterator_t {
    self_expression_element_t base;
};

typedef struct self_place_iterator_t {
    self_place_iterator_t base;
};

static void
self_interleave_iterator_next_sequence() 
/* Interleave: Distribute the sequences in their order in parallel over the
 * list of 'place in the big row'                                            */
{
    self_iterator_t* it  = &me->it_array[0];
    self_iterator_t* it2 = &me->it_array[0];
    self_iterator_t* End = &me->it_array[me->it_array_size];

    if( self_interleave_next_sequence() ) {
        return 1;
    }
    else if( ! self_instantiate_next_sequence() ) {
        return 0;
    }
    else if( self_interleave_next_sequence() ) {
        return 1;
    }
    else {
        return 0;
    }
    return 0;
} 

static void
self_concatinate_iterator_init() 
{
} 

static void
self_concatinate_iterator_next_sequence() 
{
    if( ! self_instantiate_next_sequence() ) {
        return 0;
    }
    self_concatinate();
    return 0;
} 

static void
self_instantiate_next_sequence()
{
    while( it != End ) {
        if( it->next_sequence == (void*)0 ) {
            ++it;
        }
        else if( it->next_sequence(it) ) {
            return 1;
        }
        else {
            ++it;
            for(it2=Begin; it2 != it; ++it2) {
                if( it2->reset != (void*)0 ) {
                    it2->reset(it2);
                }
            }
        }
    }
    return 0;
}

static void
self_interleave_iterator_next_sequence()
{
    self_selm_t* p = &me->array[0];
    for(it2=Begin; it2 != it; ++it2) {
        self_append(me->array, it2->array, it2->array_size);
    }
    me->array_size = (p - me->array);
}

}

static void
self_concatinate_iterator_next_sequence() 
{
    self_iterator_t* it  = &me->it_array[0];
    self_iterator_t* it2 = &me->it_array[0];
    self_iterator_t* End = &me->it_array[me->it_array_size];

    if( self_instantiate_next_sequence() ) {
        /* Concatinate */
        self_selm_t* p = &me->array[0];
        for(it2=Begin; it2 != it; ++it2) {
            self_append(me->array, it2->array, it2->array_size);
        }
        me->array_size = (p - me->array);
    }
    return 0;
} 
        
/* Permutations.
 *
 * Iteration over possible permutations of a sequence. This implementation
 * relies on 'Heap's Algorithm' in its non-recursive implementation.
 *
 * EXAMPLE: A sequence [A][B][C] has the following permutations:
 *         
 *                     [A][B][C]
 *                     [B][A][C]
 *                     [A][C][B]
 *                     [B][C][A]
 *                     [C][A][B]
 *                     [C][B][A]
 *                                                                           */
static void
self_permutation_iterator_init(self_permutation_iterator_t* me)
{
    me->base.array_size = ArraySize;
    me->base.array      = Array;
    me->base.next_sequence       = self_permutation_iterator_next_sequence;
    for(n = 1; n <= ArraySize; n++) { 
        me->p[n] = 0;  /* Index boundaries. */
    }
    me->i = 1;
}

static void
self_swap(hwut_racer_place_holder_t* array, int i, int j) 
{ 
    int    t = array[i]; 
    array[i] = array[j]; 
    array[j] = t; 
}

static int
self_permutation_iterator_next_sequence(self_iterator_t* alter_ego)
{
    self_permutation_iterator_t*  me = (self_permutation_iterator_t*)alter_ego;
    ptrdiff_t                     j;

    if( me->virginity_f ) {
        me->virginity_f = 0;
        return 1;
    }
    else if( me->i == N ) {
        return 0;
    }
    while( me->i < N) {
        if( p[me->i] < me->i) {
            j = (me->i & 0x1) ? p[i] : 0; // if i odd: j=p[i]; else: j=0;
            self_swap(&me->base.array, j, me->i);
            me->p[me->i]++;     
            me->i = 1;          
            return 1;
        } else {                          // p[i] == i
            me->p[me->i] = 0;       
            me->i++;            
        } 
    } 
    return 0;
}

/* Occupation of places in array with locked position. 
 *
 * Iterate over possible occupations of an array with a sequence. The sequence
 * remains in order. 
 *
 * EXAMPLE: Ordered sequence [A][B][C] distributed over array of five elements. 
 *          The array is drawn vertically, the occupiers given by letters.
 *
 *            [A]  [A]  [A]  [A]  [A]  [A]  [A]  [ ]  [ ]  [ ]  
 *            [B]  [B]  [B]  [ ]  [B]  [ ]  [ ]  [A]  [A]  [ ]  
 *            [C]  [ ]  [ ]  [B]  [ ]  [B]  [ ]  [B]  [ ]  [A]  
 *            [ ]  [C]  [ ]  [C]  [ ]  [ ]  [B]  [ ]  [B]  [B]  
 *            [ ]  [ ]  [C]  [ ]  [C]  [C]  [C]  [C]  [C]  [C]  
 *
 * ALGORITHM:
 *
 * (1) i = highest element in sequence (= sequence[0])
 * (2) Can sequence element 'i' move 'down' 
 *     YES --> position_map[i] += 1; 
 *             all positions below 'i' go back to 'top';
 *             DONE;
 *     NO --> (3)
 * (3) try next lower element;
 *     i == L-1 ? YES --> DONE WITH ITERATION;
 *                NO  --> i += 1;
 *     goto (2)
 *___________________________________________________________________________*/
static void
self_place_iterator_init(self_place_iterator_t*     me, 
                         size_t                     SequenceSize,
                         hwut_racer_place_holder_t* sequence,
                         ptrdiff_t                  position_memory,
                         size_t                     ArraySize)
{
    self_iterator_init(ArraySize, position_memory, self_permutation_iterator_next_sequence);

    me->sequence      = sequence;
    me->sequence_size = SequenceSize;
    me->array_size    = ArraySize;
    me->position_map  = position_memory;
    me->virginity_f   = 1;

    for(i=0; i != SequenceSize; ++i) {
        me->position_map[i] = i;              /* sequence[i] --> position i */
    }
}

static int
self_place_iterator_next_sequence(self_place_iterator_t* me)
{
    self_place_iterator_t*  me = (self_permutation_iterator_t*)alter_ego;
    int i = 0;

    if( me->virginity_f ) {
        me->virginity_f = 0;
        return 1;
    }

    for(i = 0; i != me->sequence_size - 1 ; ++i) {
        if( me->position_map[i] + 1 != me->position_map[i+1] ) {
            ++(me->position_map[i]);
            return 1;
        }
    } 

    return 0;
}

/* Occupation of places in array. 
 *
 * Iterate over possible occupations of an array with a sequence. The sequence
 * remains in order. Some positions may be LOCKED.
 *
 * This algorithm builds upon the 'self_place_iterator_t' algorithm. The free
 * positions in the array are mapped to an entirely free array and this mapping
 * is described by 'free_place_map'.
 *
 * EXAMPLE: 'X' = locked       0  1  2  3  4  5  6  7  8  
 *          array with locks  [ ][ ][X][ ][X][X][ ][ ][ ]
 *
 *                             0  1  2  3  4  5
 *          => free_place_map [0][1][3][6][7][8]
 *
 * The sequence is now distributed over an array of the size of the 'free_place_map'.
 * Now, if a sequence element is placed at position 'i' in the 'free_place_map', it 
 * means that it has to be placed in the locked array at 'free_place_map[i]'. 
 *
 * EXAMPLE: A setting of the free place map with a sequence [A][B][C] as
 *
 *                         0  1  2  3  4  5
 *                        [A][ ][ ][B][ ][C]
 *   
 *          is mapped to a setting in the array with locks by the rules (see above)
 *  
 *                  index 'free_place_map' --> index in locked array
 *                          0              --> 0
 *                          3              --> 6
 *                          5              --> 8
 *
 *          Thus the correspondent setting in the locked array becomes
 *
 *                             0  1  2  3  4  5  6  7  8  
 *          array with locks  [A][ ][X][ ][X][X][B][ ][C]
 *___________________________________________________________________________*/
static void
self_xplace_iterator_init(self_place_iterator_t*     me, 
                          size_t                     SequenceSize,
                          hwut_racer_place_holder_t* sequence,
                          ptrdiff_t                  position_memory,
                          ptrdiff_t                  position_memory2,
                          size_t                     ArraySize, 
                          size_t                     FreePlaceN,
                          ptrdiff_t                  FreePlaceArray)
{
    self_place_iterator_init(&me->base, SequenceSize, sequence, ArraySize);
    me->base.base.next_sequence = self_xplace_iterator_next_sequence;

    me->free_place_n     = FreePlaceN;
    me->free_place_array = FreePlaceArray;
    me->position_map     = position_memory2;
}

static void
self_xplace_iterator_next_sequence(self_place_iterator_t*     me)
{
    self_xplace_iterator_t*  me = (self_permutation_iterator_t*)alter_ego;
    self_place_iterator_next_sequence(&me->base);

    q = &me->position_map[0];
    for(p=&me->base.position_map[0]; p != &me->base.position_map[SequenceSize]; ++p, ++q) {
        *q = me->free_place_array[*p];
    }
} 

