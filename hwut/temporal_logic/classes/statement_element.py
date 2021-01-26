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
class SourceCodeOrigin:
    """Objects of this class store information about the origin of a rule or
       a statement in the file where they appear. Note, that this is fundamentally
       different from ReportedOrigins that contain information about the test
       programs statements of where its outputs come from.
    """
    def __init__(self, Arg1, LineN=None):
        Arg1Type = Arg1.__class__.__name__
        assert LineN is not None or Arg1Type == "SourceCodeOrigin"
        
        if Arg1Type != "SourceCodeOrigin":
            self.__file_name = Arg1
            self.__line_n    = LineN
        else:
            self.__file_name = Arg1.__file_name
            self.__line_n    = Arg1.__line_n

    def set_origin(self, Filename, LineN):
        self.__file_name = Filename
        self.__line_n    = LineN

    def set_file_name(self, Name):
        self.__file_name = Name

    def set_line_n(self, Name):
        self.__line_n = Name

    def file_name(self):
        try:    return self.__file_name
        except: return ""

    def line_n(self):
        try:    return self.__line_n
        except: return 0

    def __repr__(self):
        return self.__file_name + ":%i:" % self.__line_n
   
class SyntaxNode:
    def __init__(self, SourceCodeOrigin=None):
        self.source_code_origin = SourceCodeOrigin

    def write(self, Depth):
        return "<call of base class 'write'>"

    def error(self): 
        return False

    def ok(self):
        return True

    def is_function_definition(self):
        return False

    def is_state_machine_definition(self): 
        return False

    def is_event_handler_always(self):
        return False

    def is_event_handler(self):
        return False

    def is_temporal(self):
        return False

    def is_regular_expression_match(self):
        return False

    def is_actively_accessing_state(self):
        return True

    def prune(self):
        """In some cases, an expression branch node contains only one element. 
           In this case the node can be replaced by its successor. Note, that
           this means practically only that a node that only passes through
           the result of another one is replaced by it. Thus storage and 
           computation time can be spared.

           A node that cannot be pruned returns itself.
        """
        return self

class SyntaxError(SyntaxNode):
    def __init__(self, Missing):
        assert type(Missing) in [str, list]
        if type(Missing) == list: self.missing = Missing
        else:                     self.missing = [ Missing ]
        self.for_what_list = []
        SyntaxNode.__init__(self, SourceCodeOrigin("", -1))

    def write(self, Depth):
        position_str = "%s:%i:" % (self.source_code_origin.file_name(), self.source_code_origin.line_n()) 
        if len(self.missing) > 1: txt = position_str + " Missing one of "
        else:                     txt = position_str + " Missing "
        for element in self.missing: 
            txt += element + ", " 
        txt += "\n"
        ## for what in self.for_what_list:
        ##    txt += position_str + " for " + what + "\n"
        return txt

    def extend_missing(self, MissingList):
        for element in MissingList:
            if element not in self.missing: self.missing.append(element)

    def add_for_what(self, What):
        self.for_what_list.append(What)

    def error(self): 
        return True

    def ok(self):
        return False

    def set_error_token_index(self, Index):
        self.__error_token_index = Index

    def error_token_index(self):
        return self.__error_token_index

    def stream_position(self):
        return self.__stream_position

    def set_stream_position(self, sh):
        self.__stream_position = sh.tell()
        self.__related_stream  = sh
        sh.seek(0)
        self.source_code_origin.set_line_n(sh.read(self.__stream_position).count("\n"))
        try:    self.source_code_origin.set_file_name(sh.name)
        except: self.source_code_origin.set_file_name("<no file name>")

    def __repr__(self):
        return repr(self.missing)[-1:1]

class NodeNull(SyntaxNode):
    def __init__(self):
        pass

    def write(self, Depth):
        return " " * Depth + "NodeNull"

    def error(self): 
        return False

    def ok(self):
        return True

    def __repr__(self):
        return "NodeNull"

class Fork(SyntaxNode):
    def __init__(self, ArgList, Name="Fork", ReductionF=True):
        for arg in ArgList:
            assert arg is not None
        self.sub_node_list           = ArgList
        self.name                    = Name
        self.__reduction_permitted_f = ReductionF

    def __getitem__(self, Index):
        return self.sub_node_list[Index]

    def __iter__(self):
        return self.sub_node_list.__iter__()

    def __len__(self):
        return len(self.sub_node_list)

    def error(self):
        for node in self.sub_node_list:
            if node.error(): return True
        return False

    def ok(self):
        return not self.error()

    def disallow_reduction_to_single(self):
        self.__reduction_permitted_f = False

    def set_argument_list(self, ArgList):
        assert len(ArgList) == len(self.subnode_list)
        self.node = ArgList

    def write(self, Depth):
        txt = "  " * Depth + self.name + ":\n"
        i = 0
        for element in self.sub_node_list:
            i += 1
            txt += "  " * (Depth+1) + "(%i)\n" % i
            if element is None: txt += "  " * (Depth + 1) + "None\n"
            else:               txt += element.write(Depth + 1)
        return txt

    def prune(self):
        self.sub_node_list = [
            sub_node.prune()
            for sub_node in self.sub_node_list
        ]

        # In case that the node has only one branch it can be replaced with 
        # the end of the branch. However, there are circumstance where one 
        # requires the result type 'list' and the node needs to remain. The
        # reduction only happens if the correspondent flag is set.
        if self.__reduction_permitted_f and len(self.sub_node_list) == 1: 
            return self.sub_node_list[0]
        else: 
            return self

    def __repr__(self):
        return self.name

    def execute(self, world):
        # See 'prune() for a detailed comment. The reduction has to trigger, even if no
        # pruning was done.
        if self.__reduction_permitted_f and len(self.sub_node_list) == 1: 
            return self.sub_node_list[0].execute(world)
        else:
            return [
                node.execute(world) for node in self.sub_node_list
            ]

def reject(sh, OldPosition, Missed):
    # global __current_line_n
    # new_pos = sh.tell()
    # sh.seek(OldPosition)
    # backward_str = sh.read(new_pos - OldPosition + 1)
    # __current_line_n -= backward_str.count("\n")
    sh.seek(OldPosition)

    assert type(Missed) in [str, list]

    error_object = SyntaxError(Missed)
    error_object.set_stream_position(sh)
    return error_object

