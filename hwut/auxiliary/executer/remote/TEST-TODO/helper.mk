remotey.exe: remotey.c
	gcc -Wall -Werror -ggdb -I$(HWUT_PATH)/support/C \
		$< \
		$(HWUT_PATH)/support/C/remote/hwut_remote.c \
		$(HWUT_PATH)/support/C/remote/hwut_remote-socket.c \
	   	-o $@ 
	cp mv ./pseudo/remote/location/

clean:
	rm -f *.exe
	rm -f ./pseudo/remote/location/*
