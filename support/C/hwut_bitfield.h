/*  SPDX license identifier: LGPL-2.1
 * 
 *  Copyright (C) Frank-Rene Schaefer, private.
 *  Copyright (C) Frank-Rene Schaefer, 
 *                Visteon Innovation&Technology GmbH, 
 *                Kerpen, Germany.
 * 
 *  This file is part of "HWUT -- The hello worldler's unit test".
 * 
 *                   http://hwut.sourceforge.net
 * 
 *  This file is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU Lesser General Public
 *  License as published by the Free Software Foundation; either
 *  version 2.1 of the License, or (at your option) any later version.
 * 
 *  This file is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 *  Lesser General Public License for more details.
 * 
 *  You should have received a copy of the GNU Lesser General Public
 *  License along with this file; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor,
 *  Boston, MA 02110-1301 USA
 * 
 * --------------------------------------------------------------------------*/
#ifndef INCLUDE_GUARD_HWUT_BITFIELD_H
#define INCLUDE_GUARD_HWUT_BITFIELD_H
#include <inttypes.h>
#include <stddef.h>

extern int  hwut_bitfield_encode(uint8_t* array, size_t array_size, ...);
extern int  hwut_bitfield_decode(const uint8_t* array, size_t array_size, ...);
extern void hwut_bitfield_print_bytes(const uint8_t* array, size_t ArraySize);
extern void hwut_bitfield_print_numeric(const uint8_t* array, size_t ArraySize, const int Base, ...);
extern void hwut_bitfield_print_borders(const uint8_t* array, size_t ArraySize, ...);

#endif /* INCLUDE_GUARD_HWUT_BITFIELD_H */
