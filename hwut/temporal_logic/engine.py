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
import os
import re
import tempfile
from   StringIO  import StringIO
from   itertools import chain
from   collections import defaultdict
#_________________________________________________________________________
import hwut.auxiliary.path                           as     aux
import hwut.auxiliary.file_system                    as     fs
import hwut.temporal_logic.parser.rules              as     rule_parser
import hwut.temporal_logic.parser.statements         as     statement_parser
import hwut.temporal_logic.parser.lexical_analysis   as     lex
import hwut.temporal_logic.log                       as     log
from   hwut.temporal_logic.built_in                  import BuiltInFunctionDB
from   hwut.temporal_logic.classes.world             import World, Event
from   hwut.temporal_logic.classes.statement_element import SourceCodeOrigin
from   hwut.temporal_logic.parser.lilli_peg          import get_syntax_error

def do(RuleFilename, fh_input, LogSH, RelevantOutputPrefix="", OnlyREMatchesF=False):
    """For a given set of rules in 'RuleFilename' parse the input from 'fh_input'
    as a sequence of events. Investigate whether rules are respected or violated.
    """
    assert isinstance(RuleFilename, (str, unicode))
    assert isinstance(RelevantOutputPrefix, (str, unicode))
    assert isinstance(OnlyREMatchesF, bool)

    if LogSH is not None: log.set_log_stream_handle(LogSH)

    # (1) Court <- parse the list of rules ______________________________________________
    #
    court = _parse_rules(RuleFilename)
    if isinstance(court, (str, unicode)):
        return court

    # (2) World _________________________________________________________________________
    #
    world = World(court, BuiltInFunctionDB)
    
    # (3) Sequence of Events ____________________________________________________________
    #
    fh_input, tmp_filename = _get_event_stream(fh_input, RelevantOutputPrefix)
    if fh_input is None: return "NO OUTPUT"

    result = _parse_events(world, court, fh_input)

    # (*) Clean up ______________________________________________________________________
    #
    if tmp_filename != "": fs.try_remove(tmp_filename)

    return result

class Court:
    def __init__(self, RuleList = None):
        self.clear()
        
        if RuleList is None: return

        for rule in RuleList:
            rule.prune()
            self.add_rule(rule)

    def clear(self):
        self.absolute_condition_list       = []
        self.temporal_condition_list       = []
        self.event_handler_db              = defaultdict(list)
        self.event_handler_always          = []
        self.transition_handler_db         = defaultdict(list)
        self.regular_expression_match_list = []
        self.function_definition_list      = []
        self.state_machine_definition_list = []
        self.__event_handler_stack         = []

    def add_rule(self, rule):
        # make sure that unecessary branches are deleted.
        rule.prune()

        # sort out the different types of rules into different containers
        if rule.is_function_definition():
            self.function_definition_list.append(rule)

        elif rule.is_state_machine_definition():
            self.state_machine_definition_list.append(rule)

        elif rule.is_event_handler_always():            
            self.event_handler_always.append(rule)

        elif rule.is_event_handler():            
            for event_spec in rule.event_list:
                if type(event_spec) == tuple:
                    # event_spec[0] = from state name; event_spec[1] = to state name
                    self.transition_handler_db[event_spec].append(rule)
                else:
                    self.event_handler_db[event_spec].append(rule)

        elif rule.is_temporal():     
            self.temporal_condition_list.append(rule)
            rule.init()

        elif rule.is_regular_expression_match(): 
            self.regular_expression_match_list.append(rule)

        else:
            self.absolute_condition_list.append(rule)

    def is_event_recursive(self, EventName):
        """It is theoretically possible, that an event would trigger another
        event which somewhere down the lines triggers the event again. Such 
        recursion needs to be avoided.

       RETURNS: True -- If the event is, indeed recursive the event itself is the
                        cause of itself.
                False -- else.
        """
        for handler in self.__event_handler_stack:
            if EventName in handler.event_list: 
                log.event_triggered_inside_event_handler(TheEvent.name, 
                                                         self.__current_event_name_list)
                return True
        return False

    def handle_transition(self, world, FromState, ToState): 
        event_spec = (FromState, ToState)
        transition_handler_list = self.transition_handler_db.get(event_spec)
        
        if transition_handler_list is None: return

        for handler in transition_handler_list:
            self.__event_handler_stack.append(handler)
            if handler.execute(world) == False: 
                log.broken_rule(handler, TheEvent)
            self.__event_handler_stack.pop()

    def handle_event(self, world, TheEvent):
        """Execute any event handler that is related to the given event."""
        verdict_f = True
        event_handler_list = self.event_handler_db[TheEvent.name()]
        if len(event_handler_list) != 0:
            for handler in event_handler_list:
                self.__event_handler_stack.append(handler)
                if handler.execute(world).content == False: 
                    verdict_f = False
                    log.broken_rule(handler, TheEvent)
                self.__event_handler_stack.pop()
        
        if not verdict_f:
            return False    # It cannot become falser than false

        if len(self.event_handler_always) != 0:
            for handler in self.event_handler_always:
                if handler.execute(world) == False: 
                    verdict_f = False
                    log.broken_rule(handler, TheEvent)

        return verdict_f

    def judge_this(self, event, world):
        """Set event = None, if the rules are to be applied without any event. 
           This makes sense, in order to see function assignements being entered 
           into the world database.
        """
        # judge about absolute conditions
        for x in self.absolute_condition_list:
            world.set_current_rule(x)
            if x.execute(world).content == False: log.broken_rule(x, event)

        # judge about temporal conditions
        # -- check what conditions are to wake up and which are to go to sleep
        for x in self.temporal_condition_list:
            world.set_current_rule(x)
            x.decide_sleep_or_awake(world)

        # -- allow the conditions which are awake to make a judgement 
        #    (sleeping conditions say 'OK' to everything)
        for x in self.temporal_condition_list:
            world.set_current_rule(x)
            if x.execute(world).content == False: log.broken_rule(x, event)

    def __repr__(self):
        txt  = "implicit_events         = %i\n" % len(self.event_handler)
        txt += "temporal_condition_list = %i\n" % len(self.temporal_condition_list)
        txt += "absolute_conditions     = %i\n" % len(self.absolute_condition_list)
        return txt

    def freeze_namespace(self, Namespace):
        assert type(Namespace) == list
        pure_namespace = [ name.content for name in Namespace ]
        for rule in   self.temporal_condition_list \
                    + self.regular_expression_match_list \
                    + self.absolute_condition_list:
            rule.freeze_if_in_namespace(pure_namespace)

        for event_handler_list in self.event_handler_db.values():
            for handler in event_handler_list:
                handler.freeze_if_in_namespace(pure_namespace)

    def unfreeze_namespace(self, Namespace, ShallowF):
        assert type(Namespace) == list
        pure_namespace = [ name.content for name in Namespace ]
        if not ShallowF:
            for rule in   self.temporal_condition_list \
                        + self.regular_expression_match_list \
                        + self.absolute_condition_list:
                rule.unfreeze_if_in_namespace(pure_namespace)

            for event_handler_list in self.event_handler_db.values():
                for handler in event_handler_list:
                    handler.unfreeze_if_in_namespace(pure_namespace)
        else:
            for rule in   self.temporal_condition_list \
                        + self.regular_expression_match_list \
                        + self.absolute_condition_list:
                rule.unfreeze_if_directly_in_namespace(pure_namespace)

            for event_handler_list in self.event_handler_db.values():
                for handler in event_handler_list:
                    handler.unfreeze_if_directly_in_namespace(pure_namespace)

def _get_event_stream(fh_input, RelevantOutputPrefix):
    EventListFilename = fh_input.name

    # Announce to the parser the name of the original file. Since they are mostly the
    # same (except for empty lines that replace the irrelevant lines).
    statement_parser.register_input_source(EventListFilename)

    # If no RelevantOutputPrefix, then no filtering is necessary.
    if not RelevantOutputPrefix: return fh_input, ""

    # Replace lines that do not start with '>>>>' with empty lines
    # (this way, the line number remain intact)
    fd, filtered_file_name = tempfile.mkstemp(".hwut.tmp", EventListFilename + "-")
    fh_out                 = os.fdopen(fd, "rwb")

    line = fh_input.readline()
    while line != "":
        if len(line) < 5 or line[:4] != ">>>>": line = "\n"
        else:                                   line = line[4:]
        fh_out.write(line)
        line = fh_input.readline()

    fh_input.close()
    fh_out.seek(0)

    return fh_out, filtered_file_name

def _parse_rules(RuleFilename):
    """Parses all rules and sets them up into a Court object.
    """
    log.rules_parsing_start()

    try:    rule_sh = fs.open_or_die(RuleFilename, "rb")
    except: return "NO RULE FILE"

    statement_parser.register_input_source(RuleFilename)
    raw_rule_list = rule_parser.do(rule_sh).prune()
    if raw_rule_list.error():
        print raw_rule_list.write(1)
        return "SYNTAX ERROR"

    if raw_rule_list.__class__.__name__ == "Fork": rule_list = raw_rule_list.sub_node_list
    else:                                          rule_list = [ raw_rule_list ]

    # Rule sets must be extracted and entered separately
    i    = 0
    size = len(rule_list)
    while i < size:
        rule = rule_list[i]
        if rule.__class__.__name__ == "Primary_Namespace":
            rule = rule.prune()
            rule_list.extend(rule.rule_list)
            size += len(rule.rule_list)
            del rule_list[i]
            size -= 1
        else:
            i += 1

    log.rules_parsing_end(rule_list)
    return Court(rule_list)

def _parse_events(world, court, fh_input):
    """Parses a sequence of events coming from input stream 'fh_input'. The influence
    of the events is stored in 'world' and the world's state is judged by the 'court'.

    RETURNS: 
             "FAIL" -- if rules have been violated.
             "OK"   -- if all existing rules have been respected.
    """
    def skip_or_quit(fh_input):
        """Skips whitespace. 

        RETURNS: 'False' if end of file has been reached. 'True' otherwise.
        """
        tmp = fh_input.read(1)
        while tmp.isspace(): 
            tmp = fh_input.read(1)
        if not tmp: return False # break fh_input.read(1) == "": break
        fh_input.seek(-1, 1)
        return True

    log.statement_parsing_start()
    log.reset_error_flag()
    world.set_stream_handle(fh_input)
    world.receive_event(Event("$INIT"))

    event_n = 0
    skip_or_quit(fh_input)
    for event in statement_parser.event_iterable(fh_input, world):
        event_n += 1
        world.receive_event(event)
        court.judge_this(event, world)
        if not skip_or_quit(fh_input): break

    if log.error_flag(): result = "FAIL" 
    else:                result = "OK"

    log.statement_parsing_end(event_n, result)
    return result


def test_rule_syntax(Filename):
    try: 
        fh = open(Filename, "rb")
    except: 
        print "error: File '%s' not found." % Filename
        sys.exit()

    statement_parser.register_input_source(Filename)
    raw_rule_list = rule_parser.do(fh).prune()
    if raw_rule_list.error():
        print "<<SYNTAX ERROR>>"
        print get_syntax_error().write(0)
    else:
        print "<<ACCEPTED>>"
        ## print raw_rule_list.write(0)

def test_regular_expression_match(RE_String, Filename):
    re_object = re.compile(RE_String)
    try: 
        fh = open(Filename, "rb")
    except: 
        print "error: File '%s' not found." % Filename
        sys.exit()

    print "LineN: Trigger Information:"
    print "-----+-----------------------------------------------------------"
    line_n = 1
    while 1 + 1 == 2:
        start_pos = fh.tell()

        # Check for end of file
        if fh.read(1) == "": break
        fh.seek(-1, 1)

        # Combine lines that end with '\'
        content = "\\"
        while content[-1] == "\\":
            tmp = fh.readline()
            if tmp == "": break
            content += tmp
        content = content[1:] # Before, we set line[0] = "\\" which is not really part of the line.
        if content[-1] == "\n": content = content[:-1]

        # Match against regular expression
        tmp = re_object.match(content)
        if tmp is not None: 
            print "%05i: trigger: {" % line_n
            for line in content.splitlines():
                print "%05i: " % line_n + line
                line_n += 1
            i = 0 
            for group in tmp.groups():
                i += 1
                print "     : $%i = \"%s\";" % (i, group)
            print "%05i: }" % (line_n - 1)
        else:
            fh.seek(start_pos)
            print "%05i: (%s)" % (line_n, fh.readline()[:-1])
            line_n += 1
         
