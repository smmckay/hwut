CC := gcc -ggdb -Wall \
      -I$(HWUT_PATH)/hwut/generator/templates/c/ \
      -I$(HWUT_PATH)/support/C

FILES := total-sm_walker.exe

ifdef SystemRoot
	# Windows
	HWUT_EXE=$(HWUT_PATH)/hwut.bat
else
	HWUT_EXE=python $(HWUT_PATH)/hwut-exe.py
endif

all: $(FILES)

total-sm_walker.exe: total-sm_walker.c 
	$(HWUT_EXE) generator total-sm_walker.c -o myWalk_sm_walker
	$(CC) $^ myWalk_sm_walker.c \
    $(HWUT_PATH)/support/C/hwut_sm_walker.c -o $@ \
    -I$(HWUT_PATH)/support/C

hwut-info:
	@echo $(FILES)

clean:
	rm -f $(FILES)
	rm -f myGen_iterator.*
	rm -f myWalk_sm_walker.*
	rm -f *~ 
	rm -f *.bak *.orig tmp.*
