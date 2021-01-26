#include <DB_OpenNode.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

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

int
main(int argc, char** argv)
{
    if( argc < 2 ) {
       printf("Command line argument required.\n");
    }
    else if( strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("DB_OpenNode: Remove;\n");
        return 0;
    }

    char           tmp[65536];
    T_DB_OpenNode  open_db;
    T_DB_NodeXY    closed_db;
    int            i       = 0;
    int            g_score = 0;

    DB_OpenNode_construct(&open_db);
    DB_NodeXY_construct(&closed_db);

    test_setup(&open_db, 5);
    DB_OpenNode_print(&open_db);

    for(i=0; i < 5 ; ++i) {
        DB_OpenNode_move_best_f_score_to_closed_db(&open_db, &closed_db, &g_score);
        DB_OpenNode_print(&open_db);
        DB_NodeXY_get_display_string(&closed_db, tmp, 65536);
        Table_print("Closed DB", tmp);
    }
    
    return 0;
}


