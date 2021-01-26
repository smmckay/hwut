all: hwut_agent hwut_spy

hwut_spy: hwut_socket_spy.c hwut_spy_main.c
	# gcc -b ARM -marm -mlittle-endian -g $< -o $@ -L/cygdrive/C/QNX632/target/qnx6/armbe/lib/ -lsocket
	qcc -V 3.3.5,gcc_ntoarmle -g $^ -o $@ -lsocket

hwut_agent: hwut_socket_agent.c
	# gcc -b ARM -marm -mlittle-endian -g $< -o $@ -L/cygdrive/C/QNX632/target/qnx6/armbe/lib/ -lsocket
	qcc -V 3.3.5,gcc_ntoarmle -g $< -o $@ -lsocket

clean: 
	rm -f hwut_agent hwut_spy
