
# (*) FILES related to project
FILES := mini.exe
CC    := gcc -ggdb#
# (*) RULES
all: $(FILES)
	@echo "[RULE] all: $(FILES)"

hwut-info:
	@echo $(FILES)

%.exe: %.c 
	$(CC) -I$(HWUT_PATH)/support/C $< -o $@ 

clean:
	@echo "[RULE] clean:"
	rm -f $(OBJECTS)
	rm -f $(FILES)
	rm -f *~
	rm -f *.o *.obj
