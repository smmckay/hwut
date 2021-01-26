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

__log_stream_handle = None
__error_flag        = False

def error_flag():
    global __error_flag
    return __error_flag

def raise_error_flag():
    global __error_flag
    __error_flag = True

def reset_error_flag():
    global __error_flag
    __error_flag = False

def set_log_stream_handle(sh):
    global __log_stream_handle
    __log_stream_handle = sh

def rule_activity_change(Rule, New_SleepF, New_FrozenF):
    if __log_stream_handle is None: return

    txt = ""
    if Rule.sleep_f() != New_SleepF:
        if New_SleepF: txt = "rule asleep"
        else:          txt = "rule awake"
        txt += ". "

    if Rule.frozen_f() != New_FrozenF:
        if New_FrozenF:
            txt += "rule frozen"
        else:
            txt += "rule alive (unfrozen)"
        txt += ". "

    if Rule.on_f():
        if New_FrozenF or New_SleepF:          # Next State: 'off'
            txt += "rule 'off'"
    else:
        if not New_FrozenF and not New_SleepF: # Next State: 'on'
            txt += "rule 'on'"

    if txt != "":
        __log_stream_handle.write(__head(Rule) + txt + "\n")

def broken_rule(Rule, Event):
    global __error_flag
    if __log_stream_handle is None: return
    head_rule  = __head(Rule)
    head_event = "%05f:" % Event.time()
    L = max(len(head_rule), len(head_event)) 
    # __log_stream_handle.write(head_rule + "/" * (L - len(head_rule)) + "\n")
    __log_stream_handle.write("%s%s rule broken\n" % (head_rule, (" " * (L - len(head_rule)))))
    __log_stream_handle.write("%s%s by %s.\n"      % (head_event, (" " * (L - len(head_event))), Event.pretty_string()))
    # __log_stream_handle.write(head_stm  + "/" * (L - len(head_stm)) + "\n")

    __error_flag = True

def implicit_event(rule, current_time):
    if __log_stream_handle is None: return
    __log_stream_handle.write(__head(rule) + "implicit events: {\n")

    head_str = "%f:" % current_time

    txt = ""
    raw_txt = rule.event.write(0) # , TypeNameF=False)
    if raw_txt[-1] == "\n": raw_txt = raw_txt[:-1]
    txt += head_str + " " + raw_txt.replace("\n", "\n" + head_str)

    txt += "\n}\n"

    __log_stream_handle.write(txt)

def log_this(TheString):
    __log_stream_handle.write(TheString)

def event(Event, Time):
    __log_stream_handle.write("%05f: " % Time)
    __log_stream_handle.write(Event.pretty_string() + "\n")


def statement(statement, LastReportedTime):
    return
    if __log_stream_handle is None: return
    if statement.is_log_command():  return

    if statement.has_reported_origin():
        head_str = statement.reported_origin.pretty_string(LastReportedTime)
    else:
        head_str = "%f:" % LastReportedTime 

    txt = head_str
    if statement.has_event():
        # raw_txt = statement.event.write(0, TypeNameF=False)
        raw_txt = statement.event.pretty_string() + "\n"
        if raw_txt[-1] == "\n": raw_txt = raw_txt[:-1]
        txt += " " + raw_txt.replace("\n", "\n" + head_str)

    if txt != "": __log_stream_handle.write(txt + "\n")

def error_parsing_statement(statement):
    file_name = statement.source_code_origin.file_name()
    line_n    = statement.source_code_origin.line_n()
    head_str = "%s:%i: " % (file_name, line_n)
    __log_stream_handle.write("# syntax error. statement/event expected. (ignored)\n")
    __log_stream_handle.write(head_str + statement.write(0) + "\n")

def error_time_goes_backwards(CurrentReportedTime, LastReportedTime):
    __log_stream_handle.write("# error: time goes backwards.\n")
    __log_stream_handle.write("#   current reported time = %f.\n" % CurrentReportedTime)
    __log_stream_handle.write("#   last reported time    = %f.\n" % LastReportedTime)

def event_triggered_inside_event_handler(EventName, CurrentEventHandlerList):
    __log_stream_handle.write("# warning: refused to send event '%s' in an event handler for %s." % \
                              EventName, repr(CurrentEventHandlerList)[-1:1])

def statement_parser_confused():
    __log_stream_handle.write("# warning: statement parser confused. stepping over to next line.")

def attribute_value_change(world, AttributeName, Value):
    if __log_stream_handle is None: return
    time_space = " " * len("%f" % world.time())
    __log_stream_handle.write("%s: %s = %s\n" % (time_space, AttributeName, Value))

def rules_parsing_start():
    __log_stream_handle.write("_" * 79 + "\n")
    __log_stream_handle.write("# start parsing rules.\n")

def rules_parsing_end(rule_list):
    if __log_stream_handle is None: return
    __log_stream_handle.write("# %i rule(s) parsed.\n" % len(rule_list))
    __log_stream_handle.write("_" * 79 + "\n")

def statement_parsing_start():
    __log_stream_handle.write("# start checking incoming statements/events.\n")

def statement_parsing_end(StatementN, Result):
    __log_stream_handle.write("# %i statements found. Result = [%s]\n" % (StatementN, Result)) 
    __log_stream_handle.write("_" * 79 + "\n")

def __head(Origin):
    if Origin is None: return "Implicit Event:"
    if hasattr(Origin, "source_code_origin"):
        Origin = Origin.source_code_origin
    return "%s:%i: "  % (Origin.file_name(), Origin.line_n())

