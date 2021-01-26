#include <hwut_graph.h>
#include <hwut_path.h>
#include <List_NodeP.h>
#include <DB_OpenNode.h>

#include <assert.h>
#include <string.h>
#include <malloc.h>

                     
static void
__get_next_neighbour_node_db_direction_index(int DirectionIndex, int* x, int* y)
    /*     5 6 7 
     *     4   0 
     *     3 2 1    */
{
    /* Assume, that *x and *y point to the position right to the center when 
     * DirectionIndex == 0 */
    switch( DirectionIndex ) {
        /* case 0: --(*x); return; */
        case 1: --(*y); return;
        case 2: --(*x); return;
        case 3: --(*x); return;
        case 4: ++(*y); return;
        case 5: ++(*y); return;
        case 6: ++(*x); return;
        case 7: ++(*x); return;
    }
}

static int
__compute_h(int X, int Y, int GoalX, int GoalY) 
{
    int DeltaX = GoalX - X;
    int DeltaY = GoalY - Y;

    return DeltaX * DeltaX + DeltaY * DeltaY;
}

void
Path_construct(T_DB_NodeXY*  closed_db, T_Canvas* canvas, 
               int StartX, int StartY, int GoalX, int GoalY)
{
    T_DB_OpenNode  open_db;
    int           neighbour_x = 0;
    int           neighbour_y = 0;
    int           neighbour_g_score_straight = 0;
    int           neighbour_g_score_diagonal = 0;
    int           candidate_g_score          = 0;
    int           direction = 0;
    int           g_score   = 0;

    DB_NodeXY_construct(closed_db);
    DB_OpenNode_construct(&open_db); 
    DB_OpenNode_enter(&open_db, (T_Node*)0x0,
                      StartX, StartY, 0,
                      __compute_h(StartX, StartY, GoalX, GoalY));

    while( open_db.db_xy.begin != open_db.db_xy.end ) {
        T_Node* iterator = DB_OpenNode_move_best_f_score_to_closed_db(&open_db, closed_db, &g_score);

        /* Goal reached? */
        if( iterator->x == GoalX && iterator->y == GoalY ) break;

        neighbour_x = iterator->x + 1;
        neighbour_y = iterator->y;
        neighbour_g_score_straight = g_score + 1; 
        neighbour_g_score_diagonal = g_score + 2; 
        direction = 0;
        do { 
            if(    ! DB_NodeXY_has(closed_db, neighbour_x, neighbour_y) 
                && (neighbour_x >= 0 && neighbour_x < canvas->x_size) 
                && (neighbour_y >= 0 && neighbour_y < canvas->y_size) 
                && *(canvas->surface + (canvas->x_size * neighbour_y) + neighbour_x) == ' ' ) {

                /* Directions 1, 3, 5, 7 are diagonal, so add something that corresponds to sqrt(2) */
                if( direction & 0x1 ) candidate_g_score = neighbour_g_score_diagonal; 
                else                  candidate_g_score = neighbour_g_score_straight;

                T_Node**  open_node = DB_NodeXY_find(&open_db.db_xy, neighbour_x, neighbour_y);

                if(     open_node == open_db.db_xy.end 
                   || ! ((*open_node)->x == neighbour_y && (*open_node)->y == neighbour_y) ) {
                    DB_OpenNode_enter(&open_db, 
                                     /* parent  */ iterator, 
                                     /* x/y     */ neighbour_x, neighbour_y, 
                                     /* g_score */ candidate_g_score, 
                                     /* h_score */ __compute_h(neighbour_x, neighbour_y, GoalX, GoalY));
                } 
                else { 
                    if( candidate_g_score < (*open_node)->g_score ) {
                        DB_OpenNode_adapt_path_info(&open_db, *open_node, candidate_g_score, /* Parent */iterator);
                    }
                    else { 
                        /* Node is already on the to do list and no shorter path has been found. */
                    }
                }
            }
            ++direction;
            __get_next_neighbour_node_db_direction_index(direction, &neighbour_x, &neighbour_y);
        } while( direction != 8 );

        // DB_NodeXY_print(closed_db, "ClosedDB");
    }
}

#include <stdio.h>
void
Path_display(T_DB_NodeXY* me, T_Canvas* canvas)
{
    T_Node**  iterator = 0x0;

    if( me->begin == me->end ) return;

    iterator = me->end - 1;
    printf("%i, %i\n", (int)canvas->y_size, (int)canvas->x_size);
    do { 
        if(    (*iterator)->y >= 0 && (*iterator)->y < canvas->y_size
            && (*iterator)->x >= 0 && (*iterator)->x < canvas->x_size ) {
            *(canvas->surface + ((*iterator)->y) * (canvas->x_size) + (*iterator)->x) = 'o';
            printf("SET\n");
        }
        printf("%02X.%02X.%08X\n", (int)(*iterator)->x, (int)(*iterator)->y, (int)(*iterator)->parent);
        (*iterator) = (*iterator)->parent;
    } while( *iterator != 0x0 );
}

