#include <hwut_unit.h>
#include <inttypes.h>
#include <string.h>

int
rundolf_random()
{
    static uint32_t  tmp = 17;
    tmp = tmp * tmp;
    tmp = tmp % 57;
    return tmp;
}

int
main(int argc, char** argv)
{
    int i = 0;

    if( argc > 1 && strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("Macros from 'hwut_unit.h';\n");
        printf("HAPPY: :[0-9]+:;\n");
        return 0;
    }

    hwut_verify_verbose( 1 + 1 == 2 );
    hwut_verify_verbose( 1 + 1 == 3 );

    i = rundolf_random();
    hwut_verify_verbose( i < 10 && (i % 2 == 0));

    i = rundolf_random();
    hwut_verify_verbose( i > 20 && (i % 4 == 0));

    i = rundolf_random();
    printf("##                  i: %i; i*i: %i; (i*i)%%10: %i;\n", (int)i, (int)(i*i), (int)((i * i) % 10));
    //hwut_verify_verbose((i < 0));
    //hwut_verify_verbose(((i * i) >= 400));
    //hwut_verify_verbose(((i * i) % 10));
    hwut_verify_verbose((i > 0) && ((i * i) >= 400) && ((i * i) % 10));
    hwut_verify_verbose( rundolf_random() > 12 );

    hwut_verify( 1 + 1 == 2 );
    hwut_verify( 1 + 1 == 3 );

    /* Annotated verify 'averify' */
    hwut_averify_verbose("One plus one is two, or not?",           1 + 1 == 2);
    hwut_averify_verbose("One plus one cannot be three, or what?", 1 + 1 == 3);

    hwut_averify("Silent: One plus one is two, or not?",           1 + 1 == 2);
    hwut_averify("Silent: One plus one cannot be three, or what?", 1 + 1 == 3);
    return 0;
}
