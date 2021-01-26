#include <hwut_graph.h>
#include <stdio.h>
#include <string.h>

int 
main(int argc, char** argv)
{
    T_Data   x;
    T_Canvas canvas; 

    if( argc > 1 && strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("Grids.");
        return 0;
    }

    Canvas_construct(&canvas, 100, 40);
    { 
        Grid_construct(&x, 25, "Something About X", "x=1;xx=1;x=11;42;a=0;hallo;welt;bonjour;le;Monde;");

        x.display(&x, &canvas, 0, 0);
    }
    { 
        Grid_construct(&x, 14, "01234567890123456", "x=1;xx=1;x=11;42;a=0;hallo;welt;bonjour;le;Monde;");

        x.display(&x, &canvas, 0, 5);
    }
    { 
        Grid_construct(&x, 30, "Nonesense", "construction=12; building=13;morg=4711;");

        x.display(&x, &canvas, 20, 20);
    }
    Canvas_display(&canvas);

    return 0;
}

