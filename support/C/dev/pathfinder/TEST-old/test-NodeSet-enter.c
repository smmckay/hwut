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

void test(int EntryN) 
{
    T_NodeSet  node_set;
    int        i = 0;

    NodeSet_construct(&node_set);
    test_setup(&node_set, EntryN);
    NodeSet_print(&node_set, "Node Set");

    for(i=0; i < EntryN + 2; ++i) {
        printf("\nEnter:  X = %i; Y = %i;\n", (int)i + 9, (int)1);
        NodeSet_enter(&node_set, i + 9, 1);
        NodeSet_print(&node_set, "Result Node Set");
        test_setup(&node_set, EntryN);
    }
    

}

int
main(int argc, char** argv)
{
    if( argc < 2 ) {
       printf("Command line argument required.\n");
    }
    if( strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("NodeSet: Enter;\n");
        printf("CHOICES:  0, 1, 2, 3;\n");
        return 0;
    }

    test(atoi(argv[1]));
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

