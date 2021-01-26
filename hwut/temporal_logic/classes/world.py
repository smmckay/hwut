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
from   hwut.temporal_logic.classes.object            import Object, FunctionObject
from   hwut.temporal_logic.classes.primary           import Primary_FunctionDefinition
from   hwut.temporal_logic.classes.statement_element import SourceCodeOrigin, SyntaxNode
import hwut.temporal_logic.log                       as     log

class EventOrigin(SyntaxNode):
    def __init__(self, ArgList=None):
        self.file_name = ""
        self.line_n    = -1
        self.time      = -1
        if ArgList is None:
            return

        L = len(ArgList)
        if   L == 1:
            self.time      = ArgList[0].content
        elif L == 2:
            self.file_name = ArgList[0].content
            self.line_n    = ArgList[1].content
        elif L == 3:
            self.file_name = ArgList[0].content
            self.line_n    = ArgList[1].content
            self.time      = ArgList[2].content
        else:
            assert False

    def pretty_string(self, DefaultTime):
        if self.line_n == -1 and not self.file_name:
            return "%f:" % self.time
        else:
            return "%s:%s: %f:" % (self.file_name, self.line_n, self.time)

    def write(self, Depth):
        indent = "  " * Depth
        if self.line_n == -1 and not self.file_name:
            return indent + "EventOrigin: time = %f\n" % self.time
        else:
            return indent + "EventOrigin: %s:%i: time = %f\n" % (self.file_name, self.line_n, self.time)

    def __str__(self):
        return self.pretty_string(-1)

class Event(SyntaxNode):
    def __init__(self, Name, AdornmentList=None, Time=None):
        self.__name    = Name
        if Time is not None: 
            self.__origin = EventOrigin()
            self.__origin.time = World.BEGIN_OF_TIME
        else:                
            self.__origin = None
        if AdornmentList is None: self.__adornment_value_list = []
        else:                     self.__adornment_value_list = AdornmentList
        assert type(self.__adornment_value_list) == list

    def set_origin(self, TheEventOrigin):
        assert isinstance(TheEventOrigin, EventOrigin)
        self.__origin = TheEventOrigin

    def name(self):
        return self.__name

    def time(self):
        if self.__origin is None: return -1
        else:                     return self.__origin.time

    def set_time(self, Value):
        self.object_db["$time"] = Value

    def is_log_command(self):
        return False

    def adornment_list(self):
        return self.__adornment_value_list

    def get_adornment_by_index(self, Index):
        if Index < 0 or Index >= len(self.__adornment_value_list): 
            return -1
        return self.__adornment_value_list[Index]

    def get_adornment_by_name(self, Name):
        for adornment in self.__adornment_value_list:
            if adornment.name == Name: 
                return adornment
        return -1

    def pretty_string(self):
        if self.__adornment_value_list == []: opening_bracket_str = ""; closing_bracket_str = ""
        else:                                 opening_bracket_str = "("; closing_bracket_str = ")"
        txt = "%s%s" % (self.__name, opening_bracket_str)
        for result in self.__adornment_value_list:
            txt += "%s=%s, " % (result.name, str(result.content))
        if len(self.__adornment_value_list) != 0: txt = txt[:-2]
        txt += closing_bracket_str
        return txt

    def prune(self):
        return self

    def __str__(self):
        txt = "%s %s" % (self.__origin, self.name())
        index = -1
        for adornment in self.__adornment_value_list:
            index += 1
            txt += " [%i] %s = " % (index, adornment.name) 
            txt += str(adornment)

        if txt[-1] == "\n": txt = txt[:-1]
        return txt 

class EventDbEntry:
    
    def __init__(self, Name):
        self.__name           = Name
        self.__count_n        = 0
        self.__last_time      = World.BEGIN_OF_TIME
        self.__related_event  = Event(Name)

    @staticmethod
    def from_event(RelatedEvent, Time):
        result = EventDbEntry(RelatedEvent.name())
        result.__count_n        = 1 # Event has occurred
        result.__last_time      = Time
        result.__related_event  = RelatedEvent
        return result

    @property
    def name(self):                        return self.__name
    @property
    def last_time(self):                   return self.__last_time
    def last_time_set(self, Time):         self.__last_time = Time
    @property
    def related_event(self):               return self.__related_event
    def related_event_set(self, TheEvent): self.__related_event = TheEvent
    @property
    def count_n(self):                     return self.__count_n
    def count_n_incremenent(self):         self.__count_n += 1

    def __repr__(self):
        return "%f: [#%i] %s(%s)" % (
            self.__last_time, self.__count_n, self.__name, 
            "".join("%s, " % x for x in self.__related_event.adornment_list())
        )

class StateMachine(object):
    __slots__ = ("state_set", "state", "previous", "origin", "__time_last_transition")

    def __init__(self, StateNameList, Origin):
        self.state_set = set(StateNameList)
        self.state     = None
        self.previous  = None
        self.origin    = Origin
        self.__time_last_transition = -1

    def transit_to(self, EventName, Time):
        assert EventName  in self.state_set
        self.previous               = self.state
        self.state                  = EventName
        self.__time_last_transition = Time

    def time_since_last_transition(self, world):
        """Time since when the state has been entered."""
        return world.time() - self.__time_last_transition

class World:
    JIFFY         = 1e-6
    BEGIN_OF_TIME = -1e37

    def __init__(self, court, BuiltInFunctionDB):
        # map: Event name --> StateMachine object
        self.state_machine_db = {}

        self.init()
        self.__court = court
        for function_def in court.function_definition_list:
            self.__register_function(function_def)
        for state_machine_def in court.state_machine_definition_list:
            self.__register_state_machine(state_machine_def)

        self.object_db.update(
            (name, Object.function(function, name)) 
            for name, function in BuiltInFunctionDB.iteritems()
        )

    def init(self):
        self.object_db          = {}
        self.event_db              = {}
        self.object_db["$time"] = - World.JIFFY # on $INIT: time += JIFFY
        #
        self.source_code_filename = ""
        self.source_code_line_n   = 0
        self.__current_rule       = None
        self.__stream_handle      = None
        self.state_machine_db.clear()

    def receive_event(self, TheEvent):
        assert isinstance(TheEvent, Event)

        if self.__court.is_event_recursive(TheEvent.name()): 
            pass
        else:
            self.event_db_update(TheEvent)
            self.state_machine_db_update(TheEvent)

        return Object.bool(self.__court.handle_event(self, TheEvent))

    def time_update(self, ReportedTime):
        if ReportedTime != -1.0: self.register_time(ReportedTime)
        else:                    self.increment_time_jiffy()
        return self.time()

    def event_db_update(self, TheEvent):
        """Record some basic information about the event which just occurred.
        """
        entry = self.event_db.get(TheEvent.name())
        if entry is None:
            entry = EventDbEntry.from_event(TheEvent, self.time())
            self.event_db[TheEvent.name()] = entry
        else:
            entry.last_time_set(self.time())
            entry.related_event_set(TheEvent)
            entry.count_n_incremenent()
        log.event(TheEvent, self.time())

    def event_db_get(self, EventName):
        entry = self.event_db.get(EventName)
        if entry is None:
            entry = EventDbEntry(EventName)
            self.event_db[EventName] = entry
        return entry
        
    def state_machine_db_update(self, TheEvent):
        """If there is a state machine concerned with the event, then 
           let the state machine do its transition.
        """
        sm = self.state_machine_db.get(TheEvent.name())
        if sm is None: return
        sm.transit_to(TheEvent.name(), self.time())
        self.__court.handle_transition(self, sm.previous, sm.state)

    def freeze_namespace(self, Namespace):
        self.__court.freeze_namespace(Namespace)
        return Object.bool(True)

    def unfreeze_namespace(self, Namespace, ShallowF=False):
        self.__court.unfreeze_namespace(Namespace, ShallowF)
        return Object.bool(True)

    def current_rule(self):
        return self.__current_rule

    def set_current_rule(self, Rule):
        self.__current_rule = Rule

    def set_stream_handle(self, SH):
        self.__stream_handle = SH

    def stream_handle(self):
        return self.__stream_handle

    def time(self):
        return self.object_db["$time"]

    def register_time(self, Time):
        if Time < self.object_db["$time"]: 
            log.error_time_goes_backwards(Time, self.object_db["$time"])
        self.object_db["$time"] = Time

    def increment_time_jiffy(self):
        """Increment time by one micro (second).
        """
        self.object_db["$time"] += World.JIFFY

    def variable_access(self, Name):
        if Name == "$time_alert":
            current_rule = self.current_rule()
            if hasattr(current_rule, "time_alert") == False:
                log.log_this("Variable $time_alert not available in current context!\n")
                return -1
            else:
                return Object.number(current_rule.time_alert(self), "(time since alert)")

        elif Name == "$time": 
            return Object.number(self.time(), "(global time)")

        elif Name not in self.object_db:
            result               = Object.void(Name=Name)
            self.object_db[Name] = result
            return result

        else:
            return self.object_db[Name]

    def __register_function(self, Def):
        assert Def.__class__ == Primary_FunctionDefinition
        self.object_db[Def.function_name] = \
                      Object(Object.FUNCTION, 
                             FunctionObject(Def.function_body.execute,
                                            [], 
                                            WorldRequiredF=True))

    def __register_state_machine(self, StateMachineDef):
        event_name_list = tuple(x.content for x in StateMachineDef.event_name_list)
        for name in event_name_list:
            if name in self.state_machine_db:
                log.name_defined_in_more_than_one_state_machine(Origin, self.state_machine_db[name].origin, name)
                return

        sm = StateMachine(event_name_list, StateMachineDef.source_code_origin)
        for name in event_name_list:
            self.state_machine_db[name] = sm

    def __str__(self):
        txt = "-- attributes:\n"
        item_list = self.object_db.items()
        item_list.sort(lambda a, b: cmp(a[0], b[0]))
        for name, value in item_list:
            txt += "    %s: %s\n" % (name, value)

        txt += "\n"
        txt += "-- events:\n"
        for name, event in sorted(self.event_db.iteritems()):
            # txt += "   " + name + " "
            txt += repr(event).replace("\n", "\n  ") + "\n"

        txt += "\n"
        txt += "-- time: %s, file=%s, line-n=%s" % \
               (repr(self.object_db["$time"]), self.source_code_filename, self.source_code_line_n)

        txt = " " * 9 + txt.replace("\n", "\n" + " " * 9)
        return txt

