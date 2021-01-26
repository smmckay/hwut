FILES = \
		test-DB_OpenNode_enter.exe     \
		test-DB_OpenNode_remove.exe    \
		test-DB_OpenNode_adapt_path_info.exe \
		test-Path-solve.exe    

OUT = \
		test-NodeSet-enter.exe      \
		test-NodeSet-remove.exe     \
		test-ScoreInfoDB-find.exe   \
		test-ScoreInfoDB-enter.exe  \
		test-Path-solve.exe    

SRC=../src
GSRC=../../src

HDR=../../

SOURCES = \
		  DB_NodeXY.c     \
		  DB_NodeFScore.c \
		  DB_OpenNode.c   \
		  Path.c        

OBJS=$(SOURCES:.c=.o)

CC=gcc -Wall -ggdb # -ggdb # -Os # -ggdb

all: $(FILES)

hwut-info: 
	@echo $(FILES)

%.exe: %.o $(OBJS) ../../out/libHWUT_helper-base.a
	$(CC) $< $(OBJS) ../../out/libHWUT_helper-base.a -o $@

%.o: %.c $(HDR)/hwut_graph.h $(HDR)/hwut_scanner.h
	$(CC) -c $< -o $@ -I$(HDR) -I../ -I../header/

%.o: $(SRC)/%.c $(HDR)/hwut_graph.h $(HDR)/hwut_scanner.h
	$(CC) -c $< -o $@ -I$(HDR) -I../ -I../header/

../../out/libHWUT_helper-base.a:
	cd ../../out/
	make libHWUT_helper.a

clean:
	rm -f $(FILES)
	rm -f $(FILES:.exe=.o)
	rm -f $(OBJS)
	rm -f *.exe
	rm -f *.stackdump
	rm -f *~

