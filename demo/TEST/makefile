FILES = my-file  my-file-2  my-file-3

# by default make all files
all: $(FILES)

# respond to the call of 'hwut'
hwut-info:
	@echo $(FILES)

# default compilation rule for .c files
%: %.c
	gcc -DHALLO $< -o $@

clean:
	rm $(FILES)
