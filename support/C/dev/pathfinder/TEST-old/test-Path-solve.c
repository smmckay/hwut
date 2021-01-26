#include <hwut_graph.h>
#include <hwut_path.h>
#include <stdio.h>
#include <string.h>
#include <List_NodeP.h>

int 
main(int argc, char** argv)
{
    // int        line_n = 0;
    T_Canvas   canvas;
    // char*      writerator = 0x0;
    // size_t     byte_count = 0;

    if( argc > 1 && strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("Pathfinder.");
        return 0;
    }
    // FILE* fh = fopen("example-maze-0.txt", "rb");
    FILE* fh = fopen("example-maze.txt", "rb");
    if( fh == NULL ) {
        printf("Input file not found.\n");
        return -1;
    }

    // Canvas_construct(&canvas, 4, 2); 
    Canvas_construct(&canvas, 80, 15); 

    char* writerator = canvas.surface;
    char  dummy      = 0xFF;
    int   line_n     = 0;
    int   byte_count = 0;
    for(line_n = 0; line_n < canvas.y_size; ++line_n ) {
        byte_count = fread(writerator, 1, canvas.x_size, fh);
        if(  byte_count == 0 ) break;
        fread(&dummy, 1, 1, fh); /* Read the '\n' */
        if( byte_count == 0 ) break;
        writerator += byte_count;
    }
    Canvas_display(&canvas);

    T_DB_NodeXY   path;

    // Path_construct(&path, &canvas, 0, 0, 0, 1);
    Path_construct(&path, &canvas, 0, 0, 0, 23);
    Path_display(&path, &canvas);
    Canvas_display(&canvas);

#   if 0
    Path_construct(&path, &canvas, 0, 0, 2, 0);
    Path_display(&path, &canvas);
    Path_construct(&path, &canvas, 0, 0, 7, 0);
    Path_display(&path, &canvas);
    Path_construct(&path, &canvas, 0, 0, 21, 0);
    Path_display(&path, &canvas);

    {
        char    tmp[65536];
        char*   writerator = (char*)tmp;
        T_Node* iterator;

        writerator += snprintf(writerator, 1024, "x,y;");
        for(iterator = path.end; iterator != 0x0; iterator = iterator->parent) {
            writerator += sprintf(writerator, "%i,%i;", iterator->x, iterator->y); 
        }
        Table_print("Path", tmp);
    }
#   endif

    // Canvas_display(&canvas);

    return 0;
}
