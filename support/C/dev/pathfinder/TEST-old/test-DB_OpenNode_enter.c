#include <DB_OpenNode.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void quick_enter(T_DB_OpenNode* me, int X, int Y);
void quick_find(T_DB_OpenNode* me, int X, int Y);

void test(int EntryN);

int my_random()
{
    static long tmp = 7;
    int         result = 0;

    tmp *= tmp;
    result = tmp % 17;

    if( tmp > 413 * 413 ) tmp = tmp % 413;

    return result > 0 ? result : - result;
}

void test_setup(T_DB_OpenNode*  db, int EntryN)
{
    int i = 0;

    db->db_xy.end     = db->db_xy.begin;
    db->db_fscore.end = db->db_fscore.begin;
    printf("\n");
    for(i=0; i < EntryN; ++i) {
        DB_OpenNode_enter(db, 0x0, i + 10, 0, 3 + (i + 3) % 4, 4 + (i + 5) % 8);
    }

}

void test(int EntryN) 
{
    T_DB_OpenNode  db;
    int           i = 0;

    DB_OpenNode_construct(&db);
    DB_OpenNode_enter(&db, 0, 0, 0, my_random(), my_random());

    printf("(*) Setup before eache experiment: _____________________________________________\n");
    test_setup(&db, EntryN);
    DB_OpenNode_print(&db);
    printf("________________________________________________________________________________\n");

    for(i=0; i < EntryN + 1; ++i) {
        const int   X      = (int)i + 9;
        const int   Y      = (int)1;
        const int   GScore = my_random();
        const int   HScore = my_random();
        printf("\nEnter:  X = %i; Y = %i; G = %i; H = %i;\n", X, Y, GScore, HScore);
        DB_OpenNode_enter(&db, 0x0, X, Y, GScore, HScore);
        DB_OpenNode_print(&db);
        test_setup(&db, EntryN);
    }
}

int
main(int argc, char** argv)
{
    if( argc < 2 ) {
       printf("Command line argument required.\n");
    }
    if( strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("DB_OpenNode: Enter;\n");
        printf("CHOICES: 0, 1, 3;\n");
        return 0;
    }

    test(atoi(argv[1]));
    return 0;
}


