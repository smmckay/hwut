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
#ifndef HWUT_INCLUDE_GUARD_REMOTE_HWUT_REMOTE_H
#define HWUT_INCLUDE_GUARD_REMOTE_HWUT_REMOTE_H

/* Test application database: 
 *
 * Map application name and choice to the function that is to be called.     */
typedef struct { 
    const char* application;
    const char* choice;
    void        (*function)(void);
} hwut_remote_db_entry_t;

#define hwut_remote_db_size(DB) (sizeof(DB)/sizeof(DB[0]))


/* The one and only function that is to be called from the remote agent that
 * handles the communication with the main HWUT application.                 */
extern void hwut_remote_run(const void* Config, 
                            hwut_remote_db_entry_t* db, int DbSize);

/* Abstract Interface:
 *
 * These functions need to be implemented according to the remote communication
 * protocol which is used to communicated between HWUT and its remote test 
 * applications.                                                             */
extern int  hwut_remote_open(const void* Config);
extern int  hwut_remote_interact(hwut_remote_db_entry_t* db, int DbSize);
extern int  hwut_remote_print(const char* Message);
extern void hwut_remote_close();

/* Definition of signals for communication with HWUT.                        */
#define HWUT_REMOTE_SETTING_QUERY_APPLICATION_LIST      "$HWUT:GET_APPS$"
#define HWUT_REMOTE_SETTING_APPLICATION_LIST            "$HWUT:APPS$"
#define HWUT_REMOTE_SETTING_EXECUTION_STOP              "$HWUT:KILL$"
#define HWUT_REMOTE_SETTING_EXECUTION_STOP_ACKNOWLEDGED "$HWUT:KILLED$"
#define HWUT_REMOTE_SETTING_TEST_BEGIN                  "$HWUT:BEGIN$"
#define HWUT_REMOTE_SETTING_TEST_UNKNOWN                "$HWUT:?$"
#define HWUT_REMOTE_SETTING_TEST_STOP                   "$HWUT:STOP$"
#define HWUT_REMOTE_SETTING_TEST_STOP_ACKNOWLEDGED      "$HWUT:STOPPED$"

#endif /* HWUT_INCLUDE_GUARD_REMOTE_HWUT_REMOTE_H */
