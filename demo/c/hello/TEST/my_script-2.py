#! /usr/bin/env python
# SPDX license identifier: MIT
# (C) 2006-2016 Frank-Rene Schaefer, private.
# (C) 2006-2016 Frank-Rene Schaefer, Visteon Innovation&Technology GmbH, 
#     Kerpen, Germany.
# This file is part of HWUT - Project.
# This Source Code Form is subject to the terms of the MIT License (MIT).
#------------------------------------------------------------------------------
import sys

if "--hwut-info" in sys.argv:
    print "Greeting: German"  # Title = 'Group Title' ':' 'Title'
    sys.exit(0)


print "Hallo Welt"
