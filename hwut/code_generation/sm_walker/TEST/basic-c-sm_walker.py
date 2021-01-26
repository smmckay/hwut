# SPDX license identifier: LGPL-2.1
#
# Copyright (C) Frank-Rene Schaefer, private.
# Copyright (C) Frank-Rene Schaefer, 
#               Visteon Innovation&Technology GmbH, 
#               Kerpen, Germany.
#
# This file is part of "HWUT -- The hello worldler's unit test".
#
#                  http://hwut.sourceforge.net
#
# This file is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this file; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA
#
#------------------------------------------------------------------------------
#! /usr/bin/env python
import os
import sys

sys.path.insert(0, os.environ["HWUT_PATH"])

import hwut.code_generation.sm_walker.language.c.header_sm_walker as header_sm_walker
import hwut.code_generation.sm_walker.language.c.source_sm_walker as source_sm_walker
from   hwut.code_generation.sm_walker.language.c.source_sm_walker import State, StateTransition, StateMachineWalker

import hwut.common as common
from   collections import defaultdict

if "--hwut-info" in sys.argv:
    print "State Machine Walker: C source code basic tests;"
    sys.exit()

def check_open_dollars(result):
    print "    Open $-s: %i (must be ZERO!)" % result.count("$")
    if result.count("$") == 0:
        return
    for line_n, line in enumerate(result.splitlines(), start=1):
        if line.find("$") != -1:
            print "    [%3i] %s" % (line_n, line)
    sys.exit()

state_list_0 = [
    State("HAPPY", [
        StateTransition("HIT",     None,             "ANGRY"),
        StateTransition("STROKE", "WATCHING_TV",     "ANGRY"),
    ]),
    State("ANGRY", [
        StateTransition("STROKE", "NOT_WATCHING_TV", "HAPPY"),
    ])
]

state_list_1 = [
    State("FIT", [
        StateTransition("WORK", None,          "TIRED"),
        StateTransition("EAT",  "FRITZ_HAPPY", "TIRED"),
    ]),
    State("TIRED", [
        StateTransition("SLEEP", None,         "FIT"),
    ])
]

sm_walker_0 = StateMachineWalker("Fritz", state_list_0, "double", 7, 9)
sm_walker_0.event_code_db = {}
sm_walker_0.condition_code_db = {}
sm_walker_1 = StateMachineWalker("Otto", state_list_1, "float", 77, 99)
sm_walker_1.event_code_db = {}
sm_walker_1.condition_code_db = {}

# def do(Name, InitStateIndex, UserDataType, PathMaxLength, MaxLoopN):
source_txt, event_id_db, condition_id_db = source_sm_walker.do([sm_walker_0, sm_walker_1])
header_txt = header_sm_walker.do([sm_walker_0, sm_walker_1], event_id_db, condition_id_db)

main_txt = "\nint main(int argc, char** argv) { return 0; }"

open("tmp.c", "wb").write(header_txt + source_txt + main_txt)

print
print "--( Words with 'Fritz' )--------------------------------------"
print
done_set = set()
for line in (header_txt + source_txt).split():
    if line.find("Fritz") == -1: continue
    elif line in done_set: continue
    done_set.add(line)

for word in sorted(list(done_set)):
    print word

print
print "--( Words with 'Otto' )---------------------------------------"
print
done_set = set()
for line in (header_txt + source_txt).split():
    if line.find("Otto") == -1: continue
    elif line in done_set: continue
    done_set.add(line)

for word in sorted(list(done_set)):
    print word

print
print "--( Compiling / no messages are good messages )---------------"
print
os.system("rm -f a.out")
if not common.is_windows():
	os.system("gcc -I$HWUT_PATH/support/C tmp.c $HWUT_PATH/support/C/hwut_sm_walker.c -Wall -o a.out")
else:
	os.system("gcc -I%HWUT_PATH%\support\C tmp.c %HWUT_PATH%\support\C\hwut_sm_walker.c -Wall -o a.out")

os.system("ls a.out")
os.system("rm a.out")

