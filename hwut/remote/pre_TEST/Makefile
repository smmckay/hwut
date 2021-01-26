all: my_remoty

hwut-info:
	@echo my_remoty

hwut-remote:
	@echo "SPY:   TCP;"
	@echo "AGENT: TCP, Adr=192.168.1.11, Path=/host/;"

my_remoty: my_remoty.c
	# NOTE: The 'code coverage flags' for QNX's qcc are: 
	#       -Wc,-fprofile-argcs -Wc,-ftest-coverage
	qcc -V 3.3.5,gcc_ntoarmle -g $< \
		../C/hwut_socket_spy.c -o $@ \
		-lsocket \
		-fprofile-arcs -ftest-coverage 
	cp my_remoty /cygdrive/c/nfs_host

clean:
	rm -f my_remoty
