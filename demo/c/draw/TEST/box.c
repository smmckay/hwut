#include "vagl.h"

int
main(int argc, char** argv)
{
    char  screen[Y_SIZE][X_SIZE];
    if( argc > 1 && strcmp(argv[1], "--hwut-info") == 0 ) { 
        printf("Box: Simple\n");
        return 0;
    }

    init(screen);
    // draw_line(screen, 5, 5, 56, 17);
    // draw_circle(screen, 10, 10, 5);
    draw_box(screen, 5, 5, 35, 13);
    display(screen);
    
}

