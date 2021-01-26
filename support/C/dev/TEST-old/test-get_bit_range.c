#include <hwut_graph.h>
#include <hwut_scanner.h>
#include <stdio.h>
#include <string.h>

void
test_this(void* ValueP, int BeginI, int EndI) 
{
    int value = hwut_get_bit_range(ValueP, 4, BeginI, EndI);
    printf("%X.", (int)((unsigned char*)ValueP)[0]);
    printf("%X.", (int)((unsigned char*)ValueP)[1]);
    printf("%X.", (int)((unsigned char*)ValueP)[2]);
    printf("%X:", (int)((unsigned char*)ValueP)[3]);
    printf(" %2i %2i --> %X\n", BeginI, EndI, (int)value);
}

int 
main(int argc, char** argv)
{
    unsigned char  array[] = { 0x11, 0x22, 0x33, 0x44, };
    /*                         1100.1100.1100.1100 ....    */
    unsigned char  bray[]  = { 0xCC, 0xCC, 0xCC, 0xCC, };
    /*                         1100.0111.0001.1100.0111.0001.1100.0111 */
    unsigned char  cray[]  = { 0xC7, 0x1C, 0x71, 0xC7, };

    if( argc > 1 && strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("Extract bit range from byte sequence.");
        return 0;
    }

    test_this(bray,  0,  1);
    test_this(bray,  2,  3);
    test_this(bray,  4,  5);
    test_this(bray,  6,  7);
    test_this(bray,  8,  9);
    test_this(bray, 10, 11);
    test_this(bray, 12, 13);
    test_this(bray, 14, 15);
    test_this(bray, 16, 17);
    test_this(bray, 18, 19);
    printf("-----\n");
    test_this(array,  0,  3);
    test_this(array,  4,  7);
    test_this(array,  8, 11);
    test_this(array, 12, 15);
    test_this(array, 16, 19);
    test_this(array, 20, 23);
    test_this(array, 24, 27);
    test_this(array, 28, 31);
    printf("-----\n");
    test_this(array,  0,  7);
    test_this(array,  8, 15);
    test_this(array, 16, 23);
    test_this(array, 24, 31);
    printf("-----\n");
    test_this(array,  0,  11);
    test_this(array,  4,  15);
    test_this(array,  8,  19);
    test_this(array, 12,  23);
    test_this(array, 16,  27);
    test_this(array, 20,  31);
    printf("-----\n");
    test_this(cray,  0,  2);  
    test_this(cray,  3,  5);  
    test_this(cray,  6,  8); 
    test_this(cray,  9, 11); 
    test_this(cray, 12, 14);
    test_this(cray, 15, 17);
    test_this(cray, 18, 20);
    test_this(cray, 21, 23);
    test_this(cray, 24, 26);
    test_this(cray, 27, 29);

    return 0;
}
