#include <stdio.h>

int
main(int argc, char** argv)
{
    if( argc > 2 && strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("Greeting in C: French");
        return 0;
    }
    printf("Bonjour le Monde\n");
}
