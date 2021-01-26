#include "vagl.h"

int
main(int argc, char** argv)
{
    char  screen[Y_SIZE][X_SIZE];
    if( argc > 1 && strcmp(argv[1], "--hwut-info") == 0 ) { 
        printf("Box: Exceed Borders\n");
        printf("CHOICES: LEFT, RIGHT, TOP, BOTTOM, OUT;\n");
        return 0;
    }

    // draw_line(screen, 5, 5, 56, 17);
    // draw_circle(screen, 10, 10, 5);
    if( argc < 2 ) return;

    init(screen);

    printf("## this is one of my first tests (it's a comment)\n");
    if     ( strcmp(argv[1], "LEFT")   == 0 ) { draw_box(screen, -5, 5, 35, 13); }
    else if( strcmp(argv[1], "RIGHT")  == 0 ) { draw_box(screen, 5, 5, 135, 13); }
    else if( strcmp(argv[1], "TOP")    == 0 ) { draw_box(screen, 5, -5, 35, 12); }
    else if( strcmp(argv[1], "BOTTOM") == 0 ) { draw_box(screen, 5, 2, 35,  1300); }
    else                                      { draw_box(screen, 555, 555, 5535,  1113); }

    display(screen);
}

