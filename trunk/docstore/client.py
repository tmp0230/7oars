#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008 John Paulett (john -at- 7oars.com)
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

import httplib2

id = '123'
data = 'hello world'
#database = 'shelve'
database = 'fs'
#database = 'memory'
#action = 'POST'
action = 'PUT'
#action = 'DELETE'
base_url = 'http://localhost:8080'

def url(id):
    return '/'.join([base_url, database, id])

h = httplib2.Http()
resp, content = h.request(url(id), action, data)
print resp
print content



#resp, content = h.request('abc', 'POST', 'test string5')

