import sys
import os

import hwut.common as common
import hwut.command_line as cl
import hwut.io.messages as io
    
def main():
    try: 
        # If a calling application pipes and breaks the pipe, then an exception
        # is triggerred. This exception needs to be caught--but only on platforms
        # which actually support it.
        from signal import signal, SIGPIPE, SIG_DFL
        signal(SIGPIPE, SIG_DFL)
    except:
        pass

    try:
        bye_str        = "<terminated>"
        cl.prepare()
        command, setup = cl.get_setup(sys.argv)
        common.setup   = setup
        command(setup)
    except KeyboardInterrupt:
        print
        io.print_bye_bye()
        bye_str        = "<aborted>"

    print(" " * (common.terminal_width() - len(bye_str) - 1) + bye_str)
