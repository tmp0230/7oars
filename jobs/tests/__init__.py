# -*- coding: utf-8 -*-
#
# Copyright (C) 2008 John Paulett (john -at- 7oars.com)
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

import unittest
import doctest
import jobs
import processing

class Fibonacci(processing.Process):
    """Compute a Fibonacci sequence up to n and store in 'results' list."""
    def __init__(self, n):
        super(Fibonacci, self).__init__()  
        
        self.results = []
        self.n = n
        
    def run(self):
        a, b = 0, 1
        while b < self.n:
            self.results.append(b)
            a, b = b, a+b

class Empty(processing.Process):
    pass
  
class LocalJobRunnerTestCase(unittest.TestCase):
    def setUp(self):
        self.queue = []
        for i in xrange(0, 50):
            self.queue.append(Fibonacci(i))
        self.runner = jobs.LocalJobRunner(self.queue)
        
    def test_finished(self):
        self.assertFalse(self.runner.finished)
        self.runner.run()
        self.assertTrue(self.runner.finished)
        
    def test_time(self):
        self.runner.run()
        self.assertTrue(self.runner.runtime.elapsed > 0)
        self.assertEquals(50, len(self.runner.times))
    
    def test_queue_unaltered(self):
        self.assertEquals(50, len(self.queue))
        self.runner.run()
        self.assertEquals(50, len(self.queue))
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LocalJobRunnerTestCase))
    suite.addTest(doctest.DocTestSuite(jobs))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
    