#ifndef __HWUT_INCLUDE_GUARD__PATHFINDER__OPEN_NODE_DB_H
#define __HWUT_INCLUDE_GUARD__PATHFINDER__OPEN_NODE_DB_H

#include <List_NodeP.h>

typedef struct { 
    T_DB_NodeXY      db_xy;
    T_DB_NodeFScore  db_fscore;
} T_DB_OpenNode;

void     DB_OpenNode_construct(T_DB_OpenNode*  me);

void     DB_OpenNode_enter(T_DB_OpenNode* me, 
                           T_Node*        Parent,
                           int X, int Y, int G_Score, int H_Score);

T_Node*  DB_OpenNode_move_best_f_score_to_closed_db(T_DB_OpenNode*  open_db, 
                                                    T_List_NodeP*  closed_db, 
                                                    int*           g_score_p);

void     DB_OpenNode_adapt_path_info(T_DB_OpenNode* me, 
                                     T_Node*       info, 
                                     int           NewGScore, T_Node* Parent);

void     DB_OpenNode_print(T_DB_OpenNode* me);
#endif /* __HWUT_INCLUDE_GUARD__PATHFINDER__OPEN_NODE_DB_H */
