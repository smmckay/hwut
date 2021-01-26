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

This file generates test cases for MC/DC coverage, not code. Input is a
decision consisting of a tree of logically combined conditions. Output is a
sequence of boolean settings for all conditions involved. The setting of the
conditions implement MC/DC coverage, if possible.

EXAMPLE:

                if( A == 0 || (B == 1 && C == 2) ) ...
                    '----'     '----'    '----'
                      Ca         Cb        Cc

contains the three conditions 'A == 0', 'B == 1', and 'C == 2'. The logical
operators '||' for 'or' and '&&' for 'and' combine the conditions into a
decision. Replacing the conditions by names 'Ca', 'Cb', and 'Cc' and organizing
the decision in a tree gives:

                         Ca      Cb       Cc
                          |       |       |
                          |       '-(and)-'
                          |           |  
                          '---(or)----'
            
       .--------------------------------------------------------.
       | MC/DC coverage is achieved, if every condition appears |
       | in a scenario where its outcome is decisive.           |
       '--------------------------------------------------------'

For example, if Cb and Cc == True, then Ca does not influence the outcome of
the decision. It is 'True' independently of Ca. A test sequence that contains a
setting where 'Cb and Cc == False', satisfies the need to have a scenario where
Ca is decisive. Let us call such a scenario Cas, and respectively Cbs and Ccs

        Cas = { (Cb, Cc) where Cb and Cc == True }
        Cbs = { (Ca=False, Cc=True) }
        Ccs = { (Ca=False, Cb=True) }

Taking one of the settings of Cas and adding the setting 'Ca=True' and 'Ca=False'
therefore checks on the decisiveness of Ca. The same must be done for Cb and Cc.

        Ca = True;  Cb = True;  Cc = True;   ---- decisiveness of Ca
        Ca = False; Cb = True;  Cc = True;   -'
        Ca = False; Cb = True;  Cc = True;   ---- decisiveness of Cb
        Ca = False; Cb = False; Cc = False;  -'
        Ca = False; Cb = True;  Cc = True;   ---- decisiveness of Cc
        Ca = False; Cb = True;  Cc = False;  -'

Some of the lines above appear twice, so the set of all settings achieving MC/DC
coverage is

        Ca = True;  Cb = True;  Cc = True;  
        Ca = False; Cb = True;  Cc = True; 
        Ca = False; Cb = False; Cc = False; 
        Ca = False; Cb = True;  Cc = False; 

The correspondent settings can then be iterated through, the same way usual 'hwut'
iterators are applied. 
"""

def consistency(ConditionSet):
    """RETURNS: True  -- if the conditions are consistent. 
                False -- if not.

    If a condition in the set of pairs (condition, verdict) appears with two
    different verdicts, then the number of conditions is different from the 
    conditions in the ConditionSet. 
    """
    db = dict(
        condition for condition, verdict in ConditionSet
    )
    return len(db) == len(ConditionSet)

def OneOrMoreIsFalse(N):
    """YIELDS: List of N boolean values. 

    This generator iterates over all settings of N boolean values where there
    is at least one value is False.
    """
    array = [True] * N
    for false_i in xrange(N):
        false_i = False
        yield Remaining(array, N-1, false_i)

def OneOrMoreIsTrue(N):
    """YIELDS: List of N boolean values. 

    This generator iterates over all settings of N boolean values where there
    is at least one value is True.
    """
    array = [True] * N
    for true_i in xrange(N):
        true_i = True
        yield Remaining(array, N-1, true_i)

def Remaining(array, N, Index):
    """YIELDS: A copy of 'array' (having N boolean values)

    The value at position 'Index' is always left alone. All other values
    iterate through possible combinations of boolean settings.
    """
    for setting in BooleanAll(N-1):
        for i in xrange(Index):     array[i] = setting[i]
        for i in xrange(Index+1,N): array[i] = setting[i-1]
        yield copy(array)
        
class Node:
    """A abstract node in the tree of conditions.

    INTERFACE:
 
    * 'require(Verdict)' 

    returning an iterable over pairs (condition, verdict) which implements 
    the given Verdict.
    """
    def require(self, Verdict): assert False

class NodeOp(Node):
    """An  abstract operation node in the tree of conditions. It has multiple 
    sub nodes on which it depends.

    INTERFACE:
 
    * 'require(Verdict)' (from Node)
    * '_require_true()'
    * '_require_false()'

    Derived classes must implement: '_require_true()' and '_require_false()' 
    Each of which must return an iterable over pairs (condition, verdict) 
    which implements the corresponding verdict.
    """
    def __init__(self, SubNodeList): 
        self.sub_node_list = SubNodeList

    def require(self, Verdict):          
        if Verdict: list_of_iterables = self._require_true()
        else:       list_of_iterables = self._require_false()

        setting_list = flatten(list_of_iterables)
        return set(s for s in setting_list if consistency(s))

    def _get_settings(self, Generator):
        """The 'Generator' produces verdict lists. Verdict lists produce
        iterables over possible settings to achieve them. The 'yield' of
        this the list of possible conditions.

        YIELDS: Condition setting.
        """
        for verdict_list in Generator(len(self.sub_node_list)):
            for setting in self._require_nodes(verdict_list):
                yield setting

    def _require_nodes(self, VerdictList):
        """Requires settings from nodes for specific verdicts. A sub node 
        number 'i' must produce the verdict 'VerdictList[i]'.

        All results are collected in a 'flattened' list.

        RETURNS: Iterable over condition settings.
        """
        return flatten(
            node.require(verdict) 
            for node, verdict in izip(self.sub_node_list, verdict_list)
        )
        
class NodeLeaf(Node):
    """Leaf node: a condition.
    """
    def __init__(self, ConditionId): self.condition_id = ConditionId
    def require(self, Verdict):      return set([self.condition_id, Verdict])

class NodeNot(Node):
    """Negate a sub node. It is true if and only if the sub node is False.
    """
    def __init__(self, SubNode): self.sub_node = SubNode
    def require(self, Verdict):  return self.sub_node.require(not Verdict)

class NodeOpAnd(Node):
    """Combine 'N' sub nodes with an 'AND' operation. That is, it is true
    if and only if all nodes are true. 
    """
    def __init__(self, SubNodeList): NodeOp.__init__(SubNodeList)
    def _require_true(self):
        return (node._require_true() for node in self.sub_node_list)
    def _require_false(self):
        return self._get_settings(OneOrMoreIsFalse)   
        
class NodeOpOr(Node):
    """Combine 'N' sub nodes with an 'OR' operation. That is, it is true
    if and only if all nodes are false. 
    """
    def __init__(self, SubNodeList): NodeOp.__init__(SubNodeList)
    def _require_true(self):
        return self._get_settings(OneOrMoreIsTrue)   
    def _require_false(self):
        return (node._require_false() for node in self.sub_node_list)
        
