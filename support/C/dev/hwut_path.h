#ifndef  __HWUT_INCLUDE_GUARD_GRAPH_H
#define  __HWUT_INCLUDE_GUARD_GRAPH_H

#include "hwut_graph.h"
#include "List_NodeP.h"

struct T_Node_tag;
struct T_Canvas_tag;
struct T_List_NodeP_tag;

typedef struct {
    struct T_Node_tag*  begin;
    struct T_Node_tag*  end;
} T_Path;

extern void
Path_construct(T_DB_NodeXY*  closed_db, T_Canvas* canvas, 
               int StartX, int StartY, int GoalX, int GoalY);

extern void
Path_display(T_DB_NodeXY* me, struct T_Canvas_tag* canvas);

#endif /* __HWUT_INCLUDE_GUARD_GRAPH_H */
