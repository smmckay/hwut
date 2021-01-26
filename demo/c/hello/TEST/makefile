FILES = my-file.exe  my-file-2.exe  my-file-3.exe

# CC = C:\MinGW\bin\gcc.exe
CC := gcc

# by default make all files
all: $(FILES)

# respond to the call of 'hwut'
hwut-info:
	@echo $(FILES)

# default compilation rule for .c files
%.exe: %.c
	$(CC) -DHALLO $< -o $@

clean:
	rm $(FILES)
