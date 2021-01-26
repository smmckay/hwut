FILES = \
		test-table.exe    \
		test-object.exe   \
		test-bitfield.exe \
		test-bitfield_list.exe \
		test-get_bit_range.exe \
		test-grid.exe \
		test-hwut_unit.exe

SRC=../src

HDR=../

SOURCES = \
		scanner.c        \
		graph.c          \
		display.c        \
		canvas.c         \
		bitfield.c       \
		bitfield_list.c  \
		table.c          \
		object.c         \
		grid.c       

OUT = \

OBJS=$(SOURCES:.c=.o)

CC=gcc -Wall -ggdb # -ggdb # -Os # -ggdb

all: $(FILES)

hwut-info: 
	@echo $(FILES)

%.exe: %.o libHWUTGraph.a
	$(CC) $< libHWUTGraph.a -o $@

%.o: %.c $(HDR)/hwut_graph.h $(HDR)/hwut_scanner.h
	$(CC) -c $< -o $@ -I$(HDR)

libHWUTGraph.a: $(OBJS)
	ar -rc libHWUTGraph.a $(OBJS)

libHWUTGraph.so: $(OBJS)
	$(CC) -shared -o libHWUTGraph.so $(OBJS)

%.o: $(SRC)/%.c $(HDR)/hwut_graph.h $(HDR)/hwut_scanner.h
	$(CC) -c $< -o $@ -I$(HDR)

%.E: %.c 
	$(CC:-c=-E) -c $< -o $@ -I$(HDR)

clean:
	rm -f $(FILES)
	rm -f $(FILES:.exe=.o)
	rm -f $(FILES:.exe=.E)
	rm -f $(OBJS)
	rm -f *.exe
	rm -f libHWUTGraph.*
	rm -f *.stackdump
	rm -f *~

