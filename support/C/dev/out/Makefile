SRC=$(HWUT_PATH)/support/C/src

HDR=$(HWUT_PATH)/support/C/

SOURCES = \
		scanner.c    \
		graph.c      \
		display.c    \
		canvas.c     \
		bitfield.c   \
		table.c      \
		object.c     \
		grid.c       

OBJS=$(SOURCES:.c=.o)

CC=gcc -Wall -ggdb # -ggdb # -Os # -ggdb

all: libHWUT_helper-base.a

hwut-info: 
	@echo $(FILES)

libHWUT_helper-base.a: $(OBJS)
	ar -rc libHWUT_helper-base.a $(OBJS)

libHWUT_helper-base.so: $(OBJS)
	$(CC) -shared -o libHWUT_helper-base.so $(OBJS)

%.o: $(SRC)/%.c $(HDR)/hwut_graph.h $(HDR)/hwut_scanner.h
	$(CC) -c $< -o $@ -I$(HWUT_PATH)

clean:
	rm -f $(FILES)
	rm -f $(FILES:.exe=.o)
	rm -f $(OBJS)
	rm -f *.exe
	rm -f libHWUT_helper-base.*
	rm -f *.stackdump
	rm -f *~

