
#include <List_NodeP.h>

#include <assert.h>
#include <string.h>
#include <hwut_scanner.h>
#include <hwut_graph.h>


void
DB_NodeXY_construct(T_DB_NodeXY* me)
{
    me->begin      = (T_Node**)hwut_malloc(65536 * sizeof(T_Node*));
    me->end        = me->begin;
    me->memory_end = me->begin + 65536;

    hwut_memset((void*)me->end, 0x0, (65536) * sizeof(T_Node*));
}

void
DB_NodeXY_enter(T_DB_NodeXY* me, T_Node* NodeP)
{
    T_Node** position = DB_NodeXY_find(me, NodeP->x, NodeP->y);

    assert(me->end != me->memory_end);

    hwut_memmove(position + 1, position, (me->end - position) * sizeof(T_Node));

    *position = NodeP;

    ++(me->end);
}

void
DB_NodeXY_remove(T_DB_NodeXY* me, T_Node** Position) 
{
    assert(Position >= me->begin && Position < me->end);

    if( Position != me->end - 1 ) {
        memmove(Position, Position + 1, (me->end - Position - 1) * sizeof(T_Node*));
    }
    --(me->end);
    hwut_memset((void*)me->end, 0x0, sizeof(T_Node*));
}

#if 0
T_Node*
DB_NodeXY_move_pointer(T_DB_NodeXY* source, T_DB_NodeXY* drain, T_Node** node_pp)
{
    T_Node* result = 0x0; 

    assert(source->begin <= node_pp && source->end > node_pp);

    DB_NodeXY_enter(drain, *node_pp);
    DB_NodeXY_remove_pointer(source, node_pp);

    return result;
}
#endif

T_Node**
DB_NodeXY_find(T_DB_NodeXY* me, int X, int Y)
{
    T_Node**  upper    = me->end;
    T_Node**  lower    = me->begin;
    T_Node**  iterator = upper;

    if( upper == lower ) return upper;

    while( upper > lower + 1 ) {
        iterator = lower + ((size_t)(upper - lower) >> 1);
        if     ( (*iterator)->x > X )     upper = iterator;
        else if( (*iterator)->x < X )     lower = iterator;
        else { 
            /* (*iterator)->x == X */
            if     ( (*iterator)->y > Y ) upper = iterator;
            else if( (*iterator)->y < Y ) lower = iterator;
            else { 
                /* (*iterator)->x == X and (*iterator)->y == Y */
                return iterator;
            }
        }
    }
    /* There is only one element left for consideration: 'lower' */
    if     ( (*lower)->x > X ) return lower;
    else if( (*lower)->x < X ) return upper;
    else { 
        if( (*lower)->y >= Y ) return lower;
        else                   return upper;
    }

}

int 
DB_NodeXY_has(T_DB_NodeXY* me, int X, int Y)
{
    T_Node**  result = DB_NodeXY_find(me, X, Y);
    if( result == me->end ) return 0;
    return (*result)->x == X && (*result)->y == Y;
}

#include <stdio.h>

void
DB_NodeXY_get_display_string(T_DB_NodeXY* me, char* tmp, size_t ByteN)
{
    T_Node** iterator = 0x0;
    char* writerator  = (char*)tmp;

    writerator += snprintf(writerator, 1024, "idx,x,y,f_score,g_score;");
    for(iterator = me->begin; iterator != me->end; ++iterator) {
        writerator += sprintf(writerator, "%i,%i,%i,%i,%i;", 
                              (int)(iterator - me->begin),
                              (int)((*iterator)->x),       (int)((*iterator)->y), 
                              (int)((*iterator)->f_score), (int)((*iterator)->g_score)); 
        if( writerator - tmp > 65536 - 128 ) break;
    }
}
