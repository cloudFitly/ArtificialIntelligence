# util.py
# --------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

""" Data useful things. You should not need to look at this at all.

********** YOU SHOULD NOT CHANGE ANYTHING IN THIS FILE **********
"""

import inspect
import io
import random
# code to handle timeouts
# FIXME
# NOTE: TimeoutFuncton is NOT reentrant.  Later timeouts will silently
# disable earlier timeouts.  Could be solved by maintaining a global list
# of active time outs.  Currently, questions which have test cases calling
# this have all student code so wrapped.
#
import signal
import sys
import time


def raise_not_defined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]
    print("*** Method not implemented: %s at line %s of %s" %
          (method, line, fileName))
    sys.exit(1)


class TimeoutFunctionException(Exception):
    """Exception to raise on a timeout"""
    pass


class TimeoutFunction:
    def __init__(self, function, timeout):
        self.timeout = timeout
        self.function = function

    def handle_timeout(self, signum, frame):
        raise TimeoutFunctionException()

    def __call__(self, *args, **keyArgs):
        startTime = time.time()
        result = self.function(*args, **keyArgs)
        timeElapsed = time.time() - startTime
        if timeElapsed >= self.timeout:
            self.handle_timeout(None, None)
        return result
