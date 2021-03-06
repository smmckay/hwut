/* SPDX license identifier: MIT
 * (C) 2006-2016 Frank-Rene Schaefer, private.
 * (C) 2006-2016 Frank-Rene Schaefer, Visteon Innovation&Technology GmbH, 
 *     Kerpen, Germany.
 * This file is part of HWUT - Project.
 * This Source Code Form is subject to the terms of the MIT License (MIT).
 *---------------------------------------------------------------------------*/
#ifndef INCLUDE_GUARD_VAGL_H___
#define INCLUDE_GUARD_VAGL_H___
#include <stdio.h>

#define X_SIZE (60)
#define Y_SIZE (20)

void display(char screen[Y_SIZE][X_SIZE]);
void init(char screen[Y_SIZE][X_SIZE]);

void draw_line(char screen[Y_SIZE][X_SIZE], int X0, int Y0, int X1, int Y1);
void draw_box(char screen[Y_SIZE][X_SIZE], int TopRight_X, int TopRight_Y, int BottomLeft_X, int BottomLeft_Y);
void draw_circle(char screen[Y_SIZE][X_SIZE], int X0, int X1, int Radius);

#endif // __INCLUDE_GUARD_VAGL_H___
