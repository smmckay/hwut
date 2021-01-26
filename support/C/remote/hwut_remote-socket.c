/* Socket-based implementation of the Abstract Interface for HWUT's remote 
 * communication:
 *
 *        hwut_remote_open()
 *        hwut_remote_interact(hwut_remote_db_entry_t* db, int DbSize)
 *        hwut_remote_print(const char*)
 *        hwut_remote_open()
 *
 * (All protocol-independent elements are implemented in 'hwut_remote.c') 
 *
 * (C) Frank-Rene Schaefer, private
 *     Frank-Rene Schaefer, Visteon, Germany, Kerpen.
 * --------------------------------------------------------------------------*/
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
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <string.h>
#include <assert.h>
#include <unistd.h>   /* gets: close() */
#include <remote/hwut_remote.h>  
#include <remote/hwut_remote-socket.h>  

extern int   hwut_remote_route_message(const hwut_remote_db_entry_t* db, 
                                       int                           DbSize, 
                                       const char*                   Message, 
                                       int                           MessageSize);
extern void  hwut_remote_on_abort();

static struct {
    int  socket_id;
    char buffer[HWUT_REMOTE_SETTING_SOCKET_RX_BUFFER_SIZE];
} self;

static void self_on_abort(int);

int 
hwut_remote_open(const void* Config)
/* Open the connection to the listening HWUT application. The HWUT engine may
 * reside on a computer with multiple IP addresses and it is not clear from 
 * where this client connects to it. So, this function tries all interfaces
 * mentioned in 'config.ip_where_hwut_resides[]'.
 *
 * RETURNS: 1 -- success.
 *          0 -- else.                                                       */
{
    struct sockaddr_in  sa_in;
    struct hostent*     host = 0x0; 
    const  char*        ip_address; 
    int    i;

    /* The caller of 'hwut_remote_run()' must have casted the 'config' of type
     * 'hwut_remote_configuration_socket_t' to 'void*' which is now casted
     * back to its initial type.                                             */
    const  hwut_remote_configuration_socket_t* config = (hwut_remote_configuration_socket_t*)Config;

    /* 
     * assert(config->ip_alternative_n <= HWUT_REMOTE_SETTING_SOCKET_IP_MAX_ALTERNATIVE_N);
     */

    self.socket_id = -1;

    for(i = 0; i < config->ip_alternative_n ; ++i) {
        ip_address = config->ip_where_hwut_resides[i];
        /* Find out about the desired host machine                           */
        if( ! (host = gethostbyname(ip_address)) ) 
            continue

        /* Fill in the socket structure with host information                */
        memset(&sa_in, 0, sizeof(sa_in));
        sa_in.sin_family      = AF_INET;
        sa_in.sin_addr.s_addr = ((struct in_addr*)(host->h_addr))->s_addr;
        sa_in.sin_port        = htons(config->port_where_hwut_listens);

        /* make sure that the socket is closed upon exit                     */
        signal(SIGQUIT, self_on_abort);

        /* grab an Internet domain socket                                    */
        self.socket_id = socket(AF_INET, SOCK_STREAM, 0);
        if( self.socket_id == -1 ) 
            continue;

        /* connect to PORT on HOST                                           */
        if( connect(self.socket_id, (struct sockaddr*)&sa_in, sizeof(sa_in)) == -1 ) 
            continue;
    }

    /* socket == -1 => Could not connect to any given ip addresses.          */
    return self.socket_id != -1;
}

int
hwut_remote_interact(hwut_remote_db_entry_t* db, int DbSize)
/* Interact with the remote-listening HWUT application. That is, messages are
 * received and interpreted. Then, a callback is called according the the
 * messages content given by two words:
 *
 *    1st word: application name
 *    2nd word  choice name
 *
 * The callback is determined based on those and searching in the 'db'. When
 * '$HWUT:KILL$' is received this function exits. After the execution of a 
 * function (given by application name and choice), the string '$HWUT:END$'
 * is send to the listening HWUT application. All of this happens actually
 * in the function 'hwut_remote_route_message()' which is protocol independent.
 *
 * RETURNS: 1 -- no termination, but error.
 *          0 -- termination requested.                                      */
{
    ssize_t   length;

    assert(self.socket_id != -1);
    assert(sizeof(self.buffer) >= 1);

    while( 1 + 1 == 2 ) {
        length = recv(self.socket_id, &self.buffer[0], sizeof(self.buffer)-1, 0);
        if( length == -1 ) 
            return 1;
        /* Store a terminating zero.                                         */
        self.buffer[length] = '\0';
        if( ! hwut_remote_route_message(db, DbSize, self.buffer, sizeof(self.buffer)) ) 
            return 0;
    }
}

int
hwut_remote_print(const char* Message)
/* Sends a zero terminated string to the listening HWUT application. 
 *
 * RETURNS: 1 -- success.
 *          0 -- else.                                                       */
{
    assert(self.socket_id != -1);

    /* NEVER send ZERO bytes, because, this would CLOSE the connection.      */
    if( ! Message || *Message == '\0' ) return 0;

    else if( send(self.socket_id, Message, strlen(Message), 0) == -1 ) return 0; 

    return 1;
}

void 
hwut_remote_close()
/* Closes the connection to the listening HWUT application.
 *
 * RETURNS: 1 -- success.
 *          0 -- else.                                                       */
{
    if( self.socket_id == -1 ) return;
    close(self.socket_id);
    self.socket_id = -1;
}

static void
self_on_abort(int Signal)
/* When the communication is aborted, some things remain to be done. Try to
 * send at least some good-bye messages to the listening HWUT application and
 * close all open sockets.                                                   */
{
    (void)Signal;

    hwut_remote_on_abort(); /* Common actions, protocol independent.         */

    printf("Closing socket.\n");
    if( self.socket_id != -1 ) close(self.socket_id);
}

