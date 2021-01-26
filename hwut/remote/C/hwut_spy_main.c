int  hwut_spy_open();
void hwut_spy_close();
void hwut_spy_print(const char*);

int
main(int argc, char** argv)
{
    if( argc < 2 ) return 0;

    hwut_spy_open();
    hwut_spy_print(argv[1]);
    hwut_spy_close();
}

