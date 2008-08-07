# -*- coding: utf-8 -*-
#
# Copyright (C) 2008 John Paulett (john -at- 7oars.com)
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

import time

"""Simple timer.  Great for finding out how long code takes to execute.

>>> import stopwatch
>>> t = stopwatch.Timer()
>>> t.elapsed
...
>>> print t
...
>>> t.stop()
>>> print t
>>> print t
"""

__version__ = '0.2.0'

class Timer(object):
    def __init__(self):
        self.__stopped = None
        self.__start = time.time()
  
    def stop(self):
        self.__stopped = self.__time()
        return self.elapsed

    @property
    def elapsed(self):
        return self.__time() - self.__start
        
    def __time(self):
        if self.__stopped is not None:
            return self.__stopped
        return time.time()
    
    def __str__(self):
        return str(self.elapsed) + ' sec'
    