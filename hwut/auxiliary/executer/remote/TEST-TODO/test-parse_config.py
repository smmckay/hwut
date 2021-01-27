import os
import sys

from   subprocess import Popen

sys.path.insert(0, os.environ["HWUT_PATH"])

import hwut.auxiliary.executer.remote.parse_config as parse_config


if "--hwut-info" in sys.argv:
    print "Parse connection configuration of '--remote' tag;"
    print "CHOICES: socket;"
    sys.exit()


if "socket" in sys.argv:
    print parse_config.do("socket: my-1st; port: 0x4711;")
    print 
    print parse_config.do("socket: my-2nd; ip: 192.168.23.24; port: 0x4711;")
    print 
    print parse_config.do("socket: my-3rd; ip: www.hwut.online;")
    print 
    print parse_config.do("socket: my-4th; ip: localhost; start: bash start-remote.sh;")
