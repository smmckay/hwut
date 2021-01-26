RM := rm

LD := gcc
# Useful additional flags:
#    -ggdb              -- gdb-debugger information embedded
#    --coverage         -- for coverage analysis (lcov, gcov etc.) 
#    -fsanitize=address -- fast memory error detector

CC := gcc -c
# Useful additional flags:
#    -ggdb              -- gdb-debugger information embedded
#    -Wall              -- all warnings enabled
#    -Wimplicit         -- warn on implicit declarations
#    -pedantic          -- be pedantic
#    -Werror            -- raise all warnings as errors
#    --coverage         -- for coverage analysis (lcov, gcov etc.)
#    -std=c99           -- for C99 compliance
#    -fno-inline        -- avoid inlining, implement seperate functions
#    -fsanitize=address -- fast memory error detector

TESTS      := main2.exe              \
              main.exe #
LIBRARIES  :=  #
LIBDIRS    :=  #
OBJECTS    := common_file_name_1.o   \
              number.o               \
              common_file_name_0.o   \
              letter.o               \
              hwut-crash-on-call.o #
OBJECTS_0  := $(OBJECTS)             \
              main2.o #
OBJECTS_1  := $(OBJECTS)             \
              main.o #
INCLUDES   := -I1/12/123/1234/12345  \
              -IA/AB/ABC/ABCD        \
              -Iextra #
INCLUDES_0 := $(INCLUDES)            \
              -Iextra/more #


# Source to Object Relations __________________________________________________
#
#  main2.c                                => main2.o
#  main.c                                 => main.o
#  hwut-crash-on-call.c                   => hwut-crash-on-call.o
#  A/AB/ABC/ABCD/letter.c                 => letter.o
#              */common_file_name.c       => common_file_name_0.o
#  1/12/123/1234/12345/number.c           => number.o
#                    */common_file_name.c => common_file_name_1.o
#______________________________________________________________________________
#

all: $(TESTS)

clean: 
	$(RM) -f $(TESTS)
	$(RM) -f $(OBJECTS)
	$(RM) -f main.o main2.o 
	# OPTIONAL: $(RM) -f *~ *.bak *.info *.orig core stackdump *.tmp tmp.* *.gc*


hwut-info:
	@echo $(TESTS)

main.exe: $(OBJECTS_1) 
	$(LD) $(OBJECTS_1) -o $@

main2.exe: $(OBJECTS_0) 
	$(LD) $(OBJECTS_0) -o $@

%.o: %.c
	$(CC) $(INCLUDES) $< -o $@

%.o: 1/12/123/1234/12345/%.c
	$(CC) $(INCLUDES_0) $< -o $@

%.o: A/AB/ABC/ABCD/%.c
	$(CC) $(INCLUDES) $< -o $@

%_0.o: A/AB/ABC/ABCD/%.c
	$(CC) $(INCLUDES) $< -o $@

%_1.o: 1/12/123/1234/12345/%.c
	$(CC) $(INCLUDES_0) $< -o $@


