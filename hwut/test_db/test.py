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
import hwut.auxiliary.path                          as     aux
import hwut.auxiliary.file_system                   as     fs
import hwut.auxiliary.make                          as     make
import hwut.auxiliary.executer.core                 as     executer
from   hwut.auxiliary.executer.executer_system_call import ExecuterSystemCall
#from   hwut.auxiliary.executer.remote               import ExecuterRemote
import hwut.io.messages                             as     io
import hwut.common                                  as     common

import time
import binascii
from   copy import copy
import sys

class Test:
    def __init__(self, TestDescription, ChoiceIdx):
        # assert TestApplication.__class__ == TestDescription
        assert type(ChoiceIdx) == int

        self.description    = TestDescription
        self.__choice_index = ChoiceIdx
        self.__first_f      = False # first choice of application
        self.__last_f       = False # last choice of application

        ## self.thread = None
        self.__execution_id   = None
        self.__OUT_file_name  = aux.get_protocol_file_name(TestDescription, 
                                                           self.choice(), 
                                                           OutputF=True)
        self.__GOOD_file_name = aux.get_protocol_file_name(TestDescription, 
                                                           self.choice())
        self.__execution_id   = None

    def execution_sequence_index(self):
        assert self.__execution_id is not None
        return self.__execution_id

    def set_execution_sequence_index(self, Value):
        assert Value is None or type(Value) == int
        self.__execution_id = Value

    def set_first_f(self):
        self.__first_f = True
    
    def set_last_f(self):
        self.__last_f = True

    def first_f(self):
        return self.__first_f

    def last_f(self):
        return self.__last_f

    def choice_index(self):
        return self.__choice_index

    def choice(self):
        return self.description.result_list()[self.__choice_index].choice

    def extra_output_file_list(self):
        db = self.description.extra_output_file_list_db()
        if not db: return []

        for_all    = db.get(",,all,,")
        for_choice = db.get(self.choice())

        result = set()
        if for_all    is not None: result.update(for_all)
        if for_choice is not None: result.update(for_choice)
        return list(result)

    def result(self):
        return self.description.result_list()[self.__choice_index]

    def OUT_FileName(self):
        return "OUT/%s" % self.__OUT_file_name

    def OUT_tmp_FileName(self):
        return "OUT/%s.tmp" % self.__OUT_file_name

    def GOOD_FileName(self):
        return "GOOD/%s" % self.__GOOD_file_name

    def GOOD_ExtraFileName(self, FileName):
        file_stem = aux.get_protocol_file_name(self.description, 
                                               self.choice(), OutputF=False,
                                               Extension="") 
        return "GOOD/%s--file--%s" % (file_stem, aux.safe_string(FileName))

    def GOOD_tmp_FileName(self):
        return "GOOD/%s.tmp" % self.__GOOD_file_name

    def OUT_FileHandle(self, Mode="rb"):
        try:    return fs.open_or_die(self.OUT_FileName(), Mode)
        except: print "Error: output could not be opened."; sys.exit()

    def OUT_tmp_FileHandle(self, Mode="rb"):
        return fs.open_or_die(self.OUT_tmp_FileName(), Mode)

    def GOOD_FileHandle(self, Mode="rb", ThrowF=False, ForgiveF=False):
        try:    
            return fs.open_or_die(self.GOOD_FileName(), Mode, NoteF=False)
        except: 
            if   ForgiveF: return
            elif ThrowF:   raise Exception()
            io.on_file_access_error(self.GOOD_FileName())

    def GOOD_tmp_FileHandle(self, Mode="rb"):
        return fs.open_or_die(self.GOOD_tmp_FileName(), Mode, 
                              NoteF=False)

    def adapt_GOOD_file_crc(self, content=None):
        if content is None:
            content = fs.read_or_die(self.GOOD_FileName())
        self.result().crc_32 = binascii.crc32(content)

    def execute(self):
        """RETURNS: [0] -- Filehandle to access standard output of test.
                    [1] -- ErrorType as defined in 'hwut.auxiliary.executer.core'.
        """
        if     self.description.make_dependent_f() \
           and self.description.is_present() == False:
            return None, 0

        cmd_line = copy(self.description.interpreter_list())
        cmd_line.extend([
            aux.ensure_dot_slash(self.description.file_name()),
            self.choice(),
            "FIRST" if self.first_f() else "NOT-FIRST",
            "LAST"  if self.last_f()  else "NOT-LAST"
        ])

        stdout_fh = self.OUT_FileHandle(Mode="wb") 
        # execution_unit = None
        # execution_unit = { 
        #    "TCP":    remote_executer.tcp,
        #    "UART":   remote_executer.uart,
        #    "SYSTEM": None           # default: The system where hwut runs.
        # }[self.executer]

        # Time Out: A test shall not run too long, especially not forever.
        #           If there is a time given from previous experiments, then
        #           this time shall not be exceeded by factor 3. However, no
        #           timeout shall occur before 1 second.
        timeout_sec = None
        if     common.time_out_detection_f() \
           and self.description.time_out_detection_f() \
           and self.result().time_to_execute_sec is not None:
            timeout_sec = max(1.0, self.result().time_to_execute_sec * 3)

        # if self.description.remote_config_id() is not None: executer_class = ExecuterRemote
        executer_class = ExecuterSystemCall

        time_start = time.time() # [sec]

        error_type = executer.do(cmd_line, stdout_fh=stdout_fh,
                                 TimeOut_sec        = timeout_sec,
                                 SizeLimit_Kb       = self.description.size_limit_kb(),
                                 executer_generator = executer_class)

        time_end   = time.time() # [sec]

        # Close writeable file; re-open file to be readable.
        stdout_fh.close()
        stdout_fh = self.OUT_FileHandle(Mode="rb") 
        
        if error_type == executer.ErrorType.NONE: 
            self.result().time_to_execute_sec = time_end - time_start

        return stdout_fh, error_type

    def __repr__(self):
        txt  = "PROGRAM: %s\n" % self.description.file_name()
        txt += "CHOICE:  %s\n" % self.choice()
        return txt

