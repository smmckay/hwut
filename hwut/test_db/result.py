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
import hwut.io.mini_fly as fly

class TestResult(object):
    __slots__ = ("choice", "verdict", "time_to_execute_sec", "crc_32")

    def __init__(self, Choice, Verdict=None, TimeToExecute=None, Crc32=None):
        assert type(Choice) == str
        #assert TimeToExecute is not None

        self.choice              = Choice
        self.verdict             = Verdict
        self.time_to_execute_sec = TimeToExecute
        # Store a cyclic redundancy check number that enables to detect wether 
        # someone tampered with the correspondent GOOD-file.
        self.crc_32              = Crc32

    @staticmethod
    def from_string_list(TheList):
        assert len(TheList) == 4
        if TheList[1] == "None": verdict = None
        else:                    verdict = TheList[1]
        if TheList[2] == "None": time    = 0
        else:                    time    = float(TheList[2])
        if TheList[3] == "None": crc     = None
        else:                    crc     = float(TheList[3])
        
        result = TestResult(TheList[0], verdict, time, crc)
        return result

    def absorb(self, Other):
        self.verdict             = Other.verdict
        self.crc_32              = Other.crc_32
        self.time_to_execute_sec = Other.time_to_execute_sec
        
    def to_string_list(self):
        if self.time_to_execute_sec is None: 
            t_str = "None"
        else:                                
            t_str = "%0.6f" % self.time_to_execute_sec

        if self.crc_32 is None: 
            crc_str = "None"
        else:                   
            crc_str = "%i" % self.crc_32

        return [ 
            fly.write_string_trivial(self.choice)[:-1], self.verdict, 
            t_str, crc_str 
        ] 
        
    def __iter__(self):
        for x in self.to_string_list():
            yield x
        
    def set(self, Verdict, TimeToExecuteSec, Crc32):
        self.verdict             = Verdict
        self.time_to_execute_sec = TimeToExecuteSec
        self.crc_32              = Crc32

    def __eq__(self, Other):
        return     self.choice              == Other.choice \
               and self.verdict             == Other.verdict \
               and self.time_to_execute_sec == Other.time_to_execute_sec \
               and self.crc_32              == Other.crc_32 

    def __ne__(self, Other):
        return self.__eq__(Other)


