#include <ScoreInfoDB.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void quick_enter(T_ScoreInfoDB* me, int FScore);
void quick_find(T_ScoreInfoDB* me, int FScore);

void test(int EntryN);

void 
test_setup(T_ScoreInfoDB* node_set, int EntryN)
{
    int i = 0;

    printf("\n");
    node_set->end = node_set->begin;
    for(i=EntryN-1; i >= 0; --i) {
        quick_enter(node_set, i * 2 + 10);
    }

}

void 
test(int EntryN) 
{
    T_ScoreInfoDB  node_set;
    int        i = 0;

    ScoreInfoDB_construct(&node_set);
    test_setup(&node_set, EntryN);
    ScoreInfoDB_print(&node_set, "Node Set");

    for(i=0; i < EntryN + 2; ++i) {
        printf("\nEnter:  FScore = %i;\n", (int)(i * 2 + 9));
        ScoreInfoDB_enter(&node_set, 0x0, i + 9, i);
        ScoreInfoDB_print(&node_set, "Result Node Set");
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
        printf("ScoreInfoDB: Enter;\n");
        printf("CHOICES:  0, 1, 2, 3;\n");
        return 0;
    }

    test(atoi(argv[1]));
    return 0;
}


void
quick_enter(T_ScoreInfoDB* me, int FScore)
{
    me->end->f_score = FScore; 
    ++(me->end);
}

