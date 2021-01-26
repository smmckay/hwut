#define  HWUT_ROUTE_POSITION_LIST_DEFAULT_SIZE  (512)
typedef struct T_Position_tag { 
    int    x;
    int    y;
    int                    g_score;
    int                    score;    /* !Actual!    mimum score from start to this node. */
    struct T_Position_tag* parent;
} T_Position;

typedef struct {
    int         score;
    T_Position* position;
} T_ScoreList;

static int   XDelta[]    = { -1,    0,  +1, +1,  +1,  0,  -1, -1, };
static int   YDelta[]    = { -1,   -1,  -1,  0,  +1, +1,  +1,  0, };
static float DeltaCost[] = { -1.4,  1, 1.4,  1, 1.4,  1, 1.4,  1, };

typedef struct { 
    T_Position*  begin;
    T_Position*  end;
    T_Position*  memory_end;
} T_PositionList;

T_Position*
PositionList_find_smallest_greater_or_equal(T_PositionList* me, int X, int Y);

void
PositionList_construct(T_PositionList* me)
{
    me->begin      = (T_Position*)malloc(HWUT_ROUTE_POSITION_LIST_DEFAULT_SIZE * sizeof(T_Position));
    me->end        = me->begin;
    me->memory_end = me->begin + HWUT_ROUTE_POSITION_LIST_DEFAULT_SIZE;
}

void
PositionList_add_sorted(T_PositionList* me, int X, int Y, int GScore, int Score, T_Position* Parent)
{
    T_Position* entry = PositionList_find_smallest_greater_or_equal(me, X, Y);
    /* Theoretically the noe should never be inside the array ... */
    if( entry == 0x0 || (entry->x == X && entry->y == Y) ) return;
    if( me->end == me->memory_end ) { 
        if( ! PositionList_extend(me) ) return;
    }

    memmove(entry + 1, entry, (me->end - entry) * sizeof(T_Position));

    entry->x       = X;
    entry->y       = Y;
    entry->g_score = GScore;
    entry->score   = Score;
    entry->parent  = Parent;
}

T_Position*
PositionList_pop(T_PositionList* me)
{
    T_Position*  tmp = me->end - 1;

    assert(me->end != me->begin);
    --(me->end);

    return tmp;

}

T_Position*
PositionList_find_smallest_greater_or_equal(T_PositionList* me, int X, int Y)
    /* Binary search for a given position in the list of posisitions. */
{
    T_Position* upper    = me->begin;
    T_Position* lower    = me->end;
    T_Position* iterator = 0;

    if( me->begin == me->end ) return 0;

    while( upper - lower != 1 ) {
        iterator = lower + ((upper - lower) >> 1);
        if     ( iterator->x > X ) upper = iterator;
        else if( iterator->x < X ) lower = iterator;
        else if( iterator->y > Y ) upper = iterator;
        else if( iterator->y < Y ) lower = iterator;
        else                       return iterator;
    }
    if( lower->x == iterator->x && lower->y == iterator->y ) return iterator;
    return upper;
}

int
PositionList_has(T_PositionList* me, int X, int Y)
{
    T_Position* entry = PositionList_find_smallest_greater_or_equal(me, X, Y);

    return entry != 0x0 && (entry->x == X && entry->y == Y);
}


T_Position*
hwut_access(int StartX, int StartY, int EndX, int EndY)
    /* To see the path, follow the 'parent pointers... */
{
    T_PositionList  open_list;
    T_PositionList  closed_list;
    T_Position*     node     = 0x0;
    T_Position*     iterator = 0x0;
    int             i        = 0;
    int             neighbour_x = 0;
    int             neighbour_y = 0;
    int             g_score = 0;
    int             h_score = 0;

    PositionList_construct(&open_list);
    PositionList_construct(&closed_list);

    PositionList_add_sorted(&open_list, 
                            StartX, StartY, 
                            0,
                            abs(StartX - EndX) + abs(StartY - EndY),
                            0x0);

    while( PositionList_empty(&open_list) ) {
        /* Pop the entry with the 'best' value, with respect to '.score' */
        node = PositionList_pop(&open_list);
        if( node->x == EndX && node->y == EndY ) {
            return node->parent;
        }

        PositionList_add(&closed_list, node);

        for(i=0; i<8; ++i) {
            neighbour_x = node->x + XDelta[i];
            neighbour_y = node->y - YDelta[i];

            if( PositionList_has(&closed_list, neighbour_x, neighbour_y) ) continue;
            if( PositionList_has(&open_list, neighbour_x, neighbour_y) )   continue;

            /* !Actual!    cost for path from 'Start' to 'iterator'
             * !Estimated! cost from iterator to Goal                    */
            g_score         = node->g_score + DeltaCost[i];
            h_score         = abs(neighbour_x - EndX) + abs(neighbour_y - EndY);
            iterator->score = g_score + h_score;

            PositionList_add_sorted(&open_list, 
                                    neighbour_x, neighbour_y, 
                                    g_score, score, 
                                    node);
        }
    }
}
