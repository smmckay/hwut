import os
import sys

from   subprocess import Popen

sys.path.insert(0, os.environ["HWUT_PATH"])

from   hwut.auxiliary.executer.remote.socket_interface import ExecuterRemoteSocket, \
                                                              ConfigurationSocket

if "--hwut-info" in sys.argv:
    print "Remote Execution (module test): Socket Interface"
    print "CHOICES: run, query;"
    sys.exit()

os.system("make -f helper.mk -s remotey.exe")

config = ConfigurationSocket("mySocket")
config.port_to_listen  = 37773
config.script_to_start = "./pseudo/remote/location/remotey.exe"

if "run" in sys.argv:
    for app, choice in [("test0", "A"), ("test0", "B"), ("test1", "")]:
        print
        print "--( %s %s )--" % (app, choice)
        print "[start]",
        executer = config.executer_class(config, [app, choice], sys.stdout, sys.stderr)
        executer.wait_for_termination()
        print "[end]"

    for app, choice in [("test0", "C"), ("test2", "A"), ("test1", "A")]:
        print
        print "--( %s %s )--" % (app, choice)
        print "[start]",
        executer = config.executer_class(config, [app, choice], sys.stdout, sys.stderr)
        executer.wait_for_termination()
        print "[end]"

else:
    print
    executer = config.executer_class.for_QueryApplicationList(config)
    executer.wait_for_termination()
    print "--( Query for remote application list )--"
    if executer.result_application_list is None:
        print "   None"
    else:
        for app in executer.result_application_list:
            print "    %s" % app
    print

config.close()
print "<terminated>"
