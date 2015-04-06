# Introduction #
stopwatch is a very simple python timer.  I have found it very useful when I want to monitor how long specific parts of a program or specific processes/threads take to run.  Other great utilties already exist, such as timeit.py, but stopwatch is designed to be dead simple.

# Sample Usage #
```
>>> import stopwatch
>>> t = stopwatch.Timer() # immediately starts the clock
>>> t.elapsed # elapsed time in seconds
0.2
>>> t.elapsed
1.6
>>> str(t) # pretty print
1.8 sec
>>> for i in xrange(0, 10000)
>>>     pass
>>> t.elapsed # still going
10.4
>>> t.stop() # stop the timer
>>> t.elapsed
10.6
>>> t.elapsed # it will not go any more
10.6
```

There is also a decorator for measuring how long a function takes to execute:
```
>>> from stopwatch import clockit
>>> @clockit
    def multiply(a, b):
        return a * b
>>> r = multiple(4, 5)
multiple in 1.38282775879e-05 sec
>>> print r
20
```