/* SPDX license identifier: MIT
 * (C) 2006-2016 Frank-Rene Schaefer, private.
 * (C) 2006-2016 Frank-Rene Schaefer, Visteon Innovation&Technology GmbH, 
 *     Kerpen, Germany.
 * This file is part of HWUT - Project.
 * This Source Code Form is subject to the terms of the MIT License (MIT).
 *---------------------------------------------------------------------------*/
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

