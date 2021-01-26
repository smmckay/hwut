#include <hwut_graph.h>
#include <stdio.h>
#include <string.h>

int 
main(int argc, char** argv)
{
    T_Data     x;
    T_Canvas   canvas;

    if( argc > 1 && strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("Objects.");
        return 0;
    }

    Canvas_construct(&canvas, 100, 40);

    printf("\n");
    { 
        Object_construct(&x, "Something About X", "x=1;xx=1;x=11;Colonia;");

        x.display(&x, &canvas, 0, 0);
    }
    printf("\n");
    { 
        Object_construct(&x, "Nonsense", "construction=12;building=13;morg=4711;");

        x.display(&x, &canvas, 10, 15);
    }
    printf("\n");
    Canvas_display(&canvas);

    return 0;
}

