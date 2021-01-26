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
#! /usr/bin/env python
#
# 'whitespace.fit' makes one line look similar to another one by adapting
# the whitespaces. 
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________
import os
import sys

sys.path.insert(0, os.environ["HWUT_PATH"])

import hwut.verdict.whitespace as whitespace


if "--hwut-info" in sys.argv:
    print "Whitespace: Fit;"
    print "CHOICES: single, two, three;"
    sys.exit()

def test(X, Y):
    print "_" * 80    
    print "X: [%s]" % X.replace("\t", "\\t")
    print "Y: [%s]" % Y.replace("\t", "\\t")
    print 
    Y_follows_X = whitespace.fit(Y, X)
    print "Y follows X: [%s]" % Y_follows_X.replace("\t", "\\t")
    X_follows_Y = whitespace.fit(X, Y)
    print "X follows Y: [%s]" % X_follows_Y.replace("\t", "\\t")
    return Y_follows_X, X_follows_Y

def astest(X, Y):
    """Run tests where the lines are actually the same, except for
       their whitespaces. In that cases the fitted line must be the 
       same as the role model.
    """
    y_follows_x, x_follows_y = test(X, Y)
    x_adapted = X.replace("+", "@")
    y_adapted = Y.replace("@", "+")

    #print "# y_adapted: %s; x_follows_y: %s;" % (y_adapted, x_follows_y)
    #assert y_adapted == x_follows_y
    #print "# x_adapted: %s; y_follows_x: %s;" % (x_adapted, y_follows_x)
    #assert x_adapted == y_follows_x

if "single" in sys.argv:
    test("", "")
    test("", "@")
    test("", " @")
    test("", "@ ")
    test("", " @ ")
    astest("+", "@")
    astest("+", " @")
    astest("+", "@ ")
    astest("+", " @ ")
    astest(" +", " @")
    astest(" +", "@ ")
    astest(" +", " @ ")
    astest("+ ", " @")
    astest("+ ", " @ ")
    astest(" + ", " @ ")
    # DONE ALREADY in equivalents:
    # astest(" +", "@")    
    # astest("+ ", "@")    
    # astest("+ ", "@ ")   
    # astest(" + ", "@")   
    # astest(" + ", " @")  
    # astest(" + ", "@ ")  

elif "two" in sys.argv:
    test("", "")
    test("", "@ @")
    test("", " @ @")
    test("", "@ @ ")
    test("", " @ @ ")
    test("+", "@ @")
    test("+", " @ @")
    test("+", "@ @ ")
    test("+", " @ @ ")
    test(" +", " @ @")
    test(" +", "@ @ ")
    test(" +", " @ @ ")
    test("+ ", " @ @")
    test("+ ", " @ @ ")
    test(" + ", " @ @ ")
    
elif "three" in sys.argv:
    test("",      "@ @ @")
    test("",      " @ @ @ ")
    test("",      "@ @ @ ")
    test("",      " @ @ @")

    test("+",     "@ @ @")
    test(" +",    " @ @ @ ")
    test("+ ",    "@ @ @ ")
    test(" + ",   " @ @ @")

    test("+ +",     "@ @ @")
    test(" + +",    " @ @ @ ")
    test("+ + ",    "@ @ @ ")
    test(" + + ",   " @ @ @")

    test("+ + +",     "@ @ @")
    test(" + + +",    " @ @ @ ")
    test("+ + + ",    "@ @ @ ")
    test(" + + + ",   " @ @ @")
