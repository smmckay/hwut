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
"""
PURPOSE: 

Determines a 'virtual time unit'. The plaform specific constant shall
allow to specify time in units that are proportional to the system's 
computational power.  The goal is to measure execution time in a unit that 
is constant across platforms--a 'virtual time'. 

Let a procedure require a time 't0' to run on a platform 'p0' and a time
't1' on a platform 'p1'. That is, the virtual time 'vt' shall be the the
same for both.
                               t0      t1
                         vt = ----- = ----- = constant.
                              f(p0)   f(p1)

The function 'f(plattform)' in the above equation is what this function 
tries to implement. Measuring the executing time of some representive
operations shall provide a basis to determine the computational power
of the system in seconds.

"""
from   time import time
from   math import tan

class ego:
    last_update_time  = None
    virtual_time_unit = None

def unit():
    """Determines a 'virtual time unit' so that a process on different 
    platforms takes approximately the same time if expressed in terms
    of this unit. 

    The system load may change during longer test executions. So every 
    now and then the virtual time unit is recalculated.
    
    RETURNS: Virtual time unit [seconds]
    """
    global ego

    current_time = time()
    if ego.__last_update_time is None or ego.__last_update_time - current_time > 10.0:
        ego.__last_update_time = current_time
        ego.__virtual_time_unit = __determine({})

    return ego.__virtual_time_unit

def __determine(db):
    """Pass the 'db' as an argument to prevent that related operations are 
    optimized away.

    RETURNS: Time to execute some operations which are considered to be 
             representive for the system's performance.
    """
    begin_t = time()
    db.update(
        (i, tan(float(i)))
        for i in range(16384)
    )
    end_t = time()
    return end_t - begin_t

