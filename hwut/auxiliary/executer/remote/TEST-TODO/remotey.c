#include <unistd.h>
#include <stdlib.h>
#include <remote/hwut_remote.h>
#include <remote/hwut_remote-socket.h>

static void test0_hwut_info();
static void test0_function_a();
static void test0_function_b();
static void test1_hwut_info();
static void test1_function_c();

hwut_remote_db_entry_t test_db[] = {
    { "test0", "--hwut-info", test0_hwut_info },
    { "test0", "A",           test0_function_a },
    { "test0", "B",           test0_function_b },
    { "test1", "--hwut-info", test1_hwut_info },
    { "test1", "",            test1_function_c },
};

hwut_remote_configuration_socket_t config;

int
main(int argc, char** argv)
/** ARG1:      Port number where HWUT is listening.
 *  ARG2-ARGC: Alternative ip addresses which are provided by the host on 
 *             which HWUT is listening.                                      */
{
    int i;

    if( argc < 3 ) return -1;
   
    /* Parse the command line to get information about the HWUT host.        
     * => Port number where HWUT listens
     * => Interfaces (IP addresses) where HWUT listens on its host.          */
    config.port_where_hwut_listens = atoi(argv[1]);
    for(i = 2; 
        i < argc && i - 2 < HWUT_REMOTE_SETTING_SOCKET_IP_MAX_ALTERNATIVE_N; 
        ++i) {
        config.ip_where_hwut_resides[i-2] = argv[i];
    }
    /* config.ip_alternative_n = argc - 2; */

    /* Start the HWUT test client.                       
     *
     * 'config' is protocol-specific, but casted to 'void*'
     *          => 'config' can pass through the general interface. 
     *          The low-level implementation will cast it back to 
     *          'hwut_remote_configuration_socket_t*'.                       */
    hwut_remote_run((void*)&config, &test_db[0], 
                    hwut_remote_db_size(test_db));
    return 0;
}

static void
test0_hwut_info()
{
    hwut_remote_print("1st example remote test application.;\n");
    hwut_remote_print("CHOICES: A, B;\n");
}

static void
test1_hwut_info()
{
    hwut_remote_print("2nd example remote test application;\n");
}

/* "Today Is Very Boring".
 *  By Jack Prelutsky.                                                       */
static void
test0_function_a()
{
    hwut_remote_print("Today is very boring,\n"); 
    hwut_remote_print("it’s a very boring day,\n"); 
    hwut_remote_print("there is nothing much to look at,\n"); 
    hwut_remote_print("there is nothing much to say,\n"); 
    hwut_remote_print("there’s a peacock on my sneakers,\n"); 
    hwut_remote_print("there’s a penguin on my head,\n"); 
    hwut_remote_print("there’s a dormouse on my doorstep,\n"); 
    hwut_remote_print("I am going back to bed.\n"); 
}

static void
test0_function_b()
{
    hwut_remote_print("Today is very boring,\n"); 
    hwut_remote_print("it is boring through and through,\n"); 
    hwut_remote_print("there is absolutely nothing\n"); 
    hwut_remote_print("that I think I want to do,\n"); 
    hwut_remote_print("I see giants riding rhinos,\n"); 
    hwut_remote_print("and an ogre with a sword,\n"); 
    hwut_remote_print("there’s a dragon blowing smoke rings,\n"); 
    hwut_remote_print("I am positively bored.\n"); 
}

static void
test1_function_c()
{
    hwut_remote_print("Today is very boring,\n"); 
    sleep(0);
    hwut_remote_print("I can hardly help by yawn,\n"); 
    sleep(0);
    hwut_remote_print("there’s a flying saucer landing\n"); 
    sleep(0);
    hwut_remote_print("in the middle of my lawn,\n"); 
    sleep(0);
    hwut_remote_print("a volcano just erupted\n"); 
    sleep(0);
    hwut_remote_print("less than half a mile away,\n"); 
    sleep(0);
    hwut_remote_print("and I think I felt an earthquake,\n"); 
    sleep(0);
    hwut_remote_print("it’s a very boring day.\n"); 
}
