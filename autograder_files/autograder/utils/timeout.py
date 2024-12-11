
"""
Threading-based Timeout Decorator

This module provides a timeout decorator that interrupts a function's
execution if it exceeds the maximum runtime specified. It uses Python's
`threading` and `_thread` modules to manage timeouts and interrupt the
main thread when necessary. Additionally, it supports custom callback
functions when a timeout occurs.

Functions
---------
  
- timeout(max_runtime: float = 1, timeout_callback=None, timeout_callback_params={}):
    A decorator function that adds a timeout mechanism to any function.
    It raises a TimeoutError if the function exceeds the specified runtime.

Copyrights
----------
Author: Jiarui Li
Update Date: 2024/10/21
This module is designed for Tulane University Computer Science course
CMPS 2200 Introduction to Algorithm.
"""

import _thread
import threading
import unittest
from functools import wraps

def _timeout_quit():
    """ Timeout quit function
    
    Parameters
    ----------
    callback : function | None, default: None
        The callback function, which will be call when the function timeout
    param    : dict, default: {}
        The kwargs parameters for the callback function
    """
    _thread.interrupt_main() # Interrupt the main threading
    
def timeout(max_runtime:float=1, timeout_callback=None, timeout_callback_params={}):
    """ Timeout wrapper
    
    Parameters
    ----------
    max_runtime : float, default: 1
        The max runtime for the function
    timeout_callback : function | None, default: None
        The callback function, which will be call when the function timeout
    timeout_callback_params : dict, default: {}
        The kwargs parameters for the callback function
        
    Returns
    -------
    The output of the function if it is finished in time.
    Else, return the output of the timeout_callback or
    raise TimeoutError.
    
    Examples
    --------
    >>> import time
    >>> @timeout(0.01)
    >>> def test_func(interval=10): for i in range(interval): time.sleep(0.1)
    >>> test_func(10)
    TimeoutError: 
    """
    def _timeout_outer_wrap(func):
        @wraps(func)
        def _timeout_inner_wrap(*args, **kwargs):
            # Create a timer as watchdog
            _timer = threading.Timer(max_runtime, function=_timeout_quit, args=[])
            _timer.start()
            try: return func(*args, **kwargs)
            except KeyboardInterrupt:
                # Handle the timeout condition
                if timeout_callback is not None and callable(timeout_callback):
                    return timeout_callback(**timeout_callback_params)
                else: raise TimeoutError
            # Processing none timeout error
            except Exception as e: raise e
            finally: _timer.cancel()
        return _timeout_inner_wrap
    return _timeout_outer_wrap