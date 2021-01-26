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
import hwut.io.messages           as io
from   hwut.auxiliary.executer.executer_system_call import ExecuterSystemCall
#from   hwut.auxiliary.executer.remote               import ExecuterRemote
import hwut.auxiliary.file_system as fs
import hwut.common                as common
import subprocess
import threading
from   numbers    import Number
import os
import signal
import tempfile
import stat
import time
from   copy       import copy
from   StringIO   import StringIO
from   exceptions import OSError, Exception

class ErrorType:
    NONE               = "NONE"
    EXECUTION          = "EXECUTION"
    TIME_OUT           = "TIME_OUT"
    OVERSIZE           = "OVERSIZE"
    KEYBOARD_INTERRUPT = "KEYBOARD_INTERRUPT"
    NO_SPACE           = "NO SPACE"
    ABORTED            = "ABORTED"

def do(CmdLine, stdout_fh = None, stderr_fh = None, EnvDb = None, 
       TimeOut_sec = None, SizeLimit_Kb = None, 
       executer_generator = ExecuterSystemCall):
    """Call a program specified in the 'CmdLine'. 

    RETURNS: True,  if execution happend in appropriate time frame.
             False, if execution hit a time out.
             ErrorType, if execution failed.

    stdout_fh, stderr_fh: Capture the standard and standard error output 
                 during program executing. 

    EnvDb:       Environment variables to be added to the current environment.

    TimeOut_sec: The maximum time that the program is allowed to take for
                 execution [second].

    SizeLimit_Kb: The maximum size that a file can occupy [kile byte].

    executer: The program that is used to execute what is described in
                   the CmdLine. 

    All arguments, except for 'CmdLine' can be omitted. The 'executer' may be
    used, to define a 'remote-procedure caller', for example. Defaultwise, 
    the executer is the operating system under which hwut is running.

    The 'executer' program must behave like 'subprocess.Popen'. In particular
    it must take the arguments

             executer(CmdLine, stdout=StdOut, stderr=StdErr, env=env)

    It must spawn the execution to a parallel thread and return an object which
    allows to control it by:

                .wait() --> wait until execution ends.
                .kill() --> stop execution totally.

    The object returned from 'executer' must be 'None' in case that the process
    call could not be initiated.
    """
    assert type(CmdLine) == list
    assert SizeLimit_Kb is None or isinstance(SizeLimit_Kb, Number)

    if stdout_fh is None or stderr_fh is None:
        devnull_fh = open(os.devnull, "wb")
        if stdout_fh is None: stdout_fh = devnull_fh
        if stderr_fh is None: stderr_fh = devnull_fh
    else:
        devnull_fh = None
    assert "w" in stdout_fh.mode 
    assert "w" in stderr_fh.mode 

    command_line = clean_command_line(CmdLine)

    error_type = watch_dogged_call(executer_generator, command_line, 
                                   TimeOut_sec, SizeLimit_Kb,
                                   StdOut=stdout_fh, StdErr=stderr_fh, 
                                   env=EnvDb)

    if devnull_fh is not None: devnull_fh.close()

    return error_type

def do_stdout(CmdLine, executer_generator=ExecuterSystemCall):
    """Execute 'CmdLine' as in '.do()', but report the standard output as 
    a string. 

    RETURNS: String containing the standard output of the command that has 
             been called.
    """
    stdout_fh = tempfile.TemporaryFile()
    do(CmdLine, stdout_fh=stdout_fh, executer_generator=executer_generator)
    stdout_fh.seek(0)
    content = stdout_fh.read()
    stdout_fh.close()
    return content

def do_stdout_and_stderr(CmdLine, executer_generator=ExecuterSystemCall):
    """Execute 'CmdLine' as in '.do()', but report the standard output as 
    a string. 

    RETURNS: String containing the standard output of the command that has 
             been called.
    """
    stdout_fh = tempfile.TemporaryFile()
    stderr_fh = tempfile.TemporaryFile()

    do(CmdLine, stdout_fh=stdout_fh, stderr_fh=stderr_fh, 
       executer_generator=executer_generator)

    stdout_fh.seek(0); out_str = stdout_fh.read(); stdout_fh.close()
    stderr_fh.seek(0); err_str = stderr_fh.read(); stderr_fh.close()

    return out_str, err_str

def watch_dogged_call(executer_generator, command_line, TimeOut_sec, SizeLimit_Kb, 
                      StdOut, StdErr, env):
    """Runs a system call, but does not wait longer than 'TimeOut_sec' [sec] and
    does not produce more output than 'SizeLimit_KB' [Kilo Byte].

    RETURNS: ErrorType 
    """
    assert executer_generator is not None

    watch_dog = WatchDog(executer_generator, TimeOut_sec, SizeLimit_Kb, 
                         StdOut, StdErr, env)

    if not watch_dog.ok_f:
        return watch_dog.error_type_on_aborted()

    try:
        error_type = watch_dog.run(command_line, StdOut, StdErr)
    except KeyboardInterrupt:
        watch_dog.terminate()
        io.on_first_keyboard_interrupt()
        # Give the user the chance to send a second Ctrl-C
        # .------------------------------------------------------------------.
        # : If a 'KeyboardInterrupt' is shot in the next 2 seconds, then the :
        # : according exception is going to fly to the caller's exception    :
        # : handler.                                                         :
        # '------------------------------------------------------------------'
        time.sleep(2)

        # : Else, simply report that 'Ctrl-C' has been pushed during test.
        return ErrorType.KEYBOARD_INTERRUPT

    except:
        watch_dog.terminate()
        io.error_on_try_to_execute(command_line)
        return watch_dog.error_type_on_aborted()

    watch_dog.terminate()
    return error_type


class WatchDog:
    def __init__(self, executer_generator, TimeOut_sec, SizeLimit_Kb, 
                 StdOut, StdErr, EnvDb):
        self.thread             = None
        self.executer           = None
        self.executer_generator = executer_generator

        self.thread_watch          = None
        self.thread_watch_channels = [ StdOut, StdErr ]

        self.error_type = ErrorType.NONE

        # Environmemt Variables: Optionally, add variables.
        if EnvDb is None:
            self.env_db = None
        else:
            self.env_db = os.environ.copy() 
            self.env_db.update(EnvDb) 

        # Time Out: Do not allow Time-Outs below 5.0 second.
        self.time_out_sec  = restrict_to_greater(TimeOut_sec, 
                                                 common.get_min_timeout_sec())

        if SizeLimit_Kb is None:
            self.size_limit_byte = common.get_output_file_max_size()
        else:
            self.size_limit_byte = SizeLimit_Kb * 1024

        assert isinstance(self.size_limit_byte, Number)

        # Refuse to operate on file systems where there is less than a certain
        # minimun of free space. This avoids the risk 
        free_space_byte = common.get_free_disk_space()
        if free_space_byte < max(common.get_min_freespace_byte(), 
                                 common.get_output_file_max_size()):
            self.error_type = ErrorType.NO_SPACE
            self.ok_f = False
        else:
            self.ok_f = True

    def run(self, CmdLine, StdOut, StdErr):
        """Initiate the call to the test program and watch it in parallel. This
        function exits if:

              -- time limit exceeded (Watching frame exits).
              -- size limit exceeded (Watching frame exits).
              -- The test program exits and none of the above happend.

        Function waits on 'termination_lock'.

        RETURNS: ErrorType -- which is ErrorType.NONE in case that execution 
                              happend peacefully.
        """
        self.error_type = ErrorType.NONE

        if self.spawn_test(CmdLine, StdOut, StdErr):
            self.thread = threading.Thread(target=self.thread_await_end)
            self.thread.start()
        else:
            pass 

        self.watch()

        return self.error_type

    def terminate(self):
        """Terminate the program call thread and the wait thread.
        """
        if   self.thread is None:          return
        elif not self.executer.is_alive(): return 

        self.executer.kill()
                
        if self.thread.is_alive():
            self.thread.join()    

    def spawn_test(self, CmdLine, StdOut, StdErr):
        """Spawn a test process. There will be a thread, that solely waits for
        the process to terminate and a thread that 'watches' its time and space
        consumption. 
        """
        try:
            self.executer = self.executer_generator(CmdLine, 
                                                    stdout=StdOut, stderr=StdErr, 
                                                    env=self.env_db)
            # May be 'self.executer = None'
        except:
            self.executer = None

        return self.executer is not None 

    def thread_await_end(self):
        """Wait for the spawned test to terminated.
        """
        # self.waiter_process_started.release()
        # As long as we wait, executer.is_alive() is True.
        self.executer.wait_for_termination()

    def watch(self):
        """Watches the test thread execution with respect to TIME and SIZE 
        limits. 

        The function exits if: 
            -- The watched process exited.
            -- The time out is exceeded   (=> .error_type = TIME_OUT)
            -- The size limit is exceeded (=> .error_type = OVERSIZE)

        The thread 'sleeps' for dynamic time distances. The delta times
        adapt to the speed of which the output size develops. The strategy
        of this adpation is implemented in 'get_t_delta()'.
        """
        if self.thread is None: return

        def get_t_delta(Size, SizeBegin, Time, TimeBegin, TimeLimit, DeltaT_prev):
            """The 'size-speed' is only considered after the process has produced
            some data. This is to avoid confusion caused by 'late starters'. Then,
            the time to watch next time is adapted according to the size limit and
            the current size-speed. The increase of t_delta is bound to a factor 
            '4'. This avoids 'smarty-pants' overestimations.
            """
            WaitMax = 0.5                 # sec
            if DeltaT_prev:           WaitMax = min(WaitMax, DeltaT_prev * 4)   
            if TimeLimit is not None: WaitMax = min(WaitMax, TimeLimit - Time)
            WaitMin = min(0.001, WaitMax) # sec

            if TimeBegin is None: return WaitMin
            t_ref = Time - TimeBegin
            if t_ref <= 0:        return WaitMin
            size_ref = Size - SizeBegin
            speed    = size_ref / t_ref
            if speed <= 0:        return WaitMin

            # Time when the application probably reaches the limit
            # Estimated time to develop remaining size.
            size_remainder = self.size_limit_byte - Size
            time_to_limit  = size_remainder / speed
            # Check on a half of the distance, whether this has happend
            t_delta        = time_to_limit / 2

            if   t_delta < WaitMin: return WaitMin
            elif t_delta > WaitMax: return WaitMax
            else:                   return t_delta

        if self.time_out_sec is None: t_limit = None 
        else:                         t_limit = time.time() + self.time_out_sec

        # Catch the slow starters: Only consider time, once that a certain minimum
        # of output has been produced. Until then, watch closely.
        t_delta    = 0
        output_min = 1024  # byte 

        t_first_sample    = None  # *_first_sample not None 
        size_first_sample = 0     # => started consideration.
        while self.executer.is_alive():
            if self.error_type == ErrorType.EXECUTION:
                break

            t    = time.time()
            size = self.get_max_output_size()
            if size > output_min and t_first_sample is None: 
                t_first_sample    = t
                size_first_sample = size

            if size > self.size_limit_byte:
                self.error_type = ErrorType.OVERSIZE
                break

            elif t_limit is not None and t >= t_limit: 
                self.error_type = ErrorType.TIME_OUT
                break

            else:
                t_delta = get_t_delta(size, size_first_sample, 
                                      t, t_first_sample, t_limit, t_delta)
                self.thread.join(t_delta)

        return

    def get_max_output_size(self):
        """RETURNS: True  -- if oversized output has been detected.
                    False -- if the output's size is still in the limits.
        """
        max_size = 0
        for channel in self.thread_watch_channels:
            if channel is None: continue
            file_name = channel.name
            if file_name == os.devnull: continue
            try:    current_size = os.path.getsize(file_name)
            except: continue
            if current_size > max_size: max_size = current_size
        return max_size

    def error_type_on_aborted(self):
        if self.error_type != ErrorType.NONE: return self.error_type
        else:                                 return ErrorType.ABORTED
        

def clean_command_line(CmdLine):
    result = [ option.strip() for option in CmdLine ]
    result = [ option for option in result if len(option) != 0 ]
    return result


def restrict_to_greater(X, Limit):
    if   X is None: return X
    elif X < Limit: return Limit
    else:           return X

