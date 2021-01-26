#include <hwut_graph.h>
#include <stdio.h>
#include <string.h>

int 
main(int argc, char** argv)
{
    T_Data     x;
    T_Canvas   canvas;

    if( argc > 1 && strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("Tables.");
        return 0;
    }

    Canvas_construct(&canvas, 80, 25);
    { 
        Table_construct(&x, "Something About X", 
                            "Row A, Row B, Row C, Row D, Row E;" 
                            "a,b,,d,e;"
                            "1, 2, 3, 4, 5;");

        x.display(&x, &canvas, 0, 5);
    }
    { 
        Table_construct(&x, "Something About X", 
                            "a, b, c, d, e;" 
                            ",,,,;" 
                            ", b, ccc, d, eeee;");

        x.display(&x, &canvas, 10, 15);
    }
    {
        Table_construct(&x, "Mini", "x,y;0,0;"); 
        x.display(&x, &canvas, 0, 0);
    }
     
    Canvas_display(&canvas);

    printf("Print directly:\n\n");

    Table_print("Something About X", 
                "Row A, Row B, Row C, Row D, Row E;" 
                "a,b,,d,e;"
                "1, 2, 3, 4, 5;");

    Table_print("Something About X", 
                "a, b, c, d, e;" 
                ",,,,;" 
                ", b, ccc, d, eeee;");

    Table_print("Mini", "x,y;0,0;");

    return 0;
}

