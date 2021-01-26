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
import time

import hwut.auxiliary.path as aux
import hwut.common    as common

class RenameStrategy(CoreStrategy):

    def __init__(self, Setup, NewApplicationName):
        assert Setup.__class__.__name__ == "Setup"

        self.__break_up_f    = False
        self.__failed_only_f = Setup.failed_only_f
        self.__new_application_name = NewApplicationName
        self.__old_application_name = OldApplicationName
        self.__related_entry        = None
        self.setup = Setup

    def do(self, TestInfo):
        if self.__interaction_info == "NONE": return "UNTOUCHED"

        # NOTE: Renaming can only happen for one single test application at a time. Thus, 
        #       there is only one single related database entry that we need to track.
        assert TestInfo.description.file_name() == self.__old_application_name
        if self.__related_entry is None:
            self.__related_entry = TestInfo.description.
        # Under certain circumstances (overwriting existing files) user interaction is required.
        if self.__interaction_info == "INTERACTIVE": 
            user_reply = aux.rename_file("./GOOD/" + old_protocol_file_name, "./GOOD/" + new_protocol_file_name, InteractiveF=True)
        elif self.__interaction_info == "ALL":
            user_reply = aux.rename_file("./GOOD/" + old_protocol_file_name, "./GOOD/" + new_protocol_file_name, InteractiveF=False)
        else:
            user_reply = ""
        if user_reply in ["ALL", "NONE"]:  
            self.interaction_info = user_reply

        if user_reply not in ["YES", "ALL"]: return "UNTOUCHED"

        # Perform the renaming
        old_protocol_file_name = TestInfo.GOOD_FileName()

        new_dummy = deepcopy(test)
        new_dummy.description.set_file_name(NewProgramName)

        new_protocol_file_name = new_dummy.GOOD_FileName()

        aux.rename_file(old_protocol_file_name, new_protocol_file_name)

        # Now, change the name of the original database entry
        common.history.register_renaming(self.__old_application_name, self.__new_application_name, self.choice())

        return "RENAMED"
        
    def _end_directory_tree(self):
        if self.__related_entry is None: return None
        assert self.__related_entry.__class__ == Test

        self.__related_entry.set_file_name(self.__new_application_name)

        return None # default: no result

    def break_up_requested(self):
        return self.__break_up_f

    def set_break_up_request(self):
        self.__break_up_f = True

    def handle_only_failed_experiments(self):
        return self.__failed_only_f

    def xml_database_write_permission(self):
        return True

    def is_only_database_query(self):
        return False

    def get_referred_date(self):
        return time.asctime()


