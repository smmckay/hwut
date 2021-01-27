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
# coding: utf-8
import hwut.auxiliary.make               as     make
import hwut.auxiliary.path               as     aux
import hwut.io.messages                  as     io
import hwut.io.mini_fly                  as     fly
import hwut.common                       as     common
from   hwut.test_db.test                 import Test
from   hwut.test_db.attributes.core      import E_Attr
from   hwut.test_db.attributes.database  import attribute_db
import hwut.test_db.attributes.fly_io    as     fly_io
import hwut.test_db.attributes.interview as     interview

from   StringIO import StringIO
from   copy     import deepcopy
import os
import sys
import stat
import time

class E_Hist:
    APP_NEW                   = 0  # App
    APP_DELETED               = 1  # App
    APP_ATTR_CHANGE           = 2  # App, Attribute
    APP_ATTR_NEW              = 3  # App, Attribute
    APP_ATTR_DELETED          = 4  # App, Attribute
    APP_ATTR_APPEND_TO_LIST   = 5  # App, Attribute, Element
    APP_ATTR_REMOVE_FROM_LIST = 6  # App, Attribute, Element
    VERDICT_CHANGE            = 7  # App, Choice
    ACCEPT_OUTPUT             = 8  # App, Choice

class TestDescription(dict):
    def __init__(self, Name=None): 

        for attribute, default in attribute_db.attribute_default_iterable():
            self[attribute] = deepcopy(default)

        if Name is not None:
            self[E_Attr.APP_FILE_NAME] = Name

    @classmethod
    def from_fly(cls, fh):
        result = cls()
        if result.fly_read(fh): return result
        else:                   return None

    @classmethod
    def from_interview(cls, AppName, HwutInfoStr):
        result    = cls(AppName)
        remainder = result._interview_title_extract(HwutInfoStr)
        result._interview_attributes_extract(AppName, remainder)
        return result

    @classmethod
    def from_NO_INFO(cls, AppName):
        """Generate a test description that tells 'NO --hwut-info'
        """
        result = cls(AppName)
        result.result_list()[0].verdict = "NO INFO"
        return result

    def absorb_TextExecutionInfo(self, TEI):
        self[E_Attr.CALL_INTERPRETER_LIST]        = TEI.interpreter_sequence
        self[E_Attr.CALL_STDOUT_POST_PROCESSOR]   = TEI.stdout_post_processor
        self[E_Attr.CALL_STDERR_POST_PROCESSOR]   = TEI.stderr_post_processor
        self[E_Attr.CALL_REMOTE_CONFIGURATION_ID] = TEI.remote_config_id
        self[E_Attr.APP_MAKE_DEPENDENT_F]         = TEI.make_f

    def absorb_TestDescription(self, TD):
        prev_result_list = self.result_list()

        for key, info in TD.iteritems():
            if   key == E_Attr.APP_BUILD_TIME_SEC:       
                continue
            else:
                self[key] = info

        # It the new description contains a CHOICE which has been already in
        # the current description, then overtake the information about it.
        for result in self.result_list():
            for prev_result in prev_result_list:
                if result.choice != prev_result.choice: continue
                result.absorb(prev_result)
                break

    def all_choices_same_result_f(self):     return self[E_Attr.OUT_SAME_F]
    def result_list(self):                   return self[E_Attr.RESULT_LIST]
    def file_name(self):                     return self[E_Attr.APP_FILE_NAME]
    def group(self):                         return self[E_Attr.APP_TITLE_GROUP]
    def interpreter_list(self):              return self[E_Attr.CALL_INTERPRETER_LIST]
    def extra_output_file_list_db(self):     return self[E_Attr.OUT_EXTRA_OUTPUT_FILE_LIST]
    def make_dependent_f(self):              return self[E_Attr.APP_MAKE_DEPENDENT_F]
    def remote_config_id(self):              return self[E_Attr.CALL_REMOTE_CONFIGURATION_ID]
    def make_time_sec(self):                 return self[E_Attr.APP_BUILD_TIME_SEC]
    def potpourri_f(self):                   return self[E_Attr.OUT_CMP_POTPOURRI_F]
    def shrink_empty_lines_f(self):          return self[E_Attr.OUT_SHRINK_EMPTY_LINES_F] 
    def backslash_is_slash_f(self):          return self[E_Attr.OUT_CMP_BACKSLASH_IS_SLASH_F] 
    def shrink_space_f(self):                return self[E_Attr.OUT_SHRINK_SPACE_F] 
    def temporal_logic_f(self):              return self[E_Attr.OUT_TEMPORAL_LOGIC_F]
    def temporal_logic_rule_file_list(self): return self[E_Attr.OUT_TEMPORAL_LOGIC_RULE_LIST]
    def title(self):                         return self[E_Attr.APP_TITLE]
    def time_out_detection_f(self):          return self[E_Attr.CALL_TIMEOUT_F]
    def size_limit_kb(self):                 return self[E_Attr.CALL_SIZE_LIMIT_KB]
    def vanished_f(self):                    return self[E_Attr.APP_VANISHED_F]
    def analogy_open_str(self):              return self[E_Attr.OUT_CMP_ANALOGY_TUPLE][0]
    def analogy_close_str(self):             return self[E_Attr.OUT_CMP_ANALOGY_TUPLE][1]
    def happy_pattern_list(self):            return [ regex     for regex, y     in self[E_Attr.OUT_CMP_HAPPY_PATTERN_LIST] ]
    def happy_pattern_string_list(self):     return [ regex_str for x, regex_str in self[E_Attr.OUT_CMP_HAPPY_PATTERN_LIST] ]
    def hwut_info_request_system_time(self): return self[E_Attr.APP_HWUT_INFO_REQUEST_TIME]

    def is_present(self):                    return os.access(self.file_name(), os.F_OK)

    def has_choice(self, ChoiceName):
        assert self.result_list() != []
        if ChoiceName is None:
            if self.result_list[0].choice == "": return True
            else:                                return False
        for result in self.result_list():
            if result.choice == ChoiceName:      return True
        return False

    def has_only_default_choice(self):
        return (len(self.result_list()) == 1) and (not self.result_list()[0].name)

    def vanished_f_set(self, Value=True):                
        self[E_Attr.APP_VANISHED_F] = Value

    def set_title(self, Title, Group):                          
        self[E_Attr.APP_TITLE] = Title
        if Group is not None: 
            self[E_Attr.APP_TITLE_GROUP] = Group

    def set_file_name(self, Value):                      
        self[E_Attr.APP_FILE_NAME] = Value

    def make_history(self, NewSelf):
        """Reports changes from 'self' to 'NewSelf' in a history object. The 
        'NewSelf' is supposed to be the replacement for this 'self' in the 
        updated test database.

        RETURNS: 'history', i.e. a list of tuples reporting on changes in 
                 this TestDescription. 
        """
        history = []
        for key, old_value in self.iteritems():
            new_value = NewSelf.get(key)
            if new_value is None: 
                history.append((E_Hist.APP_ATTR_DELETED, key))
            elif old_value != new_value:
                if attribute_db.is_list(key):
                    pass # self.make_history_on_lists(key, old_value, new_value)
                else:
                    history.append((E_Hist.APP_ATTR_CHANGE, key, new_value))
            else:
                continue

        for key, new_value in NewSelf.iteritems():
            if key in self: continue

            history.append((E_Hist.APP_ATTR_NEW, key, new_value))
            if attribute_db.is_list(key):
                pass # self.make_history_on_lists(key, [], new_value)

        return history

    def get_Test_list(self, Selector):
        """Sequentializes the experiments for a given test application. Every
           choice of an application becomes becomes a test on its own. The
           'fitness' function may decide whether to consider a choice or not.

        RETURNS: list of 'Test' objects. 
        """
        if self.vanished_f(): 
            return [], []

        sequence = []
        skipped  = []
        for i, result in enumerate(self.result_list()):
            test = Test(self, i)
            if Selector.is_admissible(result): sequence.append(test)
            else:                              skipped.append(test)

        return sequence, skipped

    def make(self):
        if not make.is_remake_required(self.file_name()):
            return True
        time_start = time.time() # [sec]
        verdict    = make.make(self.file_name())
        time_end   = time.time() # [sec]

        self[E_Attr.APP_BUILD_TIME_SEC] = time_end - time_start
        return verdict

    def consistency_check(self):
        choice_name_set = set(x.choice for x in self.result_list())
        if len(choice_name_set) != len(self.result_list()):
            io.on_database_entry_consistency_check_choice_more_than_once(self, choice_name)
            return False
        elif len(choice_name_set) == 1: 
            return True
        elif "" in choice_name_set:
            # empty choice and multiple choices cannot be
            io.on_database_entry_consistency_check_empty_choice_in_multiple_choices(self)
            return False
        else:
            return True

    def __setitem__(self, Key, Value):
        """Here is where change may be detected and history may be traced!"""
        dict.__setitem__(self, Key, Value)

    def fly_write(self, fh):
        txt = []
        for attribute, value in sorted(self.iteritems()):
            default = attribute_db.get_default(attribute) 
            if value == default: continue

            name   = attribute_db.get_name(attribute)
            writer = fly_io.writer_db[attribute_db.get_type(attribute)]

            txt.append("%s: %s\n" % (name, writer(value)))

        fh.write("".join(txt))

    def fly_read(self, fh):
        """Iterates through 'fly' struct content expressions and writes them
        into the 'self's dictionary.

        RETURNS: True  -- if all mandatory attributes appeared. 
                 False -- if not.
        """
        remaining_mandatory = set(['file_name'])

        if not fly.is_struct_begin(fh): 
            return None

        while not fly.is_struct_end(fh):
            name = fly.read_label(fh)
            if name is None or not name: break

            attribute = attribute_db.get_attribute(name)
            parser    = fly_io.parser_db[attribute_db.get_type(attribute)]
            if parser is None: continue

            self[attribute] = parser(fh)

            if name in remaining_mandatory: 
                remaining_mandatory.remove(name)
    
        return not remaining_mandatory

    def _interview_title_extract(self, HwutInfoStr):
        title_line, remainder = self._interview_title_get_line(HwutInfoStr)

        self._interview_title_set(title_line)

        return remainder

    def _interview_title_set(self, TitleStr):
        if TitleStr is None:
            self.result_list()[0].verdict = "NO INFO"
            return self

        # title: title text ';'
        #          group name ':' title text ';'
        title = TitleStr.strip()
        index = title.find(":")
        if index != -1:
            group = title[:index].strip()
            title = title[index+1:].strip()
        else:
            group = None

        self.set_title(title, group)

    @staticmethod
    def _interview_title_get_line(HwutInfoStr):
        """RETURNS: [0] title line
                    [1] remainder of info source code.

        The title line is None, if there was no reasonable header.
        """
        # If there is a newline, then the title is the first line
        idx_nl = HwutInfoStr.find("\n")   
        if idx_nl != -1:
            title_line = HwutInfoStr[:idx_nl].strip()
            # If there is non-whitespace after the last ';' then this is an error
            idx_sc = title_line.find(";")
            if idx_sc != -1:
                if idx_sc != len(title_line) - 1:
                    print "Error: Response to '--hwut-info'"
                    print "Error: Title line"
                    print "Error: '%s'" % title_line.replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r")
                    print "Error: contains non-whitespace after ';'" 
                    return None, None
                else:
                    title_line = title_line[:idx_sc]
            else:
                title_line = title_line
            idx_rmd = idx_nl
        else:
            # If there is no newline, split via ';'
            idx_sc = HwutInfoStr.find(";")    
            if idx_sc == -1: 
                title_line = HwutInfoStr
                idx_rmd    = len(HwutInfoStr)
            else:            
                title_line = HwutInfoStr[:idx_sc]
                idx_rmd    = idx_sc

        remainder = HwutInfoStr[idx_rmd:].strip()

        return title_line, remainder

    def _interview_attributes_extract(self, AppName, RemainderStr):
        if RemainderStr is None: return
        self[E_Attr.APP_HWUT_INFO_REQUEST_TIME] = long(os.stat(AppName).st_mtime)

        # Find 'CHOICES', 'SAME', and other options.
        for raw_line in RemainderStr.split(";"):
            raw_line = raw_line.lstrip()
            fields   = raw_line.split()
            if not len(fields): continue

            key_word  = fields[0]
            bracket_i = key_word.find("(")
            if bracket_i != -1: key_word = key_word[:bracket_i]

            line = raw_line[len(key_word)+1:].strip()

            handler = interview.handler_db.get(key_word)
            if handler is None:
                print "Warning: test '%s'" % AppName
                print "Warning:   response to '--hwut-info' with unknown keyword"
                print "Warning:   '%s'." % key_word
                continue

            handler(self, line)

    def __repr__(self):
        fh = StringIO()
        self.fly_write(fh)
        return fh.getvalue() 


