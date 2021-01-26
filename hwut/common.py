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
HWUT_VERSION = '0.27.3' 

import os
import ctypes
import sys
import re
import subprocess

import hwut.external.colorama.colorama as colorama_color

if sys.version_info[0] < 2 or \
   (sys.version_info[0] == 2 and sys.version_info[1] < 7):
    print "Error: Hwut requires Python Version 2.7.0 or higher, but lesser than 3.0.\n"
    print "Error: Currently installed is Version %i.%i.%i.\n" % \
          (sys.version_info[0], sys.version_info[1], sys.version_info[2])
    sys.exit(-1)

def is_posix():
    try:
        import posix
        return True
    except ImportError:
        return False


try:
    # The following only works under Windows:
    # (Use the existence of 'win_kernel' as a signal for living under Windows.)
    if "windll" in dir(ctypes):
        win_kernel = ctypes.windll.kernel32
    else:
        win_kernel = None
except ImportError:
    win_kernel = None

def is_windows():
    global win_kernel
    return win_kernel is not None

def get_environment_variable(Name, Default=None):
    """RETURNS: Value of the environment converted to the type of 'Default'.

    If the given environment variable is not defined, then 'Default' is 
    returned.
    """
    try:    
        value_str = os.environ[Name]
    except: 
        if Default is not None: return Default
        print "Error: %s environment variable has not been defined." % Name
        sys.exit(-1)

    if   isinstance(Default, float):          return float(value_str)
    elif isinstance(Default, (int, long)):    return long(value_str)
    else:                                     return value_str

TEST_DIR_NAME    = get_environment_variable("HWUT_TEST_DIR_NAME", "TEST")
HWUT_PATH        = get_environment_variable("HWUT_PATH")
MAX_CPU_NUMBER   = get_environment_variable("HWUT_MAX_CPU_NUMBER", 1)
MAKE_APPLICATION = get_environment_variable("HWUT_MAKE_APP", "make")
GCOV_APPLICATION = get_environment_variable("HWUT_GCOV_APP", "gcov")

HWUT_HISTORY_FILE        = "ADM/history.xml"
HWUT_DATABASE_FILE       = "ADM/cache.fly"
HWUT_MAKE_LOG_FILE       = "ADM/make-output.txt"
HWUT_MAKE_CLEAN_LOG_FILE = "ADM/make-clean-output.txt"
HWUT_INFO_FILE_NAME      = "hwut-info.dat"
HWUT_FILE_MAKEFILE_FLY   = "hwut-make.fly"

HWUT_FILE_STEM_CRASH_ON_CALL  = "hwut-crash-on-call"

def __safe_path(Path):
    tmp = Path
    tmp = os.path.normpath(tmp)
    if is_windows() and tmp.find(" ") != -1 and tmp != "" and tmp[0] != '"':
        tmp = '"' + tmp + '"'
    return tmp

def get_min_freespace_byte():
    default = 2 * 1024 * 1024 # 2 MB
    return get_environment_variable("HWUT_MIN_DISK_FREESPACE_BYTE", default)

def get_min_timeout_sec():
    default = 20.0             # Do not detect time-outs lower than 20 sec
    result = get_environment_variable("HWUT_DEFAULT_TIMEOUT_MIN_SEC", default)
    return result

def get_output_file_max_size():
    default = 1024 * 1024     # 1 MB
    return get_environment_variable("HWUT_OUTPUT_FILE_MAX_SIZE", default)

def get_diff_display_application():
    if is_windows(): default = None
    else:            default = "vimdiff"
    return __safe_path(get_environment_variable("HWUT_DIFF_APP", default))

def get_lcov_application():
    if is_windows(): default = None
    else:            default = "lcov"
    return __get_interpreter_specification("HWUT_LCOV_APP", default)

def get_genhtml_application():
    if is_windows(): default = None
    else:            default = "genhtml"
    return __get_interpreter_specification("HWUT_GENHTML_APP", default)

def get_ctags_application():
    if is_windows(): default = "--"
    else:            default = "ctags"
    result = __get_interpreter_specification("HWUT_CTAGS_APP", default)
    if result == ["--"]: return None
    else:                return result

__time_out_detection_f = [ True ]
def time_out_detection_f():
    global __time_out_detection_f
    return __time_out_detection_f[0]

def time_out_detection_disable():
    global __time_out_detection_f
    __time_out_detection_f[0] = False

def __get_interpreter_specification(EnvVariable, Default):
    app_name = __safe_path(get_environment_variable(EnvVariable, Default))
    app_name = app_name.strip()

    interpreter_list = ("perl", "python", "bash")
    for interpreter  in interpreter_list:
        if app_name.find(interpreter) == 0: 
            return [ interpreter, app_name[len(interpreter):].strip() ]
        if app_name.find(interpreter) == 1 and app_name[0] == '"': 
            return [ interpreter, app_name[len(interpreter)+1:-1].strip() ]
    return [ app_name ]

history = None  # to be initialized in hwut-exe.py

__interface = None

def get_default_terminal_width():
    width, heigth = _get_terminal_size()
    return get_environment_variable("HWUT_TERMINAL_WIDTH", width)

def interface():
    global __interface
    return __interface

def set_interface(Value):
    global __interface
    assert Value in ["CONSOLE", "GUI"]
    assert __interface is None, \
           "Error: interface was previously set to %s. Now, to %s" % (repr(__interface), repr(Value))
    __interface = Value

def exit(Value=1):
    global __interface
    if interface() == "CONSOLE": sys.exit(Value)
    else:                        return Value


def split_file_name(ApplicationName):
    if ApplicationName is None:
        return None, None

    directory, application = os.path.split(ApplicationName)

    if application == TEST_DIR_NAME: 
        directory, application = os.path.split(ApplicationName + os.path.sep)

    directory = os.path.normpath(directory)
    return directory, application

class Something:
    pass

# Color Control:
#
# If '--no-color' is passed on the command line, then all coloring comands are
# disabled, i.e. replaced by an empty string.
__color = colorama_color # 'common.color' is referred to as coloring module.
def set_color(Color):
    global __color 
    __color = Color

def color():
    global __color
    return __color

no_color = Something()
no_color.Fore = Something()
no_color.Fore.YELLOW  = ""
no_color.Fore.BLACK   = ""
no_color.Fore.WHITE   = ""
no_color.Fore.MAGENTA = ""
no_color.Fore.GREEN   = ""
no_color.Fore.RED     = ""
no_color.Fore.CYAN    = ""
no_color.Back = Something()
no_color.Back.YELLOW  = ""
no_color.Back.BLACK   = ""
no_color.Back.WHITE   = ""
no_color.Back.MAGENTA = ""
no_color.Back.GREEN   = ""
no_color.Back.RED     = ""
no_color.Back.CYAN    = ""
no_color.Style = Something()
no_color.Style.RESET_ALL = ""
no_color.plain_length = lambda Text: len(Text)

class Setup:
    option_set_version = ("-v", "--version")
    option_set_help    = ("-h", "--help", "-?", "/?", "/h", "/help")

    def __init__(self, cl, FirstArg, SecondArg):
        self.cl = cl
        self.first_argument   = FirstArg
        self.second_argument  = SecondArg

        self.known_option_set = set()
        self.known_option_set.update(Setup.option_set_version)
        self.known_option_set.update(Setup.option_set_help)
        
        self.test_directory_pattern = ""
        self.coverage_support_set   = set()
        self.test_directory,       \
        self.test_application_name = split_file_name(FirstArg)
        self.choice                = SecondArg

        if self.search("--no-timeout"):
            time_out_detection_disable()

        test_reference_table_file = self.follow("", "--in")
        table = []
        if test_reference_table_file:
            table = output_csv.read_csv(test_reference_table_file)
        self.test_reference_table = table
        self.test_reference_table_file_out = self.follow("", "--out")


        global no_color
        self.no_color_f = self.search("--no-color")
        if self.no_color_f: set_color(no_color)
        else:               color().init()

        self.failed_only_f      = self.search("--fail")
        self.make_failed_only_f = self.search("--make-failed")
        self.good_only_f        = self.search("--ok")
        self.compression_f      = self.search("--compress")
        self.execution_f        = not self.search("--no-exec", "--ne")

        self.output_file_stem   = self.follow("", "-o", "--output-file-stem")

        # TAP protocol output
        self.output_tap_subtest_f = self.search("--tap-subtest")
        if self.output_tap_subtest_f: self.output_tap_f = True
        else:                         self.output_tap_f = self.search("--tap")

        if self.search("--lcov"): 
            self.coverage_support_set.add("lcov")
            try:    
                subprocess.call(get_lcov_application() + ["-v"])
            except: 
                print "Error: Cannot call '%s' to invoque lcov." % get_lcov_application()
                sys.exit()

        self.coverage_trace_tests_f = self.search("--cts", "--coverage-trace-test")

        if   self.search("--no-grant"): self.grant = "NONE"  # "no grant" overrides "grant" for safety
        elif self.search("--grant"):    self.grant = "ALL"
        else:                           self.grant = "INTERACTIVE"

        if self.search("--make"): self.make_target = get_next_nominus(cl)
        else:                     self.make_target = ""

        self.diff_app_name_by_command_line = self.follow("", "--diff-application", "--dapp")

        set_terminal_width(self.follow(get_default_terminal_width(), "-w", "--terminal-width"))

        self.user_compile_args      = self.followers_until("--cc-args", "--")
        self.user_link_args         = self.followers_until("--ld-args", "--")
        self.user_args              = self.followers_until("--args",    "--")
        self.hint_root_dir_list            = self.nominus_followers("--root")

        self.hint_exclude_pattern_list     = self.nominus_followers("--exclude")
        self.hint_exclude_dir_pattern_list = self.nominus_followers("--exclude-dir")
        self.hint_source_list              = self.nominus_followers("--sources")
        self.hint_root_dir_list_source     = self.nominus_followers("--root-sources")
        self.hint_root_dir_list_include    = self.nominus_followers("--root-include")
        self.hint_root_dir_list_libraries  = self.nominus_followers("--root-libs")
        self.hint_root_dir_list_objects    = self.nominus_followers("--root-objects")
        self.output_makefile               = self.follow("Makefile", "--makefile")

        language = self.follow("c", "--language", "--lang")
        if language != "c": 
            print "Error: Language '%s' not supported for stubbing."
            sys.exit(-1)

    def followers_until(self, Option, Delimiter):
        """RETURNS: List of arguments from 'Option' to 'Delimiter'
        """
        if not self.search(Option): 
            return []

        result = []
        while 1 + 1 == 2:
            arg = self.cl.next("")
            if not arg: 
                print "Error: '%s' not terminated with '%s'" % (Option, Delimiter)
                break
            self.known_option_set.add(arg)
            if arg == Delimiter: break
            result.append(arg)

        return result

    def nominus_followers(self, Option):
        self.known_option_set.add(Option)
        return self.cl.nominus_followers(Option)

    def follow(self, Default, *Options):
        self.known_option_set.update(Options)
        if   len(Options) == 1: return self.cl.follow(Default, Options[0])
        elif len(Options) == 2: return self.cl.follow(Default, Options[0], Options[1])
        elif len(Options) == 3: return self.cl.follow(Default, Options[0], Options[1], Options[2])

    def search(self, *Options):
        self.known_option_set.update(Options)
        if   len(Options) == 1: return self.cl.search(Options[0])
        elif len(Options) == 2: return self.cl.search(Options[0], Options[1])
        elif len(Options) == 3: return self.cl.search(Options[0], Options[1], Options[2])

    def diff_display_application(self):
        if self.diff_app_name_by_command_line: 
            return self.diff_app_name_by_command_line
        return get_diff_display_application()

    def check_unrecognized_options(self):
        ufos = self.cl.unidentified_options(self.known_option_set)
        if not ufos: return

        print "Error: unidentified command line option(s):"
        print ufos
        print 
        print "Please, call this application with '--help' to get an overview over the"
        print "existing options."
        sys.exit(-1)
        
def get_next_nominus(cl):
    assert cl.__class__.__name__ == "GetPot"

    cl.search_failed_f = False  # otherwise the 'next()' command wont work
    #                           # in case no flag was tested before
    txt = cl.next("")
    if len(txt) > 1 and txt[0] == "-": return ""
    else:                              return txt

# The remote target is to be set and unset on every entry and exit of a 
# TEST directory. If it is not 'None', then tests are executed remotely.
remote_executer = None

def change_directory(Dir):
    backup_dir = os.getcwd()

    norm_dir = os.path.normpath(Dir)
    if norm_dir == "": 
        return backup_dir

    try:
        os.chdir(norm_dir)  # is relative to 'home directory', i.e.
    except:
        print "Error: Directory '%s'" % os.getcwd()
        print "Error: Failed to change to directory: '%s'" % norm_dir
        sys.exit(0)

    return backup_dir

def get_free_disk_space():
    Directory = os.getcwd()
    if is_posix():
        stat = os.statvfs(Directory)
        return stat.f_bavail * stat.f_frsize
    elif is_windows():
        d0       = ctypes.byref(ctypes.c_ulonglong())
        d1       = ctypes.byref(ctypes.c_ulonglong())
        free     = ctypes.c_ulonglong()
        free_ref = ctypes.byref(free)
        if isinstance(Directory, unicode):
            if not win_kernel.GetDiskFreeSpaceExW(Directory, d0, d1, free_ref):
                print "Windows: Cannot determine Disk Space"
                sys.exit(-1)
        else:
            if not win_kernel.GetDiskFreeSpaceExA(Directory, d0, d1, free_ref):
                print "Windows: Cannot determine Disk Space"
                sys.exit(-1)
        return free.value
    else:
        print "Unknown Operating System"
        sys.exit(-1)

def _get_terminal_size():
    # Learned from: 
    #
    # http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
    #
    if is_windows():
        width_height = _get_terminal_size_windows()
        if width_height is not None: return width_height
        width_height = _get_terminal_size_tput()
        if width_height is not None: return width_height

    if is_posix():
        width_height = _get_terminal_size_posix()
        if width_height is not None: return width_height
       
    return (80, 25) # Default: width = 80; height = 25;

def _get_terminal_size_windows():
    res=None
    try:
        from ctypes import windll

        STD_IN_HANDLE     = -10
        STD_OUTPUT_HANDLE = -11
        STD_ERR_HANDLE    = -12

        h    = windll.kernel32.GetStdHandle(STD_ERR_HANDLE) 
        csbi = ctypes.create_string_buffer(22)
        res  = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
    except:
        return None
    if res:
        import struct

        (bufx, bufy, curx, cury, wattr,
         left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)

        sizex = right - left + 1
        sizey = bottom - top + 1
        return sizex, sizey
    else:
        return None

def _get_terminal_size_tput():
    try:
       proc=subprocess.Popen(["tput", "cols"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
       output=proc.communicate(input=None)
       cols=int(output[0])
       proc=subprocess.Popen(["tput", "lines"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
       output=proc.communicate(input=None)
       rows=int(output[0])
       return (cols,rows)
    except:
       return None

def _get_terminal_size_posix():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,'1234'))
        except:
            return None
        return cr

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (env['LINES'], env['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])

def all_isinstance(List, Type):
    for x in List: 
        if not isinstance(x, Type): return False
    return True


__verbosity_f = [False]

def set_verbosity_f(Value):
    assert type(Value) == bool
    global __verbosity_f
    __verbosity_f[0] = Value

def verbosity_f():
    global __verbosity_f
    return __verbosity_f[0]

__terminal_width = [ get_default_terminal_width() ]
def terminal_width():
    global __terminal_width
    return __terminal_width[0]

def set_terminal_width(Value):
    global __terminal_width
    __terminal_width[0] = Value

__home_directory = [""]  # updated by 'core.do_directory_tree()'
def set_home_directory(Value):
    global __home_directory
    __home_directory[0] = Value

def home_directory():
    global __home_directory
    return __home_directory[0]

def re_compile(PatternStr):
    """Compiles a regular expression.
    
    RETURNS: match object -- if compilation succeeded.
             None         -- if there was an error.
    """
    try: 
        return re.compile(PatternStr)
    except:
        print "Error: regular expression '%s' compilation failed." % PatternStr
        return None
    
