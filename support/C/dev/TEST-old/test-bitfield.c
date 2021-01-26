#include <hwut_graph.h>
#include <stdio.h>
#include <string.h>

int 
main(int argc, char** argv)
{
    T_BitField  x;
    T_Canvas    canvas;

    if( argc > 1 && strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("Bit fields.");
        return 0;
    }

    Canvas_construct(&canvas, 100, 40);

    { 
        unsigned char array[] = { 0xE0, 0x01, };
        /* 1110.0000.0000.0001 */
        BitField_construct(&x, "Bitfield/X", array, 2, "3, mask; 12, task; 1, solo;");

        x.base.display(&x.base, &canvas, 0, 0);
    }
    { 
        unsigned char array[] = { 0x9F, 0xE0, 0x00, 0x00, 0x1F, 0x00 };
        /* 1001.1111.1110.0000.0000.0000.0000.0000.0001.1111.0000.0000. */
        BitField_construct(&x, "Bitfield/Y", array, 6, "1, switch; 2, TTL; 8, DLC; 24, CRC; 5, Data; 8, Byte;");

        x.base.display(&x.base, &canvas, 0, 10);
    }
    Canvas_display(&canvas);

    return 0;
}

