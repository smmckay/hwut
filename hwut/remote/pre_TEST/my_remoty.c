#include <unistd.h>
int  hwut_spy_open();
void hwut_spy_close();
int  hwut_spy_print();

int
main(int argc, char** argv)
{
    /* Note: The content of the messages is an extract of Richard Stallmans essay
     *       'Why Software Should Not Have Owners'. */
    hwut_spy_open();
    if( argc < 2 ) return 0;
   
    if( strcmp(argv[1], "--hwut-info") == 0 ) { 
        hwut_spy_print("Example remote test application.;\n");
        hwut_spy_print("CHOICES: 1, 2, 3;\n");
    }
    else if( strcmp(argv[1], "1") == 0 ) { 
        hwut_spy_print("Digital information technology contributes to the world by making it\n");
        hwut_spy_print("easier to copy and modify information. Computers promise to make\n");
        hwut_spy_print("this easier for all of us.\n");
    }
    else if( strcmp(argv[1], "2") == 0 ) { 
        hwut_spy_print("Not everyone wants it to be easier. The system of copyright gives\n");
        hwut_spy_print("software programs \"owners\", most of whom aim to withhold software's\n");
        hwut_spy_print("potential benefit from the rest of the public. They would like to be\n");
        hwut_spy_print("the only ones who can copy and modify the software that we use.<<end>>\n");
    }
    else if( strcmp(argv[1], "3") == 0 ) { 
        hwut_spy_print("The copyright system grew up with printing-a technology for\n");
        hwut_spy_print("mass production copying. Copyright fit in well with this\n");
        hwut_spy_print("technology because it restricted only the mass producers of\n");
        hwut_spy_print("copies. It did not take freedom away from readers of books.\n");
        hwut_spy_print("An ordinary reader, who did not own a printing press, could\n");
        sleep(1);
        hwut_spy_print("copy books only with pen and ink, and few readers were sued\n");
        sleep(1);
        hwut_spy_print("for that.<<end>>\n");
    }

    hwut_spy_close();
}
