CC := gcc -ggdb -Wall \
      -I$(HWUT_PATH)/hwut/generator/templates/c/ \
      -I$(HWUT_PATH)/support/C

FILES := total.exe 

ifdef SystemRoot
	# Windows
	HWUT_EXE=$(HWUT_PATH)/hwut.bat
else
	HWUT_EXE=python $(HWUT_PATH)/hwut-exe.py
endif

all: $(FILES)

total.exe: total.c 
	$(HWUT_EXE) generator total.c -o myGen_iterator
	$(CC) $^ myGen_iterator.c \
          $(HWUT_PATH)/support/C/hwut_cursor.c \
          -o $@ -I$(HWUT_PATH)/support/C

%.exe: %.c
	$(CC) $< -o $@ 


hwut-info:
	@echo $(FILES)

clean:
	rm -f $(FILES)
	rm -f myGen_iterator.*
