# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
# 15y01m23d: 'plain_length' implemented by Frank-Rene Schaefer.
from .initialise  import init, deinit, reinit
from .ansi        import Fore, Back, Style, Cursor, plain_length
from .ansitowin32 import AnsiToWin32

__version__ = '0.3.3'

