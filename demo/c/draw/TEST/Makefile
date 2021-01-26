# (*) COMPILER SETUP
INCLUDE_PATH = -I../headers

# SHELL    = C:\WINDOWS\System32\cmd.exe
# COMPILER = C:\MinGW\bin\mingw32-gcc.exe

COMPILER = gcc

CC = $(COMPILER) -fprofile-arcs -ftest-coverage $(INCLUDE_PATH)


# (*) FILES relaed to project
FILES      = box.exe box-2.exe
VAGL_FILES = display.o drawing.o

# (*) RULES
all: $(FILES)
	@echo "[RULE] all: $(FILES)"

hwut-info:
	@echo $(FILES)

hwut-gcov-info:
	@echo $(VAGL_FILES:.o=.c)

hwut-gcov-obj:
	@echo ./

hwut-gcov-funcs:
	@echo draw_circle \
          init        \
          display     \
          __safe_set  \
          draw_box
         
%.o: %.c
	@echo "[RULE] %.o: %.c"
	$(CC) -c $< -o $@

%.o: ../%.c
	@echo "[RULE] %.o: %.c"
	$(CC) -c $< -o $@

%.exe: %.c $(VAGL_FILES)
	@echo "[RULE] %.exe: %.c"
	$(CC) $< $(VAGL_FILES) -lm -o $@

clean:
	@echo "[RULE] clean:"
	rm -f $(VAGL_FILES)
	rm -f $(FILES)
	rm -f *~
	rm -f *.o *.obj
	rm -f *.gcda *.gcno *.gcov
	rm -f *.info

