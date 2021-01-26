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
        DB_OpenNode_enter(db, 0x0, i + 10, 0, i * 2 + 2, 10);
    }

}

int
main(int argc, char** argv)
{
    if( argc <= 2 ) {
       printf("Command line argument required.\n");
    }
    else if( strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("DB_OpenNode: Adapth Path Information;\n");
        printf("CHOICES:     2, 4, 6;\n");
        return 0;
    }

    T_DB_OpenNode  open_db;
    T_DB_NodeXY    closed_db;
    T_Node*        iterator = 0x0;

    DB_OpenNode_construct(&open_db);
    DB_NodeXY_construct(&closed_db);

    test_setup(&open_db, 5);
    DB_OpenNode_print(&open_db);

//    for(i=0; i < 5 ; ++i) {
        /* Take the node with the 'worst' f_score and improve it until it is the best */
        iterator = *(open_db.db_fscore.begin);
        int new_gscore = iterator->g_score - 1;
        
        while( new_gscore > 0 ) {
            DB_OpenNode_adapt_path_info(&open_db, iterator, new_gscore, 0x0);
            DB_OpenNode_print(&open_db);

            new_gscore -= atoi(argv[1]);
        }
//    }
    
    return 0;
}


