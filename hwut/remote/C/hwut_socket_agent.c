/* PURPOSE: An implementation of a HWUT agent on a target which 
 *          can start applications as desired by HWUT on the remote host.

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
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>   /* gets: close() */

#define PORT  37773           /* This is **THE** default hwut port */
#define HOST  "192.168.1.11"  /* The host where hwut is listening  */

int	 socket_id   = -1;
int	 socket_id_2 = -1;

int
on_interupt()
{
    printf("Closing socket.\n");
    if( socket_id   != -1 ) close(socket_id);
    if( socket_id_2 != -1 ) close(socket_id_2);
}



int
main(int argc, char** argv)
{
    char                 message[4096];
    int                  length = 0;
    struct  sockaddr_in  sin;
    size_t               pin_size = 0;
    struct  sockaddr_in  pin;
    struct  hostent*     host = 0x0; 
    int                  virginity_f = 1;

    /* go find out about the desired host machine */
    if( (host = gethostbyname(HOST)) == 0 ) 
    { fprintf(stderr, "could not find host %s", HOST); return 0; }

    /* grab an Internet domain socket */
    if( (socket_id = socket(AF_INET, SOCK_STREAM, 0)) == -1 ) 
    { fprintf(stderr, "socket failed"); return 0; }

    sin.sin_family      = AF_INET;
    sin.sin_port        = htons(PORT);
    sin.sin_addr.s_addr = INADDR_ANY;

    /* connect to PORT on HOST */
    if( bind(socket_id, (struct sockaddr *)&sin, sizeof(sin)) == -1 ) 
    { fprintf(stderr, "binding input port failed"); return 0; }

    listen(socket_id, 1);

    /* read incoming commandos and execute them */
    while( 1 + 1 == 2 ) { 
        pin_size = sizeof(pin);
        if ( (socket_id_2 = accept(socket_id, (struct sockaddr *)&pin, &pin_size)) < 0) {
            fprintf(stderr, "Accept failed\n");
            exit(1);
        }

        /* send a message to the server PORT on machine HOST */
        length = recv(socket_id_2, message, sizeof(message), 0);
        if( length == -1 ) { 
            fprintf(stderr, "receive failed"); return 0; 
        }
        message[length] = '\0'; /* terminating zero */
        printf("Execute: <%s>\n", message);
        system(message);
        close(socket_id_2);
        socket_id_2 = -1;
    }

    /* close(socket_id); HWUT closes the connection by itself. */
    close(socket_id);

    return 0;
}


