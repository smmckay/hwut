/* PURPOSE: An implementation of a send function in 'C' that can send 
 *          data to a hwut application via a socket connection. 

 * AUTHOR:  Frank-Rene Schaefer (based on some code fragment which 
 *          was found in the internet).
 *
 * DATE:    01.12.2008                                               */
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <string.h>
#include <assert.h>
#include <unistd.h>   /* gets: close() */

#ifndef    HWUT_REMOTE_PORT
#   define HWUT_REMOTE_PORT  37773           /* This is **THE** default hwut port */
#endif
#ifndef    HWUT_REMOTE_HOST
#   define HWUT_REMOTE_HOST  "192.168.1.10"  /* The host where hwut is listening  */
#endif

int	hwut_spy_socket_id = -1;

int 
hwut_spy_open()
{
    struct  sockaddr_in  sin;
    struct  sockaddr_in  pin;
    struct  hostent*     host = 0x0; 
    int                  virginity_f = 1;

    /* go find out about the desired host machine */
    if( (host = gethostbyname(HWUT_REMOTE_HOST)) == 0 ) 
    { fprintf(stderr, "could not find host %s", HWUT_REMOTE_HOST); return 0; }

    /* fill in the socket structure with host information */
    memset(&pin, 0, sizeof(pin));
    pin.sin_family      = AF_INET;
    pin.sin_addr.s_addr = ((struct in_addr*)(host->h_addr))->s_addr;
    pin.sin_port        = htons(HWUT_REMOTE_PORT);

    /* grab an Internet domain socket */
    hwut_spy_socket_id = socket(AF_INET, SOCK_STREAM, 0);
    if( hwut_spy_socket_id == -1 ) 
    { fprintf(stderr, "socket failed"); return 0; }

    /* connect to PORT on HOST */
    if( connect(hwut_spy_socket_id, (struct sockaddr*)&pin, sizeof(pin)) == -1 ) 
    { fprintf(stderr, "connect failed"); return 0; }

    /* only release the virginity, if the connection was established. */
    return 1;
}

void 
hwut_spy_close()
{
    assert(hwut_spy_socket_id != -1);
    close(hwut_spy_socket_id);
}

int
hwut_spy_print(const char* Message)
{
    assert(hwut_spy_socket_id != -1);
    if( send(hwut_spy_socket_id, Message, strlen(Message), 0) == -1 ) 
    { fprintf(stderr, "send failed"); return 0; }

    return 1;
}


