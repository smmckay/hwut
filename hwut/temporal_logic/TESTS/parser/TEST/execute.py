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
# For further information see http://www.genivi.org/. 
#------------------------------------------------------------------------------
#! /usr/bin/env python
import sys
import os
from StringIO import StringIO

sys.path.append(os.environ["HWUT_PATH"])

import hwut.temporal_logic.parser.rules      as rule_parser
import hwut.temporal_logic.parser.statements as statement_parser
import hwut.temporal_logic.parser.lilli_peg  as lilli_peg
import hwut.temporal_logic.log               as log
from   hwut.temporal_logic.built_in          import BuiltInFunctionDB
from   hwut.temporal_logic.engine            import World, Court

if "--hwut-info" in sys.argv:
    print "Execution: Rules and Events"
    sys.exit()

world = World(Court(), BuiltInFunctionDB)
world.register_time(0) # world.time() + World.JIFFY)

log.set_log_stream_handle(sys.stdout)

def do(source_code):
    lilli_peg.node_cache.clear()
    global world
    world.register_time(world.time() + 1)
    sh = StringIO(source_code)
    print "%f:   %s" % (world.time(), source_code)
    event_trigger = statement_parser.snap_event_trigger(sh)
    event_trigger = event_trigger.prune()
    world.time_update(-1)
    event         = event_trigger.execute(world)
    world.receive_event(event)

def test(condition_code):
    lilli_peg.node_cache.clear()
    sh = StringIO(condition_code)
    print "-- %s" % condition_code
    rule = rule_parser.snap_rule(sh)
    rule = rule.prune()
    world.set_current_rule(rule)
    if rule.__class__.__name__ != "SyntaxError": print "   result:", rule.execute(world)
    else:                                        print "   result:", rule
    print


do("RESET(0.815);")
do("SHUTDOWN;")
do("SHUTDOWN(error_n=1);")
do("START(a=1, b=2, c=3);")

def filter_out_built_in_functions():
    global world
    txt = str(world)
    result_txt = ""
    for line in txt.splitlines():
        if line.find("FunctionObject") != -1: continue
        result_txt += line + "\n"
    return result_txt


print "________________________________________________________________________"
print filter_out_built_in_functions()
print "________________________________________________________________________"
print 

test("SHUTDOWN.time() > 0.999;")
test("SHUTDOWN.time() < 1;")
test("if RESET : RESET[0] == 0.815; ")
test("if RESET : if START : RESET[0] == 0.815; ")

print "________________________________________________________________________"
do("START;")
do("RESET(version=0.816);")
print "________________________________________________________________________"
print filter_out_built_in_functions()
print "________________________________________________________________________"
print 
test("if RESET : if START.count() != 0 : RESET.version == 0.815; ")
test("if RESET : if START.count() != 0 : RESET.version == 0.816; ")

