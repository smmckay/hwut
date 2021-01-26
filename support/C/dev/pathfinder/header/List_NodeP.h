#ifndef __HWUT_INCLUDE_GUARD__PATHFINDER__NODE_SET_H
#define __HWUT_INCLUDE_GUARD__PATHFINDER__NODE_SET_H

#include "hwut_graph.h"

struct T_ScoreInfo_tag;

typedef struct T_Node_tag { 
    int    x;
    int    y;
    int    f_score;
    int    g_score;
    /**/
    struct T_Node_tag*  parent;
} T_Node;

typedef struct T_List_NodeP_tag { 
    T_Node**  begin;
    T_Node**  end;
    T_Node**  memory_end;
} T_List_NodeP;

typedef T_List_NodeP  T_DB_NodeXY;
typedef T_List_NodeP  T_DB_NodeFScore;

void      DB_NodeXY_construct(T_List_NodeP* me);
void      DB_NodeXY_enter(T_DB_NodeXY* me, T_Node* NodeP);
void      DB_NodeXY_remove(T_DB_NodeXY* me, T_Node** node);
T_Node**  DB_NodeXY_find(T_DB_NodeXY* me, int X, int Y);
int       DB_NodeXY_has(T_DB_NodeXY* me, int X, int Y);
void      DB_NodeXY_get_display_string(T_DB_NodeXY* me, 
                                       char* tmp, size_t ByteN);

void      DB_NodeFScore_construct(T_DB_NodeFScore* me);
void      DB_NodeFScore_enter(T_DB_NodeFScore*      me, 
                              struct T_Node_tag*  NodeP); 
void      DB_NodeFScore_adjust_position(T_DB_NodeFScore*      me, 
                                        struct T_Node_tag*  NodeP, 
                                        int                 NewGScore);
T_Node**  DB_NodeFScore_find(T_DB_NodeFScore*   me, int F_Score);

#endif /* __HWUT_INCLUDE_GUARD__PATHFINDER__NODE_SET_H */

