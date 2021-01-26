#include <DB_OpenNode.h>
#include <List_NodeP.h>
#include <hwut_scanner.h>
#include <assert.h>

#include <stdio.h>

static void
DB_OpenNode_assert_consistency(T_DB_OpenNode* me);

void
DB_OpenNode_construct(T_DB_OpenNode*  me)
{
    DB_NodeXY_construct(&me->db_xy);
    DB_NodeFScore_construct(&me->db_fscore);

    DB_OpenNode_assert_consistency(me);
}

void
DB_OpenNode_enter(T_DB_OpenNode*  me, 
                 T_Node*        Parent,
                 int X, int Y, int G_Score, int H_Score)
{
    T_Node*   new_node_p = (T_Node*)hwut_malloc(sizeof(T_Node));
 
    // printf("DB_OpenNode_enter: %i, %i\n", (int)X, (int)Y);

    DB_OpenNode_assert_consistency(me);

    new_node_p->x       = X;
    new_node_p->y       = Y;
    new_node_p->g_score = G_Score;
    new_node_p->f_score = G_Score + H_Score;

    new_node_p->parent = Parent;

    DB_NodeXY_enter(&me->db_xy, new_node_p);
    DB_NodeFScore_enter(&me->db_fscore, new_node_p);

    DB_OpenNode_assert_consistency(me);
}

T_Node*
DB_OpenNode_move_best_f_score_to_closed_db(T_DB_OpenNode* me, T_DB_NodeXY* closed_db, int* g_score_p)
    /* Moves a node from the todo list (open_db) to the done line (closed_db). The 
     * done list does not need the score info anymore, thus the 'info' pointer is
     * not kept up-to-date. However, the g_score is communicated via the variable 
     * 'g_score_p'.                                                                 */
{
    assert(me->db_fscore.begin != me->db_fscore.end);

    DB_OpenNode_assert_consistency(me);

    T_Node*  best    = *(me->db_fscore.end - 1);
    T_Node** node_pp = DB_NodeXY_find(&me->db_xy, best->x, best->y);

    assert(node_pp != me->db_xy.end);
    assert(*node_pp == best);

    *g_score_p = best->g_score;

    DB_NodeXY_remove(&me->db_xy, node_pp);
    DB_NodeXY_enter(closed_db, best);

    /* The node with the best f-score is on top of the array. */
    --(me->db_fscore.end);
    hwut_memset((void*)me->db_fscore.end, 0, sizeof(T_Node**));

    DB_OpenNode_assert_consistency(me);
    return best;
}


void
DB_OpenNode_adapt_path_info(T_DB_OpenNode*  me,        T_Node*  node, 
                            int             NewGScore, T_Node*  NewParent)
{
    const int OldGScore = node->g_score;
    const int NewFScore = node->f_score - OldGScore + NewGScore;

    DB_OpenNode_assert_consistency(me);

    /* We found a shorter path to the same node. */
    node->parent  = NewParent;
    node->g_score = NewGScore;

    DB_NodeFScore_adjust_position(&me->db_fscore, node, NewFScore); 

    DB_OpenNode_assert_consistency(me);
}

#include <hwut_graph.h>
int
DB_OpenNode_get_index(T_DB_OpenNode* me, T_Node* NodeP)
{
    T_Node** iterator = 0x0;

    /* Let the 'xy' database be the reference for the index. */
    for(iterator = me->db_xy.begin; iterator != me->db_xy.end; ++iterator) {
        if( NodeP == *iterator ) return iterator - me->db_xy.begin;
    }
    return -1;
}

void
DB_OpenNode_print(T_DB_OpenNode* me)
{
    char      tmp1[65536];
    char      tmp2[65536];
    char*     writerator = 0x0; 
    T_Node**  sciterator = 0x0;
    T_Canvas  canvas;
    T_Data    table_xy;
    T_Data    table_fscore;

    Canvas_construct(&canvas, 80, 25);

    DB_NodeXY_get_display_string(&me->db_xy, tmp1, 65536);
    Table_construct(&table_xy, "XY Database", tmp1);

    writerator  = (char*)tmp2;
    writerator += snprintf(writerator, 1024, "idx,f_score;");
    for(sciterator = me->db_fscore.begin; sciterator != me->db_fscore.end; ++sciterator) {
        writerator += sprintf(writerator, "%i,%i;", 
                              DB_OpenNode_get_index(me, *sciterator), 
                              (int)((*sciterator)->f_score)); 
        if( writerator - tmp2 > 65536 - 128 ) break;
    }
    Table_construct(&table_fscore, "FScore Database", tmp2);


    table_xy.display(&table_xy,         &canvas, 0,                   10);
    table_fscore.display(&table_fscore, &canvas, table_xy.x_size + 6, 10);

    printf("\n");
    Canvas_display_minimal(&canvas);
}

static void
DB_OpenNode_assert_consistency(T_DB_OpenNode* me)
{
    int       prev_y      = -1;
    int       prev_x      = -1;
    int       prev_fscore = -1;
    T_Node**  iterator    = 0;
    T_Node**  sciterator  = 0;

    /* Number of nodes in the node set must be equal to the number of 
     * nodes in the score list.                                       */
    assert(me->db_xy.end - me->db_xy.begin == me->db_fscore.end - me->db_fscore.begin);
    
    if( me->db_xy.end == me->db_xy.begin ) return;
    /* XY list is sorted by '.x, .y'                                  */
    prev_x = (*(me->db_xy.begin))->x - 1;
    prev_y = (*(me->db_xy.begin))->y - 1;
    for(iterator = me->db_xy.begin; iterator != me->db_xy.end ; ++iterator) {
        if( ! ( (*iterator)->y > prev_y || (*iterator)->x > prev_x ) ) {
            printf("");
        }
        prev_x = (*iterator)->x;
        prev_y = (*iterator)->y;
    }

    /* Score list is sorted by '.fscore'                              */
    prev_fscore = (*(me->db_fscore.begin))->f_score;
    for(sciterator = me->db_fscore.begin; sciterator != me->db_fscore.end ; ++sciterator) {
        /* assert( *(sciterator->node_p)->info == sciterator );       */
        assert( (*sciterator)->f_score <= prev_fscore );
        prev_fscore = (*sciterator)->f_score;
    }
}


