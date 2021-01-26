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
#include <remote/hwut_remote.h>
#include <unistd.h>

typedef struct {
    const char*  app_begin_p;
    const char*  app_end_p;
    const char*  choice_begin_p;
    const char*  choice_end_p;
} self_app_and_choice_t; 

static void         self_app_and_choice_construct(self_app_and_choice_t* ac, 
                                                  const char*            Message, 
                                                  const char*            MessageEnd);
static int          self_control_command(self_app_and_choice_t*        ac,
                                         const hwut_remote_db_entry_t* db, 
                                         const hwut_remote_db_entry_t* End,    
                                         int*                          quit_f);
static int          self_execute_application(self_app_and_choice_t*        ac,
                                             const hwut_remote_db_entry_t* db, 
                                             const hwut_remote_db_entry_t* End);    
static void         self_report_application_list(const hwut_remote_db_entry_t* db, 
                                                 const hwut_remote_db_entry_t* End);
static int          self_is_hit(self_app_and_choice_t* ac, 
                                const char* App, const char* Choice); 

static const char*  self_skip_space(const char** p, const char* End);
static const char*  self_skip_non_space(const char** p, const char* End);
static int          self_is_equal(const char* A_zero_terminated, 
                                  const char* B_begin, 
                                  const char* B_end);
static const char*  self_get_pointer_to_next_zero(const char*);

void
hwut_remote_run(const void* Config, hwut_remote_db_entry_t* db, int DbSize)
/* Initiates, runs, and closes a communication with a listening HWUT
 * application. Functions implementating applictions and choices are 
 * listed in the 'db' of size 'DbSize'.                                      */
{
    while( ! hwut_remote_open(Config) ) { 
        sleep(1);
    }

    while( hwut_remote_interact(db, DbSize) ) {
    }

    hwut_remote_close();
}

int
hwut_remote_route_message(const hwut_remote_db_entry_t* db, 
                          int                           DbSize, 
                          const char*                   Message, 
                          int                           MessageSize)
/* Analyzes the 'Message', i.e. takes the first two words of it and
 * interpretes it as application and choice. 
 *
 * SENDS:   "$HWUT:DEAD$"   if the application's name is '$HWUT:KILL$' 
 *          "$HWUT:?$"      if the application/choice pair was not found.
 *          "$HWUT:END$"    when a function has been called and it returned.
 *                          I.e. this marks the END of a test's output.
 *
 * RETURNS: 1 -- still no '$HWUT:KILL$' received. 
 *          0 -- received '$HWUT:KILL$.                                      */
{
    const hwut_remote_db_entry_t* End = &db[DbSize];
    self_app_and_choice_t         ac;
    int                           quit_f;

    self_app_and_choice_construct(&ac, Message, &Message[MessageSize]);

    if( self_control_command(&ac, db, End, &quit_f) ) { 
        return quit_f ? 0 : 1;
    }
    else if( ! self_execute_application(&ac, db, End) ) {
        hwut_remote_print(HWUT_REMOTE_SETTING_TEST_UNKNOWN);
    }

    return 1;

}

static int  
self_control_command(self_app_and_choice_t*        ac, 
                     const hwut_remote_db_entry_t* db, 
                     const hwut_remote_db_entry_t* End,    
                     int*                          quit_f) 
/* RETURNS: true, if a control command has been received and handled.
 *          false, else.
 *
 * (*quit_f) == true, if the application is requested to quit.
 *           == false, else.                                                 */
{
    if( self_is_hit(ac, HWUT_REMOTE_SETTING_TEST_STOP, "") ) { 
        hwut_remote_print(HWUT_REMOTE_SETTING_TEST_STOP_ACKNOWLEDGED);
        *quit_f = 0;
    }
    else if( self_is_hit(ac, HWUT_REMOTE_SETTING_EXECUTION_STOP, "") ) { 
        hwut_remote_print(HWUT_REMOTE_SETTING_EXECUTION_STOP_ACKNOWLEDGED);
        *quit_f = 1;
    }
    else if( self_is_hit(ac, HWUT_REMOTE_SETTING_QUERY_APPLICATION_LIST, "") ) { 
        self_report_application_list(db, End);
        *quit_f = 0;
    }
    else {
        return 0;
    }
    return 1;
}

static int          
self_execute_application(self_app_and_choice_t*        ac, 
                         const hwut_remote_db_entry_t* db, 
                         const hwut_remote_db_entry_t* End)    
{
    const hwut_remote_db_entry_t* it; 

    /* Find the function pointer that belongs to the application/choice.     */
    for(it = &db[0]; it != End; ++it) { 
        if( self_is_hit(ac, it->application, it->choice) ) {
            hwut_remote_print(HWUT_REMOTE_SETTING_TEST_BEGIN);
            (*it->function)();
            hwut_remote_print(HWUT_REMOTE_SETTING_TEST_STOP_ACKNOWLEDGED);
            return 1;
        }
    }
    return 0;
}

static void 
self_report_application_list(const hwut_remote_db_entry_t* db, 
                             const hwut_remote_db_entry_t* End)
/* Sends the list of applications listed in the database using the 
 * 'hwut_remote_print' command. Applications are separated by ';'.           */
{
    const hwut_remote_db_entry_t* it; 
    const char*                   previous_begin_p = "";
    const char*                   previous_end_p = "";

    hwut_remote_print(HWUT_REMOTE_SETTING_TEST_BEGIN);

    for(it = &db[0]; it != End; ++it) { 
        if( self_is_equal(it->application, previous_begin_p, previous_end_p) ) continue;
        hwut_remote_print(it->application);
        hwut_remote_print(";");

        previous_begin_p = it->application;
        previous_end_p   = self_get_pointer_to_next_zero(it->application);
    }

    hwut_remote_print(HWUT_REMOTE_SETTING_TEST_STOP_ACKNOWLEDGED);
}

void
hwut_remote_on_abort()
/* Upon abort, make sure that the listening HWUT application gets informed 
 * about the terminated test and the terminating communication interface.    */
{
    hwut_remote_print(HWUT_REMOTE_SETTING_TEST_STOP_ACKNOWLEDGED);
    hwut_remote_print(HWUT_REMOTE_SETTING_EXECUTION_STOP_ACKNOWLEDGED);
}

static void
self_app_and_choice_construct(self_app_and_choice_t* ac, 
                              const char*            p, 
                              const char*            MsgEnd)
{
    ac->app_begin_p    = self_skip_space(&p, MsgEnd); 
    ac->app_end_p      = self_skip_non_space(&p, MsgEnd);
    ac->choice_begin_p = self_skip_space(&p, MsgEnd);
    ac->choice_end_p   = self_skip_non_space(&p, MsgEnd);
}

static int
self_is_equal(const char* A_zero_terminated, 
              const char* B_begin, const char* B_end)
/* RETURNS: true  -- if the zero terminated string in 'A_zero_terminated' is
 *                   equal to the begin/end bordered string 'B_*'.
 *          false -- else.                                                   */
{
    const char* a_p = A_zero_terminated;
    const char* b_p = B_begin;
    
    while( *a_p && b_p != B_end ) {
        if( *a_p++ != *b_p++ ) return 0;
    }
    /* When both pointers stand at the end, then the string where equal.     */
    return (! *a_p) && (b_p == B_end);
}

static int 
self_is_hit(self_app_and_choice_t* ac, const char* App, const char* Choice) 
/* RETURNS: true  -- if the given application name and choice name match 
 *                   the application and choice of the given entry. 
 *          false -- else.                                                   */
{
    if( ! self_is_equal(App, ac->app_begin_p, ac->app_end_p) ) {
        return 0;
    }

    return self_is_equal(Choice, ac->choice_begin_p, ac->choice_end_p);
}

static const char*
self_skip_space(const char** p, const char* End)
{
    const char* it;
    for(it = *p; it != End; ++it) {
        if( ! *it ) { *p = it; break; }
        else if( *it != ' ' && *it != '\t' && *it != '\n' ) { *p = it; break; }
    }
    return it;
}

static const char*
self_skip_non_space(const char** p, const char* End)
{
    const char* it;
    for(it = *p; it != End; ++it) {
        if( ! *it ) { *p = it; break; }
        else if( *it == ' ' || *it == '\t' || *it == '\n' ) { *p = it; break; }
    }
    return it;
}

static const char*  
self_get_pointer_to_next_zero(const char* BeginP)
{
    const char* p = BeginP;
    while( *p ) ++p;
    return p;
}
