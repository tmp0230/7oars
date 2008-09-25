# -*- coding: utf-8 -*-
#
# Copyright (C) 2008 John Paulett (john -at- 7oars.com)
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

import doctest
import unittest

import frequency

def suite():
    suite = unittest.TestSuite()
    #suite.addTest(unittest.makeSuite(SlaveTestCase))
    suite.addTest(doctest.DocTestSuite(frequency))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
