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
from hwut.temporal_logic.classes.statement_element import SyntaxNode
from   hwut.temporal_logic.classes.object          import Object
import hwut.temporal_logic.log as log

import sys

from itertools import izip
from copy      import copy

class Rule(SyntaxNode):
    def __init__(self, InitialAwakeTime=0.0):
        ## print "##callstack:" 
        ## for i in range(5):
        ##    frame = sys._getframe(i).f_code
        ##    print "## <--", frame.co_filename, frame.co_firstlineno

        self.__initial_awake_time = InitialAwakeTime
        self.__awake_time         = InitialAwakeTime
        self.__namespace     = []
        self.__frozen_f           = False
        if InitialAwakeTime == -1.0: 
            self.__sleep_f = False 
            log.rule_activity_change(self, True, self.__frozen_f);  
            self.__sleep_f = True
        else:
            self.__sleep_f = True
            log.rule_activity_change(self, False, self.__frozen_f); 
            self.__sleep_f = False

    def init(self):
        self.__awake_time = self.__initial_awake_time
        if self.__awake_time == 0: self.__sleep_f = False
        else:                      self.__sleep_f = True
        self.__frozen_f = False

    def is_function_definition(self): 
        return False

    def is_event_handler(self):  
        """General response, overiden in 'Rule_ImplicitAnouncement'."""
        return False

    def is_temporal(self):
        """Is condition linked to a temporal condition? General response,
           overidden in 'Rule_TemporalCondition'
        """
        return False

    def is_regular_expression_match(self):
        return False

    def time_alert(self, world):
        """Time since when the rule is awake.
        """
        return world.time() - self.__awake_time

    def on_f(self):
        assert isinstance(self.__sleep_f, bool)
        assert isinstance(self.__frozen_f, bool)
        return not self.__sleep_f and not self.__frozen_f

    def sleep_f(self):
        return self.__sleep_f

    def frozen_f(self):
        return self.__frozen_f

    def set_awake_time(self, Value):
        self.__awake_time = Value

    def set_sleep_f(self, Value):
        assert type(Value) == bool

        log.rule_activity_change(self, New_SleepF=Value, New_FrozenF=self.frozen_f())

        self.__sleep_f = Value

    def set_frozen_f(self, Value):
        assert type(Value) == bool
        log.rule_activity_change(self, New_SleepF=self.sleep_f(), New_FrozenF=Value)
        self.__frozen_f = Value

    def freeze_if_in_namespace(self, Namespace):
        """If the rule is part of a sub-namespace it it frozen."""
        if self.__check_namespace_is_including(Namespace):
            self.set_frozen_f(True)

    def unfreeze_if_in_namespace(self, Namespace):
        """If the rule is part of a sub-namespace it it frozen."""
        if self.__check_namespace_is_including(Namespace):
            self.set_frozen_f(False)

    def unfreeze_if_directly_in_namespace(self, Namespace):
        """If the rule is part of a sub-namespace it it frozen."""
        if self.__check_if_namespace_is_same(Namespace): 
            self.set_frozen_f(False)

    def __check_if_namespace_is_same(self, Namespace):
        if len(Namespace) != len(self.__namespace): 
            return False
        return self.__check_namespace_zipfit(Namespace)

    def __check_namespace_is_including(self, Namespace):
        """Checks wether the given namespace includes the namespace of this rule."""
        if len(Namespace) > len(self.__namespace): 
            return False
        return self.__check_namespace_zipfit(Namespace)

    def __check_namespace_zipfit(self, Namespace):
        """Take the min number of elements from 'Namespace' and 
        'self.__namespace' and compare if they are equal.
        """
        for namespace, my_namespace in izip(Namespace, self.__namespace):
            if namespace != my_namespace: return False
        return True

    def set_namespace(self, Namespace):
        assert type(Namespace) == list
        self.__namespace = copy(Namespace)

class Rule_TemporalCondition(Rule):
    def __init__(self, ArgList): # SourceOrigin, time_span, condition, NamespaceList):
        assert len(ArgList) == 3
        SourceOrigin  = ArgList[0]
        SyntaxNode.__init__(self, SourceOrigin)
        ## NOT: Rule.__init__(self)
        self.time_span = ArgList[1]
        self.condition = ArgList[2]

        if self.time_span.is_sleeping_at_begin(): Rule.__init__(self, InitialAwakeTime=-1.0)
        else:                                     Rule.__init__(self, InitialAwakeTime=0.0)

    def decide_sleep_or_awake(self, world):
        """This functions judges wether this temporal condition is active or inactive according 
           to the current state of the system.

           (1) if it is sleeping then check wether the the current state 
               can awake it.

           (2) if it is awake then check wether the curren state can send
               it to sleep.
        """
        if not self.on_f():
            if self.time_span.check_awake_condition(world): 
                self.set_sleep_f(False)
                self.set_awake_time(world.time())
        else:
            if self.time_span.check_sleep_condition(world): 
                self.set_sleep_f(True)

    def write(self, Depth):
        indent = "  " * Depth
        txt  = indent + "Rule:\n"
        txt += self.time_span.write(Depth + 1)
        txt += indent + "  REQUIRES\n"
        txt += self.condition.write(Depth + 1) 
        return txt

    def is_temporal(self):
        """Is condition linked to a temporal condition? General response,
           overidden in 'Rule_TemporalCondition'
        """
        return True

    def prune(self):
        """NOTE: We cannot prune rules, since there are (inherited) member functions that
                 are necessary for administrative purposes.
        """
        self.time_span = self.time_span.prune()
        self.condition = self.condition.prune()
        return self

    def execute(self, world):
        """A sleeping temporal rule does not judge the current state. It is fine with
           everything that happens. A temporal rule that is awake checks for the con-
           dition to be fulfilled.
        """
        if not self.on_f(): return Object.bool(True)

        return self.condition.execute(world)
        
class Rule_AbsoluteCondition(Rule):
    def __init__(self, ArgList): 
        assert len(ArgList) == 2
        SourceOrigin  = ArgList[0]
        SyntaxNode.__init__(self, SourceOrigin)
        Rule.__init__(self, InitialAwakeTime=0.0)
        self.condition = ArgList[1]

    def write(self, Depth):
        indent = "  " * Depth
        txt =  indent + "Rule:\n"
        txt += self.condition.write(Depth + 1)
        return txt

    def prune(self):
        """NOTE: We cannot prune rules, since there are (inherited) member functions that
                 are necessary for administrative purposes.
        """
        self.condition.prune()
        return self

    def execute(self, world):
        result = self.condition.execute(world)
        return result

class Rule_EventHandler(Rule):
    def __init__(self, ArgList): # SourceOrigin, condition, event, NamespaceList):
        assert len(ArgList) == 3
        SourceOrigin     = ArgList[0]
        SyntaxNode.__init__(self, SourceOrigin)
        Rule.__init__(self)
        def adapt(x):
            if x.__class__.__name__ == "Fork": return (x[0].content, x[1].content) # State Transition
            else:                            return x.content
    
        # state transition -> tuple(FromState, ToState)
        # single event     -> tuple(FromState, ToState)
        self.event_list  = [ adapt(x) for x in ArgList[1] ]
        self.consequence = ArgList[2] 

    def is_event_handler(self):
        return True

    def prune(self):
        self.consequence = self.consequence.prune()
        return self

    def execute(self, world):
        """The caller of this function knows that one of the events in the 
           self.event_list has entered. Thus we only execute the consequences.
        """
        # If the rule is not 'on' than it permits everything and everything is fine.
        if not self.on_f(): return Object.bool(True)
        # An event that is interesting for us has triggered
        # --> trigger the consequences
        return self.consequence.execute(world)
        
    def write(self, Depth):
        indent = "  " * Depth
        txt =  indent + "Rule: On %s\n" % repr(self.event_list)[1:-1]
        txt += indent + "  =>\n"
        txt += self.consequence.write(Depth + 1) 
        return txt

class Rule_EventCondition(Rule):
    def __init__(self, ArgList): # SourceOrigin, condition, event, NamespaceList):
        assert len(ArgList) == 3
        SourceOrigin     = ArgList[0]
        SyntaxNode.__init__(self, SourceOrigin)
        Rule.__init__(self)
        self.condition                = ArgList[1]
        self.condition_last_verdict_f = False
        self.consequence              = ArgList[2] 

    def is_event_handler_always(self):
        return True

    def is_event_handler(self):
        return True

    def prune(self):
        self.consequence = self.consequence.prune()
        return self

    def execute(self, world):
        """The caller of this function knows that one of the events in the 
        self.event_list has entered. Thus we only execute the consequences.

         Condition:   true           .--------.          .--------.
                                     |        |          |        |
                      false  --------'        '----------'        '--------
                                     <T>                 <T>

        The '.consequences' are only considered at <T>. that is when the
        condition transits from 'false' to 'true'.
        """
        # If the rule is not 'on' than it permits everything and everything is fine.
        if self.condition.execute(world).content == False: 
            self.condition_last_verdict_f = False
            return Object.bool(True)
        elif self.condition_last_verdict_f == True:              
            return Object.bool(True)
        else:
            # Transition from 'false' to 'true' detected: => execute consequence
            self.condition_last_verdict_f = True
            return self.consequence.execute(world)
        
    def write(self, Depth):
        indent = "  " * Depth
        txt =  indent + "Rule: On %s\n" % self.condition.write(Depth)
        txt += indent + "  =>\n"
        txt += self.consequence.write(Depth + 1) 
        return txt

class Rule_List(SyntaxNode):
    def __init__(self, ArgList):
        assert len(ArgList) >= 2
        SyntaxNode.__init__(self, ArgList[0])  # [0] = SourceCodeOrigin
        self.basic_rule_list = ArgList[1]

    def prune(self):
        for rule in self.basic_rule_list:
            rule.prune()

        # If there is only one element in the list, then this structure can 
        # be replaced by the one and only element.
        if len(self.basic_rule_list) == 1: return self.basic_rule_list[0]
        else:                              return self

    def execute(self, world):
        """All errors need to be reported. Do not stop at the first rule
        that fails.
        """
        verdict_f = True
        for rule in self.basic_rule_list: 
            if rule.execute(world).content == False: verdict_f = False
        return Object.bool(verdict_f)
    
    def write(self, Depth):
        indent = "  " * Depth
        txt =  indent + "Rule_List:\n"
        txt += indent + "  BRACKET\n"
        for rule in self.basic_rule_list:
            txt += rule.write(Depth +1)
        return txt

