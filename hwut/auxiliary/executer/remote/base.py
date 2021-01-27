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
"""
       Sender                 Receiver                           Remote Target
         |                       |                                     |
         |                       |   establish connection              |
         O------------------------------------------------------------>|
         |                       O------------------------------------>|
         |                       |                                     |
         |               .----------------.                            |
         |               | Wait for:      |                            |
         |               | <<hwut-begin>> |                            |
         |               | + magic        |                            |
         |               '----------------'                            |
         |                       |                                     |
         O-------------( <<hwut-begin>> magic )----------------------->|
         |                       |<--( <<hwut-begin>> magic )----------O
         |                       |                                     |
         |               .----------------.                            |
         |               | Receive Test   |                            |
         |               | Output         |                            |
         |               '----------------'                            |
         |                       |<----------( Content )---------------O
         |                       |<----------( Content )---------------O
         |                       |          ...                        |
         |                       |<----------( Content )---------------O
         |                       |                                     |
   .-[ OPTIONAL ]------------------------------------------------------------.
   |     |                       |                                     |     |
   |     O-------------( <<hwut-end>> magic )------------------------->|     |
   |     |                       |                                     |     |
   '-------------------------------------------------------------------------'
         |                       |                                     |
         |                       |<----( <<hwut-end>> magic )----------O
         |                       |                                     |
      (STOP)                  (STOP)                        (STOP)
      
magic = 6 letter/digit string which is determined randomly at run-time.  It
serves as an identifier, to make sure that the response belongs to the request.

(C) Frank-Rene Schaefer
"""
import hwut.io.messages        as     io
# from   hwut.auxiliary.executer.core import Executer

import os
import sys
import threading 

# Commands to ask for remote applications
HWUT_REMOTE_SETTING_QUERY_APPLICATION_LIST      = "$HWUT:GET_APPS$"
HWUT_REMOTE_SETTING_APPLICATION_LIST            = "$HWUT:APPS$"
# Commands for the test managing process
HWUT_REMOTE_SETTING_EXECUTION_STOP              = "$HWUT:KILL$"
HWUT_REMOTE_SETTING_EXECUTION_STOP_ACKNOWLEDGED = "$HWUT:KILLED$"
# Commands for test run control
HWUT_REMOTE_SETTING_TEST_STOP                   = "$HWUT:STOP$"
HWUT_REMOTE_SETTING_TEST_STOP_ACKNOWLEDGED      = "$HWUT:STOPPED$"
HWUT_REMOTE_SETTING_TEST_BEGIN                  = "$HWUT:BEGIN$"
HWUT_REMOTE_SETTING_TEST_UNKNOWN                = "$HWUT:?$"

HWUT_REMOTE_SETTING_TEST_STOP_ACKNOWLEDGED_LENGTH = len(HWUT_REMOTE_SETTING_TEST_STOP_ACKNOWLEDGED)

class RemoteConfiguration:
    def __init__(self, ConnectionId, ExecuterClass):
        self.id             = ConnectionId
        self.executer_class = ExecuterClass


class ExecuterRemote: # (Executer):
    """Base class for objects that act as 'ExecutionUnit'-s for remote 
    execution. The main function of this class is the function call operator
    '__call__'. It provided an interface similar to 'subprocess.Popen'. 

    Then the function call operator is called, it returns a RemoteThread
    object, or 'None' if the remote process execution cannot be started. 

    The RemoteThread object has two functions which are required by the caller:
    '.wait()' which waits for the execution to terminate and '.kill()' which
    initiates a forced termination of the remote execution.

    Particular protocols are implemented in derived classes as well as their
    receivers and senders.
    """
    def __init__(self, CmdLine, stdout, stderr, env=None):
        """
        CmdLine is None:     Query for application list.
        CmdLine is not None: Run remote application with 'CmdLine'.
        
        The call to the remote executor must comply the the signature and
        behavior of an 'ExecutionUnit' as described in the documentation of 
        function 

                        hwut.auxiliary.executer.core.do()

        That is, it must spawn a thread and provide a handle to something 
        that implements '.wait()' and '.kill()'.

        The 'env' is currently only there for conformity.


        """
        # ONLY spawn thread, AFTER object has been setup!
        self.abort_f = False

        if CmdLine is not None:
            if not CmdLine:         return None # Cannot start
            elif len(CmdLine) == 1: self.app = CmdLine[0]; self.choice = ""
            elif len(CmdLine) == 2: self.app, self.choice = CmdLine[0:2]
            self.stdout  = stdout
            self.stderr  = stderr
            self.process = threading.Thread(target=self.receive)
        else:
            self.result_application_list = None
            self.process = threading.Thread(target=self.query_application_list)

        self.process.start()

    def receive(self):
        """Execute the application 'self.app' with 'self.choice' remotely. 
        Writes received contents to the standard output.
        """
        def on_content(Text):
            self.stdout.write(Text)

        if not self.__interact("%s %s" % (self.app, self.choice), on_content): 
            return 

        self.stdout.flush()

    def query_application_list(self):
        """Request the list of applications from remote site. The received 
        data is interpreted as a list of application names with ';' as a 
        delimiter.
        """

        response_txt = []
        def on_content(Text):
            response_txt.append(Text)

        if not self.__interact(HWUT_REMOTE_SETTING_QUERY_APPLICATION_LIST, on_content):
            return 

        response_str = "".join(response_txt)

        application_list             = [ x.strip() for x in response_str.split(";") ]
        self.result_application_list = [ x for x in application_list if x ]
    
    def __interact(self, SendCmd, OnContent):
        """Interact with the remote site. Send 'SendCmd' and call 'OnContent' 
        each time a response is received. As soon as the token 
          
                      HWUT_REMOTE_SETTING_TEST_STOP_ACKNOWLEDGED

        is received, the interaction terminates.
        """
        if not self.configuration.open(): 
            print "Error: HWUT cannot remote connect with configuration '%s'" % self.configuration.id
            return False

        elif not self.configuration.send(SendCmd):
            print "Error: HWUT remote connection via '%s' cannot be established." % self.configuration.id
            print "Error: Tried to send '%s %s'" % SendCmd
            return False

        chunk          = self.configuration.receive()
        previous_chunk = self.detect_begin(chunk)
        if previous_chunk is None: return False

        previous_chunk_end_i = None
        while not self.abort_f:
            chunk                 = self.configuration.receive()
            previous_chunk_end_i, \
            chunk                 = self.detect_termination_token(chunk, 
                                                                  previous_chunk)
            if previous_chunk_end_i is not None: 
                previous_chunk = previous_chunk[:previous_chunk_end_i]

            if previous_chunk: 
                OnContent(previous_chunk)

            if previous_chunk_end_i is not None: 
                OnContent(chunk)
                break

            previous_chunk = chunk

        return True

    def is_ok(self):
        return self.configuration.is_ok()

    def kill(self):
        self.abort_f = True

    def wait_for_termination(self):
        while self.process.is_alive():
            pass

    def detect_termination_token(self, Chunk, PreviousChunk):
        """RETURNS: [0] verdict 
                        1 -- if the termination token has been detected
                        0 -- if the current chunk and the end of the last
                             chunk does not match the termination token. 
                    [1] chunk to be flushed to stdout
        """
        T  = HWUT_REMOTE_SETTING_TEST_STOP_ACKNOWLEDGED
        TL = HWUT_REMOTE_SETTING_TEST_STOP_ACKNOWLEDGED_LENGTH
        L  = len(Chunk)
        LP = len(PreviousChunk)
        if L >= TL and Chunk.endswith(T):         return LP, Chunk[:-TL]

        begin_i = TL - L
        if Chunk != T[begin_i:]:                  return None, Chunk
        elif PreviousChunk.endswith(T[:begin_i]): return LP - begin_i, ""
        else:                                     return None, Chunk

    def detect_begin(self, Chunk):
        if Chunk.startswith(HWUT_REMOTE_SETTING_TEST_BEGIN): 
            return Chunk[len(HWUT_REMOTE_SETTING_TEST_BEGIN):]
        elif Chunk.startswith(HWUT_REMOTE_SETTING_TEST_UNKNOWN):
            print "Error: Remote agent did not recognize application choice pair."
        else:
            print "Error: Initiating token has not been received from remote agent."
        return None

    def derived_initiate_run(self, ApplicationName, Choice):
        assert False

    def derived_receive(self, ApplicationName, Choice):
        assert False

    def derived_close(self):
        assert False


def get_remote_application_list(ConfigurationDb):
    """Connect through all configurations mentioned in 'ConfigurationDb'. Query
    the remote site for all test applications that can be run. 

    RETURNS: list-of( pairs-of(configuration-id, application-name) )
    """
    
    if ConfigurationDb is None:
        return []

    result = []
    for config in ConfigurationDb.itervalues():

        executer = config.executer_class.for_QueryApplicationList(config)
        if not executer.is_ok(): continue

        io.on_query_remote_application_list(config.id)

        executer.wait_for_termination()

        if executer.result_application_list is None:
            app_n = 0
        else:
            app_n = len(executer.result_application_list)
            result.extend((config.id, app) for app in executer.result_application_list)

        io.on_query_remote_application_list_end(config.id, app_n)

    return result
