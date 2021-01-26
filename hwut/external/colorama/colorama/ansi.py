# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
# 15y01m23d: 'plain_length' implemented by Frank-Rene Schaefer.
'''
This module generates ANSI character codes to printing colors to terminals.
See: http://en.wikipedia.org/wiki/ANSI_escape_code
'''
from itertools import chain

CSI = '\033['
OSC = '\033]'
BEL = '\007'

CONTROL_CHAR_BEGIN_SET = (CSI[0], OSC[0], BEL[0])


def code_to_chars(code):
    return CSI + str(code) + 'm'

class AnsiCodes(object):
    def __init__(self, codes):
        for name in dir(codes):
            if not name.startswith('_'):
                value = getattr(codes, name)
                setattr(self, name, code_to_chars(value))


class AnsiCursor(object):
    def UP(self, n=1):
        return CSI + str(n) + "A"
    def DOWN(self, n=1):
        return CSI + str(n) + "B"
    def FORWARD(self, n=1):
        return CSI + str(n) + "C"
    def BACK(self, n=1):
        return CSI + str(n) + "D"
    def POS(self, x=1, y=1):
        return CSI + str(y) + ";" + str(x) + "H"

def set_title(title):
    return OSC + "2;" + title + BEL

def clear_screen(mode=2):
    return CSI + str(mode) + "J"

def clear_line(mode=2):
    return CSI + str(mode) + "K"


class AnsiFore:
    BLACK           = 30
    RED             = 31
    GREEN           = 32
    YELLOW          = 33
    BLUE            = 34
    MAGENTA         = 35
    CYAN            = 36
    WHITE           = 37
    RESET           = 39

    # These are fairly well supported, but not part of the standard.
    LIGHTBLACK_EX   = 90
    LIGHTRED_EX     = 91
    LIGHTGREEN_EX   = 92
    LIGHTYELLOW_EX  = 93
    LIGHTBLUE_EX    = 94
    LIGHTMAGENTA_EX = 95
    LIGHTCYAN_EX    = 96
    LIGHTWHITE_EX   = 97


class AnsiBack:
    BLACK           = 40
    RED             = 41
    GREEN           = 42
    YELLOW          = 43
    BLUE            = 44
    MAGENTA         = 45
    CYAN            = 46
    WHITE           = 47
    RESET           = 49

    # These are fairly well supported, but not part of the standard.
    LIGHTBLACK_EX   = 100
    LIGHTRED_EX     = 101
    LIGHTGREEN_EX   = 102
    LIGHTYELLOW_EX  = 103
    LIGHTBLUE_EX    = 104
    LIGHTMAGENTA_EX = 105
    LIGHTCYAN_EX    = 106
    LIGHTWHITE_EX   = 107


class AnsiStyle:
    BRIGHT    = 1
    DIM       = 2
    NORMAL    = 22
    RESET_ALL = 0

Fore   = AnsiCodes( AnsiFore )
Back   = AnsiCodes( AnsiBack )
Style  = AnsiCodes( AnsiStyle )
Cursor = AnsiCursor()

_all_codes = [
    value
    for name, value in chain(Fore.__dict__.iteritems(), 
                             Back.__dict__.iteritems(), 
                             Style.__dict__.iteritems(), 
                             Cursor.__dict__.iteritems()) 
    if name and name[0] != "_"
]

def _all_codes_detect_begin(Text, Begin):
    """RETURNS: Number of characters to skip in order to skip the code letters
                at the beginning of 'Text' at position 'Begin'.
    """
    for code in _all_codes:
        if Text.startswith(code, Begin): 
            return len(code)
    return 0

def plain_length(Text):
    """RETURNS: length of the plain text, ignoring the ANSI control characters.
    """
    global _all_codes

    L = len(Text)
    n = 0
    i = -1
    while i < L - 1:
        i += 1
        letter = Text[i]
        if letter in ('\r', '\n'):
            i += 1
        if letter not in CONTROL_CHAR_BEGIN_SET:
            n += 1
        else:
            i += _all_codes_detect_begin(Text, i) 
    return n

        



