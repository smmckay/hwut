#include <ScoreInfoDB.h>
#include <stdio.h>
#include <string.h>

void quick_enter(T_ScoreInfoDB* me, int FScore);
void quick_find(T_ScoreInfoDB* me, int FScore);

int
main(int argc, char** argv)
{
    if( argc < 2 ) {
       printf("Command line argument required.\n");
    }
    if( strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("ScoreInfoDB: Find;\n");
        printf("CHOICES:  0, 1, 2, 3;\n");
        return 0;
    }

    T_ScoreInfoDB  node_set;

    ScoreInfoDB_construct(&node_set);

    if( strcmp(argv[1], "0") == 0 ) {
        ScoreInfoDB_print(&node_set, "Node Set");

        quick_find(&node_set, 0);
        quick_find(&node_set, 33);
    }
    else if( strcmp(argv[1], "1") == 0 ) {
        quick_enter(&node_set, 35);

        ScoreInfoDB_print(&node_set, "Node Set");

        quick_find(&node_set, 34);
        quick_find(&node_set, 35);
        quick_find(&node_set, 36);
    }
    else if( strcmp(argv[1], "2") == 0 ) {
        quick_enter(&node_set, 35);
        quick_enter(&node_set, 34);

        ScoreInfoDB_print(&node_set, "Node Set");

        quick_find(&node_set, 33);
        quick_find(&node_set, 34);
        quick_find(&node_set, 35);
        quick_find(&node_set, 36);
    }
    else if( strcmp(argv[1], "3") == 0 ) {
        quick_enter(&node_set, 35);
        quick_enter(&node_set, 34);
        quick_enter(&node_set, 33);

        ScoreInfoDB_print(&node_set, "Node Set");

        quick_find(&node_set, 32);
        quick_find(&node_set, 33);
        quick_find(&node_set, 34);
        quick_find(&node_set, 35);
        quick_find(&node_set, 36);
    }
    
    return 0;
}


void
quick_enter(T_ScoreInfoDB* me, int FScore)
{
    me->end->f_score = FScore; 
    me->end->g_score = FScore ^ 0xFF;
    ++(me->end);
}

void
quick_find(T_ScoreInfoDB* me, int FScore)
{
    T_ScoreInfo*  node = ScoreInfoDB_find(me, me->begin, FScore);

    printf("Search: FScore = %i;\n", (int)FScore);
    if( node == me->end ) { 
        printf("Found:  END\n");
    }
    else {
        printf("Found:  FScore = %i;\n", (int)node->f_score);
    } 
    printf("\n");
}
