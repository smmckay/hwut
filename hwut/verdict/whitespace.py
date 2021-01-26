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
"""PURPOSE: 

This module contains functions to handle whitespace during comparison
of a nominal output (Good) and the actual output (Output).

(C) Frank-Rene Schaefer
_______________________________________________________________________________
"""
from   itertools import izip, izip_longest
import re
    
def shrink(Text):
    """-- Delete any trailing or starting whitespace. 
       -- Shrink any number of adjacent whitespace to a single space.

    RETURNS: The shrinked text.
    """
    txt = Text.strip()
    txt = txt.replace("\t", " ") 
    txt = txt.replace("\r\n", "\n") 
    # Do the replacement in two steps for speed-up
    while txt.find("        ") != -1: txt = txt.replace("        ", " ")
    while txt.find("    ")     != -1: txt = txt.replace("    ", " ")
    while txt.find("  ")       != -1: txt = txt.replace("  ", " ")
    return txt

def iterable(Text):
    """Generates an iterable over the whitespaces in 'Text'.

    This function is supposed to be used with Text objects that are
    'stripped' of bordering whitespaces!

    YIELDS: The whitespace
       
    The first element is the whitespace at the beginning of the line.
    The last element is the whitespace at the end of the line. Both
    may be of length 0.
    """
    L = len(Text)
    if L == 0: 
        return

    k = 0
    i = 0
    while 1 + 1 == 2:
        # find end of non-space
        for i in xrange(k, L):
            if Text[i].isspace(): break
        else:
            return


        # find end of space
        k = i + 1
        for k in xrange(k, L):
            if not Text[k].isspace(): break
        else:
            yield Text[i:]
            return

        yield Text[i:k]
        
def at_begin(Text):
    """RETURNS: The whitespace at the beginning of Text.
    """
    L = len(Text)
    i = 0
    for i in xrange(L):
        if not Text[i].isspace(): break
    return Text[:i]

def at_end(Text):
    """RETURNS: The whitespace at the end of Text.
    """
    L = len(Text)
    k = L - 1
    for k in xrange(L - 1, -1, -1):
        if not Text[k].isspace(): break
    return Text[k+1:]
    
def fit(Follower, RoleModel):
    """Adapt the whitespace in Follower, so that it fits the whitespace in 
    the RoleModel. Thus, a 'diff' programm will not complain about differing
    whitespaces.
    """
    rm_end   = at_end(RoleModel)

    # Adapting the 'beginning whitespace' caused confusion. It keeps diff-tools
    # sometimes from matching the correct lines.
    fl_begin = at_begin(Follower)

    # Delete bordering whitespace in RoleModel and Follower
    role_model = RoleModel.strip()
    if Follower.find("\t") != -1: follower = Follower.replace("\t", " ")
    else:                         follower = Follower
    follower = follower.strip()

    word_list = follower.split()
    if len(word_list) == 0:
        return fl_begin + rm_end

    def get_space(rm_space, f_space, word):
        # Never paste the 'inside' whitespace after the last word.
        if rm_space is not None and word is not None: return rm_space
        elif f_space is not None:                     return f_space
        else:                                         return None

    
    # Begin whitespace
    result = [ fl_begin ]
    i      = 0
    for rm_space, f_space, word in izip_longest(iterable(role_model), 
                                                iterable(follower), 
                                                word_list[:-1], 
                                                fillvalue=None):

        if word is None: break
        else:            result.append(word)

        space = get_space(rm_space, f_space, word)
        if space is None: pass 
        else:             result.append(space)


    # Ending whitespace
    result.append(word_list[-1])
    result.append(rm_end)

    return "".join(result)

