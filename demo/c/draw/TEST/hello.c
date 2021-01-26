#include<stdio.h>
#include<string.h>

#define IF_OPTION(option) \

int
main(int argc, char** argv)
{
    if( argc > 1 && strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("This is a hello world application.\n");
        printf("CHOICES: Good, Bad;");
    }

}

