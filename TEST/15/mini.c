#include <stdio.h> 
#include <hwut_unit.h> 

int main(int argc, char** argv)
{    
    int*   nulley = (void*)0;

    hwut_info("False Positive Regression;\n"
              "CHOICES: ONE;");
    
    /* In the good case, the following line was not there. Now, that it is
     * the program prematurely exits with segmentation fault. The HWUT result
     * should be 'FAIL'. When this bug was reported, it did not.             */
    printf("Hallo\n");
    fflush(stdout);
    nulley[0] = 0x4711;

    hwut_if_choice("ONE") {
        printf("ONE\n");
    }
    return 0;
};

