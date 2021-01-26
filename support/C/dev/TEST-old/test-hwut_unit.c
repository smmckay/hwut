#include <hwut_unit.h>
#include <string.h>

int
rundolf_random()
{
    static long  tmp = 17;
    tmp = tmp * tmp;
    if( tmp > 100000 ) tmp = tmp % 100000;
    return tmp % 57;
}

int
main(int argc, char** argv)
{
    int i = 0;

    if( argc > 1 && strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("Macros from 'hwut_unit.h'.");
        return 0;
    }

    hwut_verify_verbose( 1 + 1 == 2 );
    hwut_verify_verbose( 1 + 1 == 3 );

    i = rundolf_random();
    hwut_verify_verbose( i < 10 && (i % 2 == 0));

    i = rundolf_random();
    hwut_verify_verbose( i > 20 && (i % 4 == 0));

    i = rundolf_random();
    hwut_verify_verbose( i < 0 && (i * i) >= 400 && (i * i) % 10);
    hwut_verify_verbose( rundolf_random() > 12 );

    hwut_verify( 1 + 1 == 2 );
    hwut_verify( 1 + 1 == 3 );

    /* Annotated verify 'averify' */
    hwut_verify_verbose("One plus one is two, or not?",           1 + 1 == 2);
    hwut_verify_verbose("One plus one cannot be three, or what?", 1 + 1 == 3);

    hwut_averify("Silent: One plus one is two, or not?",           1 + 1 == 2);
    hwut_averify("Silent: One plus one cannot be three, or what?", 1 + 1 == 3);
    return 0;
}
