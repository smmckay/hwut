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
import threading

class Worker(threading.Thread):
    """A 'worker' is something that can apply a strategy. It is in a specific
    directory, on a specific host and is active or not. Once, it is done, it
    reports some result to the 'principal'.
    """
    def __init__(self, WorkerId, StrategyClass):
        self.worker_id = WorkerId
        self.strategy  = StrategyClass()
        self.principal = None
        self.test_info = None
        return threading.Thread.__init__(self)
        
    def configure(self, TestInfo, principal):
        self.test_info = TestInfo
        self.principal = principal
        
    def run(self):
        if os.getcwd() != test_info.directory:
            os.cwd(test_info.directory)
        result = self.strategy.do(test_info)
        self.principal.on_work_done(worker, self.test_info, result)

class Principal:
    """A principal organizes all workers and collects their results. 
    """
    worker_list      = None
    free_worker_list = None
    worker_number    = 1
    result_list      = None

    @classmethod
    def init(cls, StrategyClass):
        global Principal.free_worker_list
        global WorkerNumber
        
        if cls.worker_list is not None:      del cls.worker_list[:]
        if cls.free_worker_list is not None: del cls.free_worker_list[:]
        
        cls.worker_list = [
            Worker(i, StrategyClass()) for i in xrange(WorkerNumber)
        ]
        cls.free_worker_list = [ worker for worker in cls.worker_list ]
        
        cls.result_list = []
    
    @classmethod
    def assign(cls, TestInfo, principal):
        if not cls.free_worker_list: 
            return False
        worker = free_worker_list.pop()
        worker.configure(TestInfo, cls)
        worker.start()
        return True
    
    @classmethod
    def on_work_done(cls, worker, TestInfo, Result):
        cls.free_worker_list.append(worker)
        cls.result_list.append((TestInfo, Result))
        
def do(TestSequence):
    for test in TestSequence:
        while 1 + 1 == 2:
            if Principal.assign(test): break
            time.sleep(0.5)
            
            