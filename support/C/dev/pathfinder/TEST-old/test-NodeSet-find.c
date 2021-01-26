#include <NodeSet.h>
#include <stdio.h>
#include <string.h>

void quick_enter(T_NodeSet* me, int X, int Y);
void quick_find(T_NodeSet* me, int X, int Y);

int
main(int argc, char** argv)
{
    if( argc < 2 ) {
       printf("Command line argument required.\n");
    }
    if( strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("NodeSet: Find;\n");
        printf("CHOICES:  0, 1, 2a, 2b, 3a, 3b;\n");
        return 0;
    }

    T_NodeSet  node_set;

    NodeSet_construct(&node_set);

    if( strcmp(argv[1], "0") == 0 ) {
        NodeSet_print(&node_set, "Node Set");

        quick_find(&node_set, 0, 0);
        quick_find(&node_set, 33, 99);
    }
    else if( strcmp(argv[1], "1") == 0 ) {
        quick_enter(&node_set, 34, 47);

        NodeSet_print(&node_set, "Node Set");

        quick_find(&node_set, 33, 99);
        quick_find(&node_set, 34, 46);
        quick_find(&node_set, 34, 47);
        quick_find(&node_set, 34, 48);
        quick_find(&node_set, 35, 0);
    }
    else if( strcmp(argv[1], "2a") == 0 ) {
        quick_enter(&node_set, 34, 47);
        quick_enter(&node_set, 34, 48);

        NodeSet_print(&node_set, "Node Set");

        quick_find(&node_set, 34, 46);
        quick_find(&node_set, 34, 47);
        quick_find(&node_set, 34, 48);
        quick_find(&node_set, 34, 49);
    }
    else if( strcmp(argv[1], "2b") == 0 ) {
        quick_enter(&node_set, 47, 34);
        quick_enter(&node_set, 48, 34);

        NodeSet_print(&node_set, "Node Set");

        quick_find(&node_set, 46, 34);

        quick_find(&node_set, 47, 33);
        quick_find(&node_set, 47, 34);
        quick_find(&node_set, 47, 35);

        quick_find(&node_set, 48, 33);
        quick_find(&node_set, 48, 34);
        quick_find(&node_set, 48, 35);

        quick_find(&node_set, 49, 33);
    }
    else if( strcmp(argv[1], "3a") == 0 ) {
        quick_enter(&node_set, 34, 47);
        quick_enter(&node_set, 34, 48);
        quick_enter(&node_set, 34, 49);

        NodeSet_print(&node_set, "Node Set");

        quick_find(&node_set, 34, 46);
        quick_find(&node_set, 34, 47);
        quick_find(&node_set, 34, 48);
        quick_find(&node_set, 34, 49);
        quick_find(&node_set, 34, 50);
    }
    else if( strcmp(argv[1], "3b") == 0 ) {
        quick_enter(&node_set, 47, 34);
        quick_enter(&node_set, 48, 34);
        quick_enter(&node_set, 49, 34);

        NodeSet_print(&node_set, "Node Set");

        quick_find(&node_set, 46, 34);

        quick_find(&node_set, 47, 33);
        quick_find(&node_set, 47, 34);
        quick_find(&node_set, 47, 35);

        quick_find(&node_set, 48, 33);
        quick_find(&node_set, 48, 34);
        quick_find(&node_set, 48, 35);

        quick_find(&node_set, 49, 33);
        quick_find(&node_set, 49, 34);
        quick_find(&node_set, 49, 35);

        quick_find(&node_set, 50, 34);
    }
    
    return 0;
}

#include <malloc.h>

void
quick_enter(T_NodeSet* me, int X, int Y)
{
    ((me->end))->x = X; 
    ((me->end))->y = Y;
    ++(me->end);
}

void
quick_find(T_NodeSet* me, int X, int Y)
{
    T_Node*  node = NodeSet_find(me, X, Y);

    printf("Search: X = %i; Y = %i;\n", (int)X, (int)Y);
    if( node == me->end ) { 
        printf("Found:  END\n");
    }
    else {
        printf("Found:  X = %i; Y = %i;\n", (int)node->x, (int)node->y);
    } 
    printf("\n");
}
