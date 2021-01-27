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
import hwut.common            as     common
from   hwut.common            import color
import hwut.auxiliary.table   as     table
import hwut.io.colorize_map   as     colorize_map
import hwut.auxiliary.path    as     path

import os
import sys
from   operator  import itemgetter
from   itertools import izip
from   copy      import copy

class something:
    pass

__setup = something()
__setup.print_raise_write_protection_f    = False
__setup.print_update_program_entry_info_f = False

def formatted_output(Header, Message):
    word_list = Message.split()
    MaxL = common.terminal_width() - len(Header) - 7

    line = ""
    line_size = 0
    for word in word_list:
        if line_size + len(word) > MaxL:
            print Header + ": " + line
            line_size = 0
            line = ""
        line += word + " "
        line_size += len(word) + 1

    if line_size != 0:
        print Header + ": " + line
    sys.stdout.flush()

def print_line_separator(NewlineF=True):
    sys.stdout.write("-" * (max(0, common.terminal_width() - 1)) + "\n")
    sys.stdout.flush()

def print_double_line_separator():
    sys.stdout.write(color().Fore.YELLOW)
    sys.stdout.write("=" * (max(0, common.terminal_width() - 1)) + "\n")
    sys.stdout.write(color().Style.RESET_ALL)
    sys.stdout.flush()

def print_coverage(Coverage):
    print_line_separator()
    txt = art_coverage_str
    txt = __concatenate_art_strings(txt, art_space_str)
    txt = __concatenate_art_strings(txt, __get_art_number(Coverage))
    txt = __concatenate_art_strings(txt, art_percent_str)
    print txt,
    print " = sum(coverage(function) * line_number(function)) / total_sum(line numbers)"
    sys.stdout.flush()

def print_ok(Dir, MissingGoodFilesF=False, MultipleDirsF=False):
    if MultipleDirsF == False:
        print
        txt = art_ok_str
        if MissingGoodFilesF:
            print __concatenate_art_strings(txt, art_question_mark_str)
        else: 
            print __concatenate_art_strings(txt, art_exclamation_mark_str)
    else:
        if MissingGoodFilesF:
            print_right_aligned(art_single_okq_str, color().Fore.YELLOW)
        else:
            print_right_aligned(art_single_ok_str, color().Fore.GREEN)

def __print_short_summary(Dir, TestList, Label):
    iterable = (
        (test_info.description.file_name(), test_info.choice())
        for test_info in TestList
    ) 
    __print_short_summary_core(Dir, iterable, Label)

def __print_short_summary_core(Dir, NameChoicePairIterable, Label):
    prev_file_name = ""
    txt = []
    for file_name, choice in NameChoicePairIterable:
        if file_name != prev_file_name:
            if choice:
                txt.append("    %s %s _ %s\n" % (Label,  file_name, choice))
            else:
                txt.append("    %s %s\n" % (Label,  file_name))
        else:
            txt.append("    %s\__ %s\n" % (" " * (len(Label) + len(prev_file_name)),
                       choice))
        prev_file_name = file_name

    sys.stdout.write("".join(txt))
    sys.stdout.flush()

def print_failure(Dir, NameChoicePairList, MultipleDirsF=False):
    print_right_aligned(art_single_fail_str, color().Fore.RED)
    print_line_separator()
    __print_short_summary_core(Dir, NameChoicePairList, "[FAIL]")

def print_right_aligned(ArtText, Color=None):
    H       = horizontal_size(ArtText)
    padding = common.terminal_width() - 1 - H

    txt  = __concatenate_space("\n" * (ArtText.count("\n")+1), padding)
    if Color is not None: txt  = __concatenate_same(txt, Color)
    txt  = __concatenate_art_strings(txt, ArtText)
    txt += color().Style.RESET_ALL
    sys.stdout.write(txt)

def colorize(txt):
    txt = txt.replace("$S", color().Fore.BLACK)
    txt = txt.replace("$B", color().Fore.BLUE)
    txt = txt.replace("$R", color().Fore.RED)
    txt = txt.replace("$G", color().Fore.GREEN)
    txt = txt.replace("$C", color().Fore.CYAN)
    txt = txt.replace("$Y", color().Fore.YELLOW)
    txt = txt.replace("$",  color().Style.RESET_ALL)
    return txt

def print_bye_bye():
    print_line_separator()
    # art_bye_str_color = colorize(art_bye_str)

    H_console = common.terminal_width()
    H_loco    = horizontal_size(art_locomotive_str)
    H_wagon   = horizontal_size(art_wagon_str)
    H_bye     = horizontal_size(art_bye_str) 

    bye_f   = False
    loco_f  = False
    wagon_n = 0
    while True:
        remainder = H_console

        if H_bye > remainder:  break
        bye_f      = True
        remainder -= H_bye

        if H_loco > remainder: break
        loco_f     = True
        remainder -= H_loco

        if H_wagon > remainder: break
        wagon_n    = int(remainder / H_wagon)
        remainder -= wagon_n * H_wagon
        break
        
    txt = "\n" * art_locomotive_str.count("\n")
    if loco_f: 
        txt = __concatenate_art_strings(txt, art_locomotive_str)
    for i in xrange(wagon_n):
        txt = __concatenate_art_strings(txt, art_wagon_str)

    if bye_f:
        if remainder > 1:
            txt = __concatenate_padding(txt, art_rail_str, remainder-1)
        txt = __concatenate_art_strings(txt, art_bye_str)

    sys.stdout.write(txt)
    sys.stdout.flush()

def __time_string(Time_sec):
    if Time_sec is None:
        return "--:--:--:---"

    time_sec  = float(Time_sec)

    time_h     = int(time_sec / 3600.0)
    time_sec  -= time_h * 3600.0
    time_min   = int(time_sec / 60.0)
    time_sec  -= time_min * 60.0
    time_msec  = (time_sec - int(time_sec)) * 1000
    time_sec   = float(int(time_sec))

    txt = ""
    if time_h == 0:    txt += "   "
    else:              txt += "%2i:" % time_h
                       
    if time_min == 0:  txt += "   "
    elif time_h == 0:  txt += "%2i:"  % time_min
    else:              txt += "%02i:" % time_min
                       
    if time_sec == 0:  txt += "   "
    elif time_min == 0:txt += "%2i:"  % time_sec
    else:              txt += "%02i:" % time_sec

    if time_msec == 0: txt += "  0"
    elif time_sec == 0:txt += "%3i"  % time_msec
    else:              txt += "%03i" % time_msec

    return txt

def __print_x(Title, Msg, Border=4, Dot="."):
    L      = max(0, common.terminal_width() - Border)
    MsgL   = color().plain_length(Msg) + 2
    TitleL = color().plain_length(Title)
    TotalL = TitleL + MsgL

    space  = Dot * (L - TotalL)
    result = "%s%s%s\n" % (Title, space, Msg)

    return result

def __print(Title, Msg, Border=4, Dot="."):
    label = get_label_for_verdict(Msg)
    return __print_x(Title, label, Border, Dot)

def print_total_time(Directory, TotalExecutionTime, TotalMakeTime):
    print_line_separator()
    print __print("Execution Time ", __time_string(TotalExecutionTime)),
    print __print("Make Time ",      __time_string(TotalMakeTime)),
    print __print("Total Time Sum ", __time_string(TotalMakeTime + TotalExecutionTime)),
    sys.stdout.flush()

def print_test_time(Element, SuppressApplicationNameF):
    __print_about_experiment_end(Element, 
                                 __time_string(Element.result().time_to_execute_sec), 
                                 SuppressApplicationNameF=SuppressApplicationNameF)

def print_make_time(Element):
    __print_about_experiment_end(Element, 
                                 __time_string(Element.description.make_time_sec()),
                                 AlternativeLabel="<<MAKE>>")

def __print_about_experiment_end(TestInfo, Msg, AlternativeLabel="", SuppressApplicationNameF=False):
    Title, TitleL = __get_application_call_description(TestInfo, AlternativeLabel, SuppressApplicationNameF)
    txt = __print(Title, Msg)
    sys.stdout.write(txt)
    sys.stdout.flush()

def dir_string(Dir, PrevDir):
    # Find common directories in directory strings.
    dir_node_i = -1
    LPD = len(PrevDir)
    for i, letter in enumerate(Dir): 
        if i >= LPD: break
        if letter != PrevDir[i]: break
        if letter == "/" or letter == "\\": dir_node_i = i

    # No commonalities --> return directory as is
    if dir_node_i == -1: return Dir
    return "." * dir_node_i + Dir[dir_node_i:]

def print_summary(Directory_vs_Result_Pairs, DirsWithMissingGOODFiles=[]):
    # len_of_dir_plus_result = map(lambda x: x[0] + x[1], Directory_vs_Result_Pairs)
    # len_of_dir_plus_result = map(path.relative_to_home_pretty, len_of_dir_plus_result)
    print_double_line_separator()
    Directory_vs_Result_Pairs.sort(
        key=lambda x: ("" if path.relative_to_home_pretty(x[0]) == "(this directory)" else x[0])
    )

    if not Directory_vs_Result_Pairs:
        print "\n   Nothing has been done.\n"
        return

    if len(Directory_vs_Result_Pairs) == 1:
        return

    print "\nSUMMARY:\n"

    # total_n: x[3]; good_n: x[2]; fail_n = total_n - good_n
    total_fail_n = sum(x[3] - x[2] for x in Directory_vs_Result_Pairs)
    total_test_n = sum(x[3] for x in Directory_vs_Result_Pairs)

    total_verdict = "[OK]"
    if total_fail_n != 0: total_verdict = "[FAIL]"

    txt = []
    if len(Directory_vs_Result_Pairs) != 1:
        txt.append(("Fails:", "N:", "Verdict:", "Directory:"))

    def get_verdict_str(Verdict):
        label = get_label_for_verdict(Verdict)
        if   Verdict == "OK":   return "    %s" % label
        elif Verdict == "DONE": return "  %s"   % label
        elif Verdict == "NONE": return "    %s" % label
        else:                   return "  %s"   % label

    def get_fail_n_str(FailN):
        if FailN > 0: return "%5i" % FailN
        else:         return ""

    prev_dir = ""
    for dir, verdict, good_n, total_n in Directory_vs_Result_Pairs:
        verdict_str = get_verdict_str(verdict)
        # dir_str     = dir_string(path.relative_to_home_pretty(dir), prev_dir)
        dir_str     = dir_string(dir, prev_dir)
        fail_n_str  = get_fail_n_str(total_n - good_n)

        txt.append((fail_n_str, "%i" % total_n, verdict_str, dir_str))
        prev_dir = dir

    # Print table
    #
    max_l = table.max_cell_widths(txt)
    print "    " + table.get_row(txt[0], max_l, Pad=" ")
    print 
    for line in txt[1:]:
        print "    " + table.get_row(line, max_l, Pad=" ")
    print

    # Print Big Result
    #
    print_line_separator()
    if total_verdict.strip() == "[FAIL]":
        txt = art_space_str
        if   total_fail_n == 1:
            txt = __concatenate_art_strings(txt, art_fails_once_str)
        elif total_fail_n == 2:
            txt = __concatenate_art_strings(txt, art_fails_twice_str)
        elif total_fail_n == 3:
            txt = __concatenate_art_strings(txt, art_fails_trice_str)
        else:
            txt = __concatenate_art_strings(txt, art_fails_str)
            txt = __concatenate_art_strings(txt, art_space_str)
            txt = __concatenate_art_strings(txt, __get_art_number(total_fail_n, IntF=True))
            txt = __concatenate_art_strings(txt, art_space_str)
            txt = __concatenate_art_strings(txt, art_x_str)
    else:
        dirs_with_missing_good_files = map(path.relative_to_home_pretty, 
                                           DirsWithMissingGOODFiles)
        txt = art_ok_str
        if dirs_with_missing_good_files != []:
            txt = __concatenate_art_strings(txt, art_question_mark_str)
        else:
            txt = __concatenate_art_strings(txt, art_exclamation_mark_str)

    # Take out empty lines
    txt = ["%s\n" % line for line in txt.splitlines() if line.strip()]

    if total_test_n == 0: 
        ok_ratio = 1.0
    else:
        ok_ratio = float(total_test_n - total_fail_n) / float(total_test_n)

    if True:
        txt.append("%s\n" % right_aligned_colored("(%i tests)" % total_test_n, 
                                                 GreenRatio=ok_ratio))
        print "".join(txt)
    else:
        txt.append("%s\n" % right_aligned("(%i tests)" % total_test_n)) 

        size_x = max(len(line) for line in txt) #common.terminal_width()
        # size_x = max(size_x, common.terminal_width())
        txt    = ["%s%s" % (line, "-" * (size_x - len(line))) for line in txt]
        for line in txt:
            print line,

        print colorize_map.do(txt, 1.0 - ok_ratio),

    print_double_line_separator()
    sys.stdout.flush()

def right_aligned(Text):
    padding_n = common.terminal_width() - len(Text) - 1
    if padding_n < 0: padding_n = 0
    print "%s%s" % (" " * padding_n, Text)

def right_aligned_colored(Text, GreenRatio):
    padding_n = common.terminal_width() - len(Text) - 1
    if padding_n < 0: padding_n = 0
    padding_str = "%s" % (" " * padding_n)

    green_n     = len(padding_str) * GreenRatio
    return "%s%s%s%s%s%s" % (           \
           color().Back.GREEN,          \
           padding_str[:int(green_n)],  \
           color().Back.RED,            \
           padding_str[int(green_n):],  \
           color().Style.RESET_ALL,     \
           Text)


def print_time_summary(Directory_vs_TimeResult_Pairs):
    print_double_line_separator()
    
    # sort by total time
    Directory_vs_TimeResult_Pairs.sort(lambda x, y: - cmp(x[1].make + x[1].execute, y[1].make + y[1].execute))
    print "SUMMARY:"
    print 
    print "  Total Time:   Make Time:    Directory:"
    sum_total = 0.0
    sum_make = 0.0
    for dir, result in Directory_vs_TimeResult_Pairs:
        ## if   result == "OK":   judgement = "[OK]"
        ## elif result == "DONE": judgement = "[DONE]"
        ## else:                  judgement = "[FAIL]"
        sum_total += result.make + result.execute
        sum_make  += result.make
        mtime_str = __time_string(result.make)
        ttime_str = __time_string(result.execute + result.make)
        dir       = path.relative_to_home_pretty(dir)
        prefix = ""
        # if dir in dirs_with_missing_good_files: prefix = "??"
        print "  " + ttime_str + "  " + mtime_str + "  " + dir

    print_line_separator()
    make_time_percentage = 0.0
    if sum_total != 0.0: make_time_percentage = 100.0 * sum_make / sum_total 
    print "  " + __time_string(sum_total) + "  " + __time_string(sum_make) + "  (make time = %.2f%%)" % make_time_percentage
    print_double_line_separator()
    sys.stdout.flush()

def on_directory_enter(Dir, Title, DateStr, ExecutionName=None):
    print_double_line_separator()

    dir_name = path.relative_to_home_pretty(Dir)
    if dir_name == "(this directory)": dir_name = ""
    
    L  = common.terminal_width() - 1
    if ExecutionName is not None:
        execution_box,     \
        execution_box_size = frame_text(ExecutionName, 
                                        color().Fore.RED + color().Back.YELLOW, 
                                        color().Fore.BLACK)
    else:
        execution_box      = "\n\n\n"
        execution_box_size = 0

    Lt = len(Title)
    if Lt < L: padding_right = padding_left = (L - Lt) / 2
    else:      padding_right = padding_left = 0

    padding_left -= execution_box_size
    if padding_left < 0:
        padding_right = max(0, padding_right - padding_left)
        padding_left  = 0

    if padding_left + padding_right + Lt + execution_box_size < L:
        padding_right = L - (padding_left + Lt + execution_box_size)

    left_str  = " " * padding_left
    right_str = " " * padding_right


    color_on  = "%s%s" % (color().Back.YELLOW, color().Fore.BLACK)
    color_off = color().Style.RESET_ALL

    empty_line = "%s%s%s" % (color_on, " " * (L - execution_box_size), color_off)

    title_txt = "".join([
        "%s\n"         % empty_line,
        "%s%s%s%s%s\n" % (color_on, left_str, Title, right_str, color_off),
        "%s\n"         % empty_line,
    ])

    txt = __concatenate_art_strings(execution_box, title_txt)
    sys.stdout.write(txt)

    Ln   = len(dir_name)
    Ld   = len(DateStr)
    Lmax = L - Ld - 3
    pruned_name = dir_name
    if Ln > Lmax:
        Lcut = Ln - Lmax + 3
        if Ln > Lcut: pruned_name = "...%s" % pruned_name[Lcut:]
        else:         pruned_name = ""


    space2 = " " * (L - len(pruned_name) - Ld - 2)
    sys.stdout.write("%s%s %s\n"    % (pruned_name, space2, DateStr))
    print_line_separator()
    sys.stdout.flush()

def on_no_test_application_found(Selector, Dir):
    Dir = path.relative_to_home_pretty(Dir)
    Program     = Selector.app_pattern
    Choice      = Selector.choice_pattern
    FailedOnlyF = Selector.failed_only_f
    txt = "   Directory: " + Dir + "\n"
    if Program is None:
        if FailedOnlyF:
            txt += "   No failed test found!\n"
        else:
            txt += "   No test not found!\n"
    else:
        if Choice:
            txt += "   Test '%s', choice '%s' not found!\n" % (Program, Choice)
        else:
            txt += "   Test '%s' not found!\n" % Program
        if FailedOnlyF:
            txt += "   Maybe, the application did not fail. You specified '--fail'."

    print 
    print txt
    sys.stdout.flush()

def no_hwut_related_directories_found():
    print "Error: Recursive search did not find a directory '%s'!" % common.TEST_DIR_NAME
    print "Error: May be, set environment variable HWUT_TEST_DIR_NAME!"
    sys.stdout.flush()
    common.exit(-1)

def on_test_start(TestInfo):
    """GroupElementF = False allows to categorically block a decision wether 
       to treat the test as part of a group or not.
    """
    GroupedF = TestInfo.description.group() != ""
    FirstChoiceF = TestInfo.first_f()

    if not FirstChoiceF:
        sys.stdout.write("")
    else:
        if GroupedF: 
            sys.stdout.write("    %s\n" % TestInfo.description.title())
        else:   
            sys.stdout.write(" * %s\n" % TestInfo.description.title())
    sys.stdout.flush()

def on_test_group_start(TestInfo):
    GroupName = TestInfo.description.group()
    if GroupName: sys.stdout.write("\n * %s:\n\n" % GroupName)
    sys.stdout.flush()

def on_choice_not_available(TestInfo):
    sys.stdout.write("        (program '%s' does not provide choice '%s')" % \
                     (TestInfo.file_name(), TestInfo.choice()))
    sys.stdout.flush()

def warning_recompute_crc_for_good_file_because_none_found(TestInfo):
    sys.stdout.write("        (compute new CRC for file 'GOOD/%s')\n" % TestInfo.GOOD_FileName())
    sys.stdout.flush()

def general_error(Str):
    print "Error: " + Str
    sys.stdout.flush()

def error_crc32_mismatch(TestInfo):
    sys.stdout.write("        (CRC check failed for 'GOOD/%s' !)\n" % TestInfo.GOOD_FileName())
    sys.stdout.flush()

def on_test_is_good_already(TestInfo):
    on_test_end(TestInfo, "ALREADY GOOD")
    sys.stdout.flush()

def __get_application_call_description(TestInfo, AlternativeLabel="", SuppressApplicationNameF=False):
    Program = TestInfo.description.file_name()
    if AlternativeLabel == "": Choice = TestInfo.choice()
    else:                      Choice = AlternativeLabel
    if Choice != "":
        # print test program name only on first choice
        if TestInfo.first_f() == False or SuppressApplicationNameF: 
            Label = " " * len(Program) + " " + Choice
        else:
            Label = Program + " " + Choice
    else:   
        if SuppressApplicationNameF: Label = " " * len(Program)
        else:                        Label = Program

    return "        %s " % Label, len(Label)

def on_test_end(TestInfo, Result, ExtraFileVerdictDb=None):
    __print_about_experiment_end(TestInfo, Result)
    if ExtraFileVerdictDb is not None:
        LastI = len(ExtraFileVerdictDb) - 1
        for i, info in enumerate(sorted(ExtraFileVerdictDb.iteritems())):
            extra_file_name, verdict = info
            extra_file_comparison_verdict(TestInfo, extra_file_name, verdict, i==LastI)
    sys.stdout.flush()

def extra_file_comparison_verdict(TestInfo, FileName, CmpVerdict, LastF):
    Program = TestInfo.description.file_name()
    if   LastF: c = "'"
    else:       c = ":"

    file_description_str = "%s-(file)- %s " % (c, FileName)
    Title                = "        %s %s" % (" " * len(Program), file_description_str)
    txt                  = __print(Title, CmpVerdict)
    sys.stdout.write(txt)
    sys.stdout.flush()

def on_update_program_entry_info(Filename):
    if __setup.print_update_program_entry_info_f:
        print "Update: call '%s --hwut-info'" % Filename
    sys.stdout.flush()

def on_database_entry_consistency_check_choice_more_than_once(Entry, ChoiceName):
    formatted_output("Warning", "Choice '%s' appeared more than once for application '%s'.\n" % \
                     (ChoiceName, Entry.file_name()) + \
                     "Choices are " + repr(map(lambda c: c.name, Entry.choice_list()))[1:-1])

def on_database_entry_consistency_check_empty_choice_in_multiple_choices(Entry):
    print "Inconsistency: Empty Choice '' appeared together with other choices in '%s'." % \
            (Entry.file_name())
    print "Inconsistency: Choices: ", repr(map(lambda x: x.name, Entry.choice_list()))
    sys.stdout.flush()

def on_update_program_entry_info_all_terminated():
    print  # newline after possible "// update:" messages
    sys.stdout.flush()

def on_copied_OUT_to_GOOD(Dir, Filename):
    print __print(Filename, "COPIED TO GOOD", 2)
    sys.stdout.flush()
    return

def print_missing_good_files(DB):
    for dir, test_list in DB.items():
        if not test_list: continue
        __print_short_summary(dir + "/GOOD", test_list, "[NO GOOD FILE]")

def print_missing_out_files(DB):
    for dir, test_list in DB.items():
        __print_short_summary(dir + "/OUT", test_list, "[NO OUT FILE]")

def on_raise_write_protection(Dir, Filename):
    if __setup.print_raise_write_protection_f:
        sys.stdout.write("set write protection for '%s/%s'\n" % (Dir, Filename)) 

def on_no_test_program_specified():
    print "Error: no test program specified"

def on_make_only_this(Program):
    print "make: %s" % Program,   # ',' means that there's stuff to be appended.
    sys.stdout.flush()

def on_make_only_this_end(MakeTarget, SuccessF):
    if SuccessF: result = get_label_for_verdict("MADE")
    else:        result = get_label_for_verdict("MAKE FAILED")

    __on_end("make: %s" % MakeTarget, result)

def on_query_remote_application_list(RemoteConfigId):
    print "query remote: %s" % RemoteConfigId,   # ',' means that there's stuff to be appended.
    sys.stdout.flush()

def on_query_remote_application_list_end(RemoteConfigId, RemoteAppN):
    result = "%s[%i APPS]%s" % (color().Back.GREEN, RemoteAppN, color().Style.RESET_ALL)
    __on_end("query remote: %s" % RemoteConfigId, result)

def on_make_bunch_of_test_programs(Bunch):
    for program in Bunch:
        print "make: %s" % program
    sys.stdout.flush()

def __on_end(LeftLabel, RightLabel):
    L      = max(0, common.terminal_width())
    LeftL  = len(LeftLabel)
    RightL = len(RightLabel)
    txt    = " "
    if LeftL + RightL + 1 < L: 
        txt += "." * (L - LeftL - RightL)
    txt += "%s" % RightLabel
    print txt
    sys.stdout.flush()

def on_makefile_does_not_contain_target_hwut_info(Directory):
    print "Error: Directory: %s" % Directory
    print "Error:"
    print "Error:     Makefile: no response on 'make hwut-info'."
    print "Error:"
    sys.stdout.flush()

def on_makefile_does_not_report_coverage_related_source_files(Directory):
    formatted_output("Note", \
                     "Missing Makefile target 'hwut-gcov-info' and/or 'hwut-gcov-obj'.\n")

def on_makefile_does_not_report_coverage_related_object_directory(Directory):
    print "Error: Makefile in directory '%s'" % Directory
    print "Error: does not report a object directory 'hwut-gcov-obj'. " 
    print "Error: This is necessary, if you want to instruct hwut to investigate coverage."
    print "Error: Please, add something like the following lines to your makefile:"
    print "Error:"
    print "Error: hwut-gcov-obj:"
    print "Error:     @echo the_dir_where_i_store_object_files"
    print "Error:"
    sys.stdout.flush()
    common.exit(-1)

def on_make_clean():
    print "make: clean"
    sys.stdout.flush()

def on_make_target_not_in_TEST_directory(MakeTarget):
    formatted_output("Error:", 
                     "Target of make '%s' is not placed in current directory. Please, " % MakeTarget + \
                     "write the make rules so that they place all test applications in " + \
                     "the current %s-directory." % common.TEST_DIR_NAME)
    common.exit(-1)

def on_warning_source_file_has_executable_rights(Filename):
    """Some files are usually considered source files that are to be compiled.
       If they have executable rights, it might get confusing.
    """
    formatted_output("Warning", 
                     "file '%s' has executable rights (normally considered to be a source file)." % Filename)

def on_database_not_found(Dir):
    formatted_output("Warning",  "No database file for hwut-information found for directory: " +
                     "%s" % Dir)

def on_database_no_entry_for_application_thus_ignored(ApplicationName):
    formatted_output("Warning", 
                     "'%s' has no entry in database--ignored." % ApplicationName)

def on_database_entry_no_such_choice(ApplicationName, Choice):
    if Choice is not None:
       formatted_output("Error", 
                        "'%s' in database does not provide the choice '%s'." % (ApplicationName, Choice))
    else:
       formatted_output("Error", 
                        "'%s' in database does require choice, but none was specified." % ApplicationName)
    common.exit(-1)

def on_database_entry_not_available(ApplicationName):
    formatted_output("Error", 
                     "'%s' in database but no longer available--dismissed." % ApplicationName)
    common.exit(-1)

def on_database_new_entry(ApplicationName):
    formatted_output("Note", "'%s' added to database." % ApplicationName) 

def on_database_contained_entry_multiple_times(ApplicationName):
    formatted_output("Warning", "'%s' appeared multiple times in database---dismissed." % ApplicationName) 

def on_xml_parsing_error(XMLFileName, ErrorMsg):
    formatted_output("Warning", 
                     "Parsing error in '%s' of directory '%s'. " % (XMLFileName, path.relative_to_home_pretty(os.getcwd())) + 
                     "XML parser reports '%s'. " % ErrorMsg + \
                     "XML file is cleared.")

def on_xml_database_entry_consistency_check_failed(Entry):
    print "Warning: Entry '%s' in xml-database of directory '%s'" % (Entry.file_name(), path.relative_to_home_pretty(os.getcwd()))
    print "Warning: is inconsistent. Entry is cleared and reset."

def on_application_does_not_exist_in_database(Application):
    formatted_output("Warning", 
                     "Application '%s' is not entered into database yet." % Application + \
                     "Consider running hwut in test mode. This will create an entry in the" + \
                     "database automatically.")

def on_program_is_not_executable(ApplicationName, OptionList):
    sys.stdout.write("\nError: Program '%s' is not executable (or does not exist)\n" % ApplicationName + \
                     "Error:\n" + \
                     "Error: current directory:    " + os.getcwd() + "\n" + \
                     "Error: command line options: " + repr(OptionList) + "\n" + \
                     "Error:\n" + \
                     "Error: -- Is this a script and you forgot to specify your interpreter?\n" + \
                     "Error:    If so, type '#! /usr/bin/env my_interpreter' in the first line of your file.\n" + \
                     "Error: -- Or, set the PATH variable so that it contains the path to your application!\n")
    common.exit(-1)

def xml_missing_attribute(Section, Attribute):
    print "Error: XML-File - missing attribute '%s' in section '%s'" % (Attribute, Section)

def on_unknown_diff_program(Program):
    print "Warning: diff program '%s' unknown to hwut." % Program

def on_found_unusual_executables(UnusualExecutableNameList):
    formatted_output("Warning",  
                     "The following executable names have been found, but they have unusual names " + \
                     "or extensions. HWUT ignores those files and **UNSETS** executable rights. " + \
                     "The list consists of the following: " + \
                     repr(UnusualExecutableNameList)[1:-1])

def on_database_recurred_entry(file):
    label = "check: %s " % file
    print __print(label, "RECURRED", 2)

def on_database_vanished_entry(file):
    label = "check: %s " % file
    print __print(label, "VANISHED", 2)

def on_history_file_not_found(Dir):
    formatted_output("Warning", "no history file found.")

def on_file_cannot_be_opened(Filename):
    #print "         Error: cannot open file '%s'" % Filename
    common.exit(-1)

def on_file_deleted(Filename):
    print "Deleted: '%s'" % Filename

def on_file_temporary_cannot_be_deleted(Filename):
    print "         warning: cannot delete temporary file '%s'" % Filename

def on_file_temporary_cannot_be_opened(Filename):
    #print "         Error: cannot open temporary file '%s'" % Filename
    common.exit(-1)

def on_file_log_file_cannot_be_opened(Filename):
    print "         Error: cannot error log file '%s'" % Filename
    common.exit(-1)

def on_file_access_error(Filename):
    # formatted_output("Error", "file '%s'" % Filename + " cannot be accessed")
    pass

def on_file_does_not_exist(Filename):
    extention = os.path.splitext(Filename)
    if len(extention) == 0: Rule = Filename
    else:                   Rule = "*%s" % extention[1]
    formatted_output("Error", 
                     "File '%s'" % Filename + " is not accessible. " \
                     "Maybe, add rule %s in file 'ADM/scripts.txt'" % Rule)
    sys.exit(-1)

def on_file_missing_GOOD_file(TestInfo):
    pass
    # sys.stdout.write(
	#                "        (missing 'GOOD/%s')\n" % TestInfo.GOOD_FileName())

def on_file_missing_OUT_file_during_accept(TestInfo, TestRunAllowedF):
    if TestRunAllowedF: 
        message = "        (missing '%s', running test ...)\n" % TestInfo.OUT_FileName()
    else:
        message = "        (missing '%s', user forbid test run, no accept)\n" % TestInfo.OUT_FileName()
    sys.stdout.write(message) 

def on_file_system_object_does_not_exist(Filename, Comment):
    formatted_output("Error", "'%s'" % Filename + " does not exist. " + Comment)

def display_function_coverage_results(EntryList, RelevantFunctionNameList):
    L = max(0, common.terminal_width() - 9)

    def report(function_name, entry, BracketF):
        FunctionL = len(function_name)
        coverage_str = "(%i) %5.1f%%" % (entry.line_n, (entry.line_coverage * 100.0))
        CoverageL = len(coverage_str)

        if   BracketF:              txt = "  ( " 
        elif entry.occurence_n > 1: txt = "  + "
        else:                       txt = "    "
        txt += function_name
        if FunctionL + CoverageL < L: 
            txt += "." * (L - FunctionL - CoverageL)
        txt += "%s" % coverage_str
        if BracketF: txt += " )" 
        else:        txt += "  "

        return txt

    print
    print "Functions:"
    # Separate the wheat from the chaff
    for function_name, entry in EntryList:
        if RelevantFunctionNameList == [] or function_name in RelevantFunctionNameList:
            continue

        print report(function_name, entry, True)

    for function_name, entry in EntryList:

        if not (RelevantFunctionNameList == [] or function_name in RelevantFunctionNameList):
            continue

        print report(function_name, entry, False)

def display_file_coverage_results(FileList):
    L = max(0, common.terminal_width() - 9)

    print
    print "Files:"
    for entry in FileList:
        FileL        = len(entry.name)
        coverage_str = "%.1f%%" % (entry.line_coverage * 100.0)
        CoverageL = len(coverage_str)
        txt = "    " + entry.name
        if FileL + CoverageL < L: 
            txt += "." * (L - FileL - CoverageL)
        txt += "%s" % coverage_str
        print txt

def on_gcov_time_stamp_mismatch(SourceFile, GCNO_File, GCDA_File):
    print "related gcno: %s" % GCNO_File
    print "related gcda: %s" % GCDA_File
    print "Report files for file '%s' have different time stamp identifiers." % SourceFile
    print "This happens if files are build again after execution."
    sys.exit()


def on_gcov_no_output(FileName):
    formatted_output("Error", 
                     "Calling 'gcov' did not result in any output for file '" + FileName + "'. " + \
                     "A reason may be that a normal hwut run was not done yet.")

def on_gcov_missing_files(FileList):
    print
    print "   GCov is missing files!"
    print "   Has HWUT been run for testing yet?"
    print "   Are compile options '-fprofile-arcs -ftest-coverage' set?"
    print
    formatted_output("Missing", reduce(lambda a, b: a + ", " + b, FileList) + ".")

def error_on_gcov_non_english_language_detected():
    print "When using 'gcov' the shell must be set to 'english'. That is,"
    print "execute 'export LC_ALL=en' prior to executing hwut."
    sys.exit()
    
def error_on_try_to_execute(CommandLine):
    # formatted_output("Error",
    #                 "System failed to execute:\n" \
    #                 "%s" % "".join("%s " % x for x in CommandLine))
    pass

def horizontal_size(ArtText):
    if type(ArtText) == list:
        return max(color().plain_length(line) for line in ArtText)
    else:
        return max(color().plain_length(line) for line in ArtText.splitlines())

def on_first_keyboard_interrupt():
    global art_flash
    global art_keyboard_interrupt

    art_flash_size = horizontal_size(art_flash)
    text_size      = horizontal_size(art_keyboard_interrupt)
    total_size     = art_flash_size + text_size
    padding        = int(float(common.terminal_width() - 1 - total_size) / 5)
    if padding < 0: padding = 0

    txt = __concatenate_space("\n" * art_flash.count("\n"), padding)
    txt = __concatenate_same(txt, color().Fore.YELLOW)
    txt = __concatenate_art_strings(txt, art_flash)
    txt = __concatenate_same(txt, color().Fore.RED)
    txt = __concatenate_space(txt, padding)
    txt = __concatenate_art_strings(txt, art_keyboard_interrupt)
    txt = __concatenate_same(txt, color().Fore.YELLOW)
    txt = __concatenate_space(txt, padding)
    txt = __concatenate_art_strings(txt, art_flash)
    txt = __concatenate_same(txt, color().Style.RESET_ALL)
    print
    print txt

def no_response_to_hwut_info(AppName):
    print __print(AppName, "NO INFO", 2)

def remote_start_require_response_starting_with_key(EntryIdentifier):
    formatted_output("Warning:", "The given Makefile responded to 'make hwut-remote' in an unexpected manner. " + \
                     "A 'hwut-remote:' must start its output with the 'REMOTE' keyword, i.e. write something like " + \
                     "'@echo \"REMOTE\"' in the first line of your compile section. It is possible that you have " + \
                     "defined a default target which caught 'make hwut-remote', in this case ignore this warning, or " + \
                     "try to get rid of the 'catch-all' target.")

def report_coverage_summary(ReportList):

    if len(ReportList) == 1: 
        print_double_line_separator()
        return

    # Compute Average
    total_coverage = 0.0
    total_line_n   = 0.0
    max_line_n     = 0.0
    for dir, coverage, line_n in ReportList:
        if coverage == 0.0: continue
        total_coverage += coverage * line_n
        total_line_n   += line_n
        if line_n > max_line_n: max_line_n = line_n

    print_double_line_separator()
    print "SUMMARY:\n"
    print " LineN: Coverage: Directory:"
    print 

    L = 5
    prev_dir = ""
    for dir, coverage, line_n in ReportList:
        dir = path.relative_to_home_pretty(dir)

        line_n_str = "%i" % line_n
        print " " + (" " * int(L - len(line_n_str))) + line_n_str,
        print "  ",
        print "%5.1f%%" % coverage,
        print " ",
        print dir_string(dir, prev_dir)
        prev_dir = dir

    # Print total average
    if total_line_n != 0.0: total_avrg = total_coverage / total_line_n
    else:                   total_avrg = 0.0

    print_coverage(total_avrg)

    print_double_line_separator()

def remote_start_requires_definition_of_an_agent():
    formatted_output("Error:", 
                     "Missing 'AGENT:' statement. The given makefile defined a 'hwut-remote' target. This target **needs** to define " + \
                     "the agent on the remote device which is acting on the behalf of hwut.")
    sys.exit()

def remote_start_requires_definition_of_a_spy():
    formatted_output("Error:", 
                     "Missing 'SPY:' statement. The given makefile defined a 'hwut-remote' target. This target **needs** to define " + \
                     "the spy on the remote device which is sending data to hwut.")
    sys.exit()

def remote_start_requires_names_for_parameter(Name, List):
    formatted_output("Error:", 
                     "Missing parameter name in '%s' definition." % Name)
    sys.exit()

def remote_start_requires_the_type_as_first_argument(Name, List):
    formatted_output("Error:", 
                     "Missing type definition for '%s'." % Name + \
                     "There should be at least a definition of the type of the connection (TCP, UDP, etc.) as the first argument.")
    sys.exit()

def remote_start_requires_parameter_definition(Type, Name, Parameter, PresentParameterList):
    formatted_output("Error:", 
                     "Missing parameter '%s' for '%s' for connection of type '%s'. Present"  \
                     % (Parameter, Name, Type) + \
                     " parameters are %s." % repr(PresentParameterList)[1:-1])

def remote_start_remote_path_must_end_with_slash(Path):
    formatted_output("Error:", 
                     "Remote path specification '%s' does not end with slash or backslash."  \
                     % Path)
    sys.exit()

art_flash = \
"""   ,/  
 ,'/.-,
'--. ,'
  /,'  
 /'    
"""

art_keyboard_interrupt = \
""" 
Keyboard interrupt (Ctr-C) canceled execution.   
                                                 
(A quick a second keyboard interrupt aborts hwut)
"""
                                                 

art_coverage_str = \
"""  ____                                    
 / ___|_____   _____ _ __ __ _  __ _  ___ 
| |   / _ \ \ / / _ \ '__/ _` |/ _` |/ _ \\
| |__| (_) \ V /  __/ | | (_| | (_| |  __/
 \____\___/ \_/ \___|_|  \__,_|\__, |\___|
                               |___/      
"""

art_numbers_str = \
"""  ___    _   ____    _____   _  _     ____     __     _____    ___     ___       
 / _ \  / | |___ \  |___ /  | || |   | ___|   / /_   |___  |  ( _ )   / _ \      
| | | | | |   __) |   |_ \  | || |_  |___ \  | '_ \     / /   / _ \  | (_) |     
| |_| | | |  / __/   ___) | |__   _|  ___) | | (_) |   / /   | (_) |  \__, |  _  
 \___/  |_| |_____| |____/     |_|   |____/   \___/   /_/     \___/     /_/  (_) 
                                                                                 
"""

art_numbers_str_lines = art_numbers_str.splitlines()

art_number_position_db = { 
        "0": (0,  8),
        "1": (8,  4),
        "2": (12, 8),
        "3": (20, 8),
        "4": (28, 8),
        "5": (37, 9),
        "6": (45, 8),
        "7": (53, 8),
        "8": (61, 8),
        "9": (69, 8),
        ".": (77, 4),
}

art_space_str = \
"""    
    
    
    
    
    
"""

art_percent_str = \
""" _  __
(_)/ /
  / / 
 / /_ 
/_/(_)
      
"""

art_exclamation_mark_str = \
"""  _ 
 | |
 | |
 |_|
 (_)"""

art_question_mark_str = \
""" ___ 
 |__ \\
   / /
  |_| 
  (_) 
"""

art_ok_str = \
"""     ___  _ _   _  __                        _    
    / _ \| | | | |/ /___  _ __ _ __ ___  ___| |_ 
   | | | | | | | ' // _ \| '__| '__/ _ \/ __| __|
   | |_| | | | | . \ (_) | |  | | |  __/ (__| |_ 
    \___/|_|_| |_|\_\___/|_|  |_|  \___|\___|\__|"""


art_locomotive_str = """        ( ) )
       ()   
      --  -----
    __||__|[_]|
   o)__ |_| ..|
__<(__(O)__(O)_
"""

art_wagon_str = """
 ____.___._____
 |  _         |
 |.| |.[].[]..|
=|_|-|________|
~__(O)____(O)__
"""

art_rail_str = """




_
"""

art_bye_str = """ ____                 ____             _ 
| __ ) _   _  ___    | __ ) _   _  ___| |
|  _ \| | | |/ _ \   |  _ \| | | |/ _ \ |
| |_) | |_| |  __/_  | |_) | |_| |  __/_|
|____/ \__, |\___( ) |____/ \__, |\___(_)
_______|___/_____|/_________|___/________
"""

art_color_locomotive_str = """$C        ( ) )$
       $C()$   
      --  -----
    __||__|[_]|
   o)__ |_| ..|
__<(__($RO$)__($RO$)_
"""

art_color_wagon_str = """
$R____.___._____
 |  _         |
 |.| |.[].[]..|
=|_|-|________|
~__($RO$)____($RO$)__
"""

art_bye_str_color = """ $G____                 ____             _ $
$G| __ ) _   _  ___    | __ ) _   _  ___| |$
$G|  _ \| | | |/ _ \   |  _ \| | | |/ _ \ |$
$G| |_) | |_| |  __/_  | |_) | |_| |  __/_|$
$G|____/ \__, |\___( ) |____/ \__, |\___(_)$
_______$G|___/$_____$G|/$_________$G|___/$_________        
"""

art_trail_tr = """




_
"""

art_bye_bye_str = """$C        ( ) )                     $G____                 ____             _ $
       $C()$       $R____.___._____   $G| __ ) _   _  ___    | __ ) _   _  ___| |$
      $R--  -----$ $Y| $R _$         $Y|   $G|  _ \| | | |/ _ \   |  _ \| | | |/ _ \ |$
    $B__||__|[_]|$ $Y|$$B.$$R| |$$B.[].[]..$$Y|   $G| |_) | |_| |  __/_  | |_) | |_| |  __/_|$
   $Yo$$B)__ |_|$.-.|=$Y|_$R|$Y_$R|$Y________|   $G|____/ \__, |\___( ) |____/ \__, |\___(_)$
_ $B<($__(O)__(O)_~__(O)____(O)____________$G|___/$_____$G|/$_________$G|___/$_________        
"""

art_failure_str = \
"""    _____     _ _                  _ 
   |  ___|_ _(_) |_   _ _ __ ___  | |
   | |_ / _` | | | | | | '__/ _ \ | |
   |  _| (_| | | | |_| | | |  __/ |_|
   |_|  \__,_|_|_|\__,_|_|  \___| (_) """

art_distraught_str = \
"""        _ _     _                         _     _       
     __| (_)___| |_ _ __ __ _ _   _  __ _| |__ | |_     
    / _` | / __| __| '__/ _` | | | |/ _` | '_ \| __|    
   | (_| | \__ \ |_| | | (_| | |_| | (_| | | | | |_   _
    \__,_|_|___/\__|_|  \__,_|\__,_|\__, |_| |_|\__| (_)
                                    |___/               """
art_fails_str = \
""" _____     _ _     
|  ___|_ _(_) |___ 
| |_ / _` | | / __|
|  _| (_| | | \\__ \\
|_|  \\__,_|_|_|___/
"""
                   
art_fails_once_str = \
""" _____     _ _        ___                 
|  ___|_ _(_) |___   / _ \\ _ __   ___ ___ 
| |_ / _` | | / __| | | | | '_ \\ / __/ _ \\
|  _| (_| | | \\__ \\ | |_| | | | | (_|  __/
|_|  \\__,_|_|_|___/  \\___/|_| |_|\\___\\___|
"""

art_fails_twice_str = \
""" _____     _ _       _____          _          
|  ___|_ _(_) |___  |_   _|_      _(_) ___ ___ 
| |_ / _` | | / __|   | | \\ \\ /\\ / / |/ __/ _ \\
|  _| (_| | | \\__ \\   | |  \\ V  V /| | (__| __/
|_|  \\__,_|_|_|___/   |_|   \\_/\\_/ |_|\\___\\___|
"""

art_fails_trice_str = \
""" _____     _ _       _____     _          
|  ___|_ _(_) |___  |_   _| __(_) ___ ___ 
| |_ / _` | | / __|   | || '__| |/ __/ _ \\
|  _| (_| | | \\__ \\   | || |  | | (_|  __/
|_|  \\__,_|_|_|___/   |_||_|  |_|\\___\\___|
"""

art_x_str = \
"""      
__  __
\\ \\/ /
 >  < 
/_/\\_\\
"""

art_single_ok_str = \
"""  ___  _  _
 / _ \\| |/ )
( (_) | _ <
 \\___/|_|\\_) """

art_single_okq_str = \
"""  ___  _  _  __
 / _ \| |/ )(_ )
( (_) | _ <  //
 \___/|_|\_) O """

art_single_fail_str = \
"""  ___   _    _   _
 |  _| / \\  | | | |
 | |_|/ - \\ | | | |_
 |_|  |_|_| |_| |___| """


art_flowers_str = \
"""                            wWWWw             _            
     @@@@   @@@@         vVVVv (_ _)     _     _(_)_    .----.  
    @@()@@ @@()@@ wWWWw  (_ _)   Y     _(_)_  (_)@(_) .'o O  o'.
     @@@@   @@@@  (_ _)    Y    \|/   (_)@(_)   (_)\  '-.-..-.-'
       \     /      Y     \|/    |/    /(_)        |      ::
       |/   \|     \|/    \|/   \|   \/           \|/   \/::\//  """



def frame_text(Txt, Color, Color2):
    L = len(Txt) + 2
    txt =     ["%s%s%s|%s\n"   % (Color, (" " * L), Color2, color().Style.RESET_ALL)]
    txt.append("%s %s %s|%s\n" % (Color, Txt,       Color2, color().Style.RESET_ALL))
    txt.append("%s%s%s|%s\n"   % (Color, (" " * L), Color2, color().Style.RESET_ALL))
    return "".join(txt), len(Txt) + 3

def justify_horizonal_length(Text):
    Hf = horizontal_size(Text)
    return ["%s%s" % (line, " " * (Hf - color().plain_length(line))) for line in Text]

def __concatenate_art_strings(First, Second):
    first  = First.splitlines()
    second = Second.splitlines()

    Vf = len(first)
    Vs = len(second)
    V  = max(Vf, Vs)

    # Vertical Padding
    if   Vf < V: first.extend([""] * (V - Vf))
    elif Vs < V: second.extend([""] * (V - Vs))

    # Horizontal Padding 
    first  = justify_horizonal_length(first) 
    second = justify_horizonal_length(second) 

    return "".join(
        "%s%s\n" % (x, y) for x, y in izip(first, second)
    )

def __concatenate_space(Text, N):
    if N < 0: return Text
    txt_space = "".join("%s\n" % (" " * N) for i in xrange(Text.count("\n")))
    return __concatenate_art_strings(Text, txt_space)

def __concatenate_same(Text, Same):
    txt_space = "".join("%s\n" % Same for i in xrange(Text.count("\n")))
    return __concatenate_art_strings(Text, txt_space)

def __concatenate_padding(Text, Padding, N):
    txt = Text
    for i in range(N):
        txt = __concatenate_art_strings(txt, Padding)
    return txt

def __get_art_number(Number, IntF=False):

    if IntF: number_str = "%i" % int(Number)
    else:    number_str = "%.1f" % float(Number)

    subline_n = len(art_space_str.splitlines())

    result = [""] * subline_n
    for letter in number_str:
        for i in range(subline_n):
            begin, size = art_number_position_db[letter]
            end = begin + size - 1
            result[i] += art_numbers_str_lines[i][begin:end]

    final_result = ""
    for line in result:
        final_result += line + "\n"

    return final_result

def coverage_summary(CoverageDB):
    """CoverageDB:

            .-----------.   .------------------------------------.
            | file name |-->| .file_name                         |
            '-----------'   | .test_list_by_function_db:         |
                            |    function name --> test/coverage |
                            | .total:                            |
                            |    { .line; .branch; }             |
                            | .sub_coverage_db:                  |
                            |    .---------------.   .---------. |
                            |    | function name |-->| .line   | |
                            |    '---------------'   | .branch | |
                            |                        '---------' |
                            '------------------------------------'                     
    """
    if CoverageDB is None: return

    def print_file_str(file_name, entry):
        print "=" * common.terminal_width()
        print "DIR:  %s"  % path.relative(os.path.dirname(file_name))
        left  = "FILE: %s" % os.path.basename(file_name)
        right = coverage_str(entry.total)
        print __print_x(left, right)

    def coverage_str(C):
        # Ensure: If there is some coverage (i.e. > 0), then it shall NEVER
        #         appear as 'coverage = 0%' because of truncation.
        line_cov   = int(C.line * 100.)
        if C.line > 0   and line_cov == 0:   line_cov   = 1

        if C.branch is not None:
            branch_cov = int(C.branch * 100)
            if C.branch > 0 and branch_cov == 0: branch_cov = 1
            return " L:%3i%% B:%3i%%" % (line_cov, branch_cov) 
        else:
            return " L:%3i%% B: -:-" % line_cov

    def print_func_str(Func, C):
        left  = " * %s" % Func
        right = coverage_str(C)
        print __print_x(left, right),

    def print_test_str(Test, C):
        left  = "   %s %s" % (Test.description.file_name(), Test.choice())
        right = "[%s] %s" % (Test.result().verdict, coverage_str(C))
        print __print_x(left, right),

    print "Line/Branch Coverage Report"
    for file_name, entry in sorted(CoverageDB.iteritems(), key=itemgetter(0)):
        print_file_str(file_name, entry)
        for function_name, coverage in sorted(entry.sub_coverage_db.iteritems(), key=itemgetter(0)):
            print_func_str(function_name, coverage)
            test_list = entry.test_list_by_function_db.get(function_name) 
            if test_list is None: 
                continue
            for test, coverage in test_list:
                if test is not None: print_test_str(test, coverage)
        
    print "=" * 80

good_verdicts = ("OK", "NO DIFFERENCE", "NONE", "MADE")
bad_verdicts  = ("FAIL", "MAKE FAILED", "NO OUTPUT", "TIME_OUT")
def get_label_for_verdict(Verdict):
    global bad_verdicts
    global good_verdicts

    if   Verdict == "DONE": 
        return "%s[DONE]%s" % (color().Back.YELLOW, color().Style.RESET_ALL)
    elif Verdict == "NONE": 
        return "%s(())%s"   % (color().Back.YELLOW, color().Style.RESET_ALL)
    elif Verdict in good_verdicts:
        return "%s[%s]%s" % (color().Back.GREEN, Verdict, color().Style.RESET_ALL)
    elif Verdict in bad_verdicts: 
        return "%s[%s]%s" % (color().Back.RED, Verdict, color().Style.RESET_ALL)
    else:                   
        return "%s[%s]%s" % (color().Back.CYAN, Verdict, color().Style.RESET_ALL)
