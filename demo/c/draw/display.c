/* SPDX license identifier: MIT
 * (C) 2006-2016 Frank-Rene Schaefer, private.
 * (C) 2006-2016 Frank-Rene Schaefer, Visteon Innovation&Technology GmbH, 
 *     Kerpen, Germany.
 * This file is part of HWUT - Project.
 * This Source Code Form is subject to the terms of the MIT License (MIT).
 *---------------------------------------------------------------------------*/
#include<vagl.h>

void init(char screen[Y_SIZE][X_SIZE])
{
    int x = -1;
    int y = -1;

    for(x=0; x<X_SIZE; ++x) { 
        for(y=0; y<Y_SIZE; ++y) { 
            screen[y][x] = ' ';
        }
    }
}

void display(char screen[Y_SIZE][X_SIZE])
{
    int x = -1;
    int y = -1;

    for(y=0; y<Y_SIZE; ++y) { 
        printf("%02i:", y);
        for(x=0; x<X_SIZE; ++x) { 
            printf("%c", screen[y][x]);
        }
        printf("\n");
    }
}

