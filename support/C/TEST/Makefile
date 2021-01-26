FILES = \
		test-hwut_unit.exe        \
		test-hwut_cursor.exe      \
		test-hwut_bitfield.exe    \
		test-hwut_bitfield-iterator.exe  \
		test-hwut_bitfield-iterator2.exe  \
        test-hwut_sm_walker.exe   \
        test-hwut_sm_walker-2.exe \
        test-hwut_sm_walker-3.exe \
        test-hwut_sm_walker-4.exe \
        test-hwut_sm_walker-5.exe \
        test-hwut_sm_walker-6.exe \
        test-hwut_sm_walker-forbidd-allow.exe \
        test-hwut_sm_walker-inconsistent-condition.exe \
        test-hwut_sm_walker-condition-norms.exe \
        test-hwut_sm_walker-condition-norms-negative.exe \
        test-hwut_sm_walker-coverage.exe \
        test-hwut_sm_walker-print.exe

SRC=..#
HDR=..#

ifdef SystemRoot
	# Windows
	HWUT_EXE=$(HWUT_PATH)/hwut.bat
else
	HWUT_EXE=python $(HWUT_PATH)/hwut-exe.py
endif

SOURCES = \
	hwut_sm_walker.c \
        hwut_bitfield.c \
        hwut_cursor.c

# OBJS=$(addprefix ./obj/, $(SOURCES:.c=.o))
OBJS=$(SOURCES:.c=.o)
.SECONDARY: $(OBJS)

#HWUT_GCOV=-DNDEBUG

CC=gcc -Wall -Werror -I$(HDR) -fprofile-arcs -ftest-coverage $(HWUT_GCOV) -ggdb # -Os 

LD=gcc -ggdb

all: $(FILES)

hwut-info: 
	@echo $(FILES)

test-hwut_cursor.exe: test-hwut_cursor.o $(OBJS)
	$(LD) $< $(OBJS:hwut_cursor.o=) -lgcov -o $@

test-hwut_bitfield-%.exe: test-hwut_bitfield-%.o $(OBJS)
	$(LD) $< $(OBJS:hwut_bitfield.o=) -lgcov -o $@

test-hwut_bitfield.exe: test-hwut_bitfield.c $(OBJS)
	@$(HWUT_EXE) gen $< -o BitFieldIterator
	$(CC) $< $(OBJS) BitFieldIterator.c -o $@ 

%.exe: %.o $(OBJS)
	$(LD) $< $(OBJS) -lgcov -o $@

# ./obj/%.o: %.c 
test-hwut_unit.o: test-hwut_unit.c 
	$(CC) -c $< -o $@ -I$(HDR) -DHWUT_OPTION_CONTINUE_ON_FAIL

# ./obj/%.o: %.c 
%.o: %.c 
	$(CC) -c $< -o $@ -I$(HDR)

# ./obj/%.o: $(SRC)/%.c 
%.o: $(SRC)/%.c 
	$(CC) -c $< -o $@ -I$(HDR)

%.E: %.c 
	$(CC:-c=-E) -c $< -o $@ -I$(HDR)

	

clean:
	rm -f $(FILES)
	rm -f $(FILES:.exe=.o)
	rm -f $(FILES:.exe=.E)
	rm -f $(OBJS)
	rm -rf ./obj/*
	rm -f *.exe
	rm -f *.orig *.bak *.stackdump 
	rm -f *.gc*
	rm -f *.info
	rm -f *~
	rm -f BitFiterator*

