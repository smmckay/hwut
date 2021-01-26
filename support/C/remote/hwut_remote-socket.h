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
#ifndef HWUT_INCLUDE_GUARD_REMOTE_HWUT_REMOTE_SOCKET_H
#define HWUT_INCLUDE_GUARD_REMOTE_HWUT_REMOTE_SOCKET_H

#ifndef    HWUT_REMOTE_SETTING_SOCKET_RX_BUFFER_SIZE 
#  define  HWUT_REMOTE_SETTING_SOCKET_RX_BUFFER_SIZE      64
#endif

/* Maximum number of alternative IP addresses which may be tried to connect
 * to a HWUT tester. This determines the size of a configuration array.      */
#ifndef    HWUT_REMOTE_SETTING_SOCKET_IP_MAX_ALTERNATIVE_N 
#  define  HWUT_REMOTE_SETTING_SOCKET_IP_MAX_ALTERNATIVE_N    8
#endif

typedef struct {
    const char*  (ip_where_hwut_resides[HWUT_REMOTE_SETTING_SOCKET_IP_MAX_ALTERNATIVE_N]);
    int          port_where_hwut_listens;
} hwut_remote_configuration_socket_t;

#endif /* HWUT_INCLUDE_GUARD_REMOTE_HWUT_REMOTE_SOCKET_H */
