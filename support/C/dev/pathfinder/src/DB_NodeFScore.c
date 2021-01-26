#include <List_NodeP.h>

#include <hwut_graph.h>
#include <malloc.h>
#include <assert.h>

void hwut_memmove(void*, void*, size_t);

void
DB_NodeFScore_construct(T_DB_NodeFScore* me)
{
    me->begin      = (T_Node**)malloc(65536 * sizeof(T_Node*));
    me->end        = me->begin;
    me->memory_end = me->begin + 65536;
}

void
DB_NodeFScore_enter(T_DB_NodeFScore* me, T_Node* NodeP)
{
    T_Node** position = DB_NodeFScore_find(me, NodeP->f_score);

    if( position != me->end ) {
        hwut_memmove(position + 1, position, (me->end - position) * sizeof(T_Node*));
    }
    *position = NodeP;
    ++(me->end);

    assert( me->end <= me->memory_end );
}

T_Node**
DB_NodeFScore_find(T_DB_NodeFScore* me, int F_Score)
    /* Binary search for f-score. Highest f-score is at the end of the list.
     *
     *         begin                                           end
     *         |                                               |
     *        [98  67  44  23  21  20  19  16  15  14  13  12] ::
     *                  |                           |
     *                  lower                       upper                       */
{
    T_Node**  upper    = me->end;
    T_Node**  lower    = me->begin;
    T_Node**  iterator = upper;

    if( upper == lower ) return me->end;

    while( upper > lower + 1 ) {
        iterator = lower + ((size_t)(upper - lower) >> 1);
        if     ( (*iterator)->f_score < F_Score ) upper = iterator;
        else if( (*iterator)->f_score > F_Score ) lower = iterator;
        else { 
            /* iterator->x == X and iterator->y == Y */
            return iterator;
        }
    }
    /* There is only one element left for consideration: 'lower' */
    if( (*lower)->f_score <= F_Score ) return lower;
    else                               return upper;
}

void
DB_NodeFScore_adjust_position(T_DB_NodeFScore* me, T_Node* NodeP, int NewFScore)
/* If the f-score of a node has changed, it needs to be rellocated in the 
 * database, so that the search algorithm can succeed.                     */
{
    const int  OldFScore = NodeP->f_score;
    T_Node**   old_p     = DB_NodeFScore_find(me, OldFScore);
    T_Node**   new_p     = DB_NodeFScore_find(me, NewFScore);
    T_Node**   iterator  = 0x0;

    assert(NewFScore < OldFScore);
    assert(new_p     >= old_p);
    assert(old_p     != me->end );

    iterator = old_p;
    while( *iterator != NodeP ) {
        if( (*iterator)->f_score != OldFScore || iterator == me->begin ) {
            /* If node was not found backwards, it **must** appear forwards, otherwise
             * the database is inconsistent.                                           */
            iterator = old_p;
            do {
                assert( iterator != me->end );
                assert( (*iterator)->f_score == OldFScore );
                ++iterator;
            } while( *iterator != NodeP );
            break;
        }
        --iterator;
    }
     
    /* Assume that the f-score can only get better, if not no update is 
     * to be done.                                                         */
    assert( *iterator == NodeP );
    assert( new_p >= iterator );
    /* The new_p cannot be == begin, because otherwise there would not have
     * been any improvement.                                               */
    assert( new_p != me->begin );

    /* The node_p is to be inserted before the node pointed to by 'new_p'  */
    if( new_p - iterator > 1 ) {
        hwut_memmove(iterator, iterator + 1, (new_p - 1 - iterator) * sizeof(T_Node**));
    }
    *(new_p - 1) = NodeP;
    (*(new_p - 1))->f_score = NewFScore;
}

#include <stdio.h>
#include <hwut_graph.h>

#if 0
void
DB_NodeFScore_print(T_DB_NodeFScore* me, const char* Name)
{
    char          tmp[1024];
    char*         writerator = (char*)tmp;
    T_ScoreInfo*  iterator;

    writerator += snprintf(writerator, 1024, "f_score,g_score,node;");
    for(iterator = me->begin; iterator != me->end; ++iterator) {
        writerator += sprintf(writerator, 
                              "%i,%i,%X;", (*iterator)->f_score, (*iterator)->g_score, 
                              (int)(*iterator)->node_p);
    }

    Table_print(Name, tmp);
}
#endif

