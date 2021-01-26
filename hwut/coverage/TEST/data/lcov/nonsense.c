#include <stdio.h>
void
nonsense(int X)
{
    if( X > 0 ) {
        printf("First\n");
    }
    printf("Second\n");
}

void
never(int X)
{
    printf("Never\n");
    if( X ) {
       printf("Ever\n");
    }
}
