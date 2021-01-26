#include <NodeSet.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void quick_enter(T_NodeSet* me, int X, int Y);
void quick_find(T_NodeSet* me, int X, int Y);

void test(int EntryN);

void test_setup(T_NodeSet* node_set, int EntryN)
{
    int i = 0;

    printf("\n");
    node_set->end = node_set->begin;
    for(i=0; i < EntryN; ++i) {
        quick_enter(node_set, i + 10, 0);
    }

}


int
main(int argc, char** argv)
{
    if( argc < 2 ) {
       printf("Command line argument required.\n");
    }
    if( strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("NodeSet: Remove;\n");
        printf("CHOICES:  front, middle, back;\n");
        return 0;
    }

    T_NodeSet  node_set;
    int        i = 0;

    NodeSet_construct(&node_set);
    test_setup(&node_set, 5);
    NodeSet_print(&node_set, "Node Set");

    if( strcmp(argv[1], "front") == 0 ) {
        for(i=0; i < 5 ; ++i) {
            NodeSet_remove(&node_set, node_set.begin);
            NodeSet_print(&node_set, "Result Node Set");
        }
    }
    else if( strcmp(argv[1], "middle") == 0 ) {
        for(i=0; i < 5 ; ++i) {
            NodeSet_remove(&node_set, node_set.begin + ((node_set.end - node_set.begin) >> 1));
            NodeSet_print(&node_set, "Result Node Set");
        }
    }
    else if( strcmp(argv[1], "back") == 0 ) {
        for(i=0; i < 5 ; ++i) {
            NodeSet_remove(&node_set, node_set.end - 1);
            NodeSet_print(&node_set, "Result Node Set");
        }
    }
    
    return 0;
}

#include <malloc.h>

void
quick_enter(T_NodeSet* me, int X, int Y)
{
    me->end->x = X; 
    me->end->y = Y;
    ++(me->end);
}

