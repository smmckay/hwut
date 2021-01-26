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

TESTS      := test-count-static.exe          \
              test-print_hello.exe #
LIBRARIES  :=  #
LIBDIRS    :=  #
OBJECTS    := one.o                          \
              two.o                          \
              three.o #
OBJECTS_0  := $(OBJECTS)                     \
              test-count-static.o #
OBJECTS_1  := $(OBJECTS)                     \
              count.o                        \
              test-print_hello.o #
INCLUDES   := -Iinclude_directory #
INCLUDES_0 := $(INCLUDES)                    \
              -Isource_directory             \
              -I../../../../../../support/C #


# Source to Object Relations __________________________________________________
#
#  test-print_hello.c         => test-print_hello.o
#  test-count-static.c        => test-count-static.o
#  source_directory/count.c   => count.o
#  source_directory/3/three.c => three.o
#  source_directory/2/two.c   => two.o
#  source_directory/1/one.c   => one.o
#______________________________________________________________________________
#

all: $(TESTS)

clean: 
	$(RM) -f $(TESTS)
	$(RM) -f $(OBJECTS)
	$(RM) -f count.o test-count-static.o test-print_hello.o 
	# OPTIONAL: $(RM) -f *~ *.bak *.info *.orig core stackdump *.tmp tmp.* *.gc*


hwut-info:
	@echo $(TESTS)

test-print_hello.exe: $(OBJECTS_1) 
	$(LD) $(OBJECTS_1) -o $@

test-count-static.exe: $(OBJECTS_0) 
	$(LD) $(OBJECTS_0) -o $@

%.o: %.c
	$(CC) $(INCLUDES_0) $< -o $@

%.o: source_directory/%.c
	$(CC) $(INCLUDES) $< -o $@

%.o: source_directory/1/%.c
	$(CC)  $< -o $@

%.o: source_directory/2/%.c
	$(CC)  $< -o $@

%.o: source_directory/3/%.c
	$(CC)  $< -o $@


