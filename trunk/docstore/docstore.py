#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008 John Paulett (john -at- 7oars.com)
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

from __future__ import with_statement 
import web
import re
import os
import shelve
import uuid
#try:
#    import hgshelve
#except ImportError:
#    print 'Warning: hgshelve not installed'

"""A RESTful document store.  Each document is stored with a 
key value.  We provide several implementations of the document
store:
 * MemoryDB - all documents are stored in memory and will be lost upon 
              server restart.
              http://server/memory/
 * FilesystemDB - all documents are persisted into a specified
                  directory, so that each document is in a separate
                  file.
                  http://server/fs/
 * ShelveDB - all documents are persisted with a Python shelve store.
              http://server/shelve/

Keys may be characters, numbers, dashes, and underscores, with a length
of at least one and a max of 255.

All operations occur with the HTTP primitives (GET, POST, PUT, DELETE).
Documents can be uploaded either via PUT or POST.  PUT does not 
require a key, but a generated, unique, key will be provided in the 
response  For example, issuing a PUT to http://server/shelve/ with the
document will return an id of the document. POST requires a key and data.
For example, sending a POST to http://server/shelve/123456789 with a 
document will store this document at this key.  If a document already
exists with that key, it will be overwritten.

To retreive a listing of all the documents in a database, perform a GET
on the root of the database, e.g. http://server/shelve/

To obtain a specific document issue a GET request to the database with 
the documents key, e.g. http://server/shelve/123456789

To delete a document, simple issue an HTTP DELETE command to the 
resource, e.g. to http://server/shelve/123456789.
"""

VALID_KEY = re.compile('[a-zA-Z0-9_-]{1,255}')

urls = (
        '/memory/(.*)', 'MemoryDB',
        '/fs/(.*)', 'FilesystemDB',
        '/shelve/(.*)', 'ShelveDB',
        #'/hgshelve/(.*)','HgShelveDB'
        )

def is_valid_key(key):
    """Checks to see if the parameter follows the allow pattern of
    keys.
    """
    if VALID_KEY.match(key) is not None:
        return True
    return False
    
def validate_key(fn):
    """Decorator for HTTP methods that validates if resource 
    name is a valid database key. Used to protect against 
    directory traversal.
    """
    def new(*args):
        if not is_valid_key(args[1]):
            web.badrequest()
        return fn(*args)
    return new

class AbstractDB(object):
    """Abstract database that handles the high-level HTTP primitives.
    """
    def GET(self, name):
        if len(name) <= 0:
            print '<html><body><b>Keys:</b><br />'
            for key in self.keys():
                print ''.join(['<a href="',str(key),'">',str(key),'</a><br />'])
            print '</body></html>'
        else:
            self.get_resource(name)
           
    @validate_key
    def POST(self, name):
        data = web.data()
        self.put_key(str(name), data)
        print str(name)
        
    @validate_key
    def DELETE(self, name):
        self.delete_key(str(name))
        
    def PUT(self, name=None):
        """Creates a new document with the request's data and 
        generates a unique key for that document.
        """
        key = str(uuid.uuid4())
        self.POST(key)
        print key

    @validate_key
    def get_resource(self, name):
        result = self.get_key(str(name))
        if result is not None: 
            print result
        
class MemoryDB(AbstractDB):
    """In memory storage engine.  Lacks persistence.
    """
    database = {}
    def get_key(self, key):
        try:
            return self.database[key]
        except KeyError:
            web.notfound()
            
    def put_key(self, key, data):
        self.database[key] = data
    
    def delete_key(self, key):
        try:
            del(self.database[key])
        except KeyError:
            web.notfound()
    
    def keys(self):
        return self.database.iterkeys()
    
class FilesystemDB(AbstractDB):
    """Storage engine that stores a file
    for each document.
    """
    db_dir = 'db'
    def get_key(self, key):
        try:
            with open(self.file_name(key), 'rb') as f:
                return f.read()
        except:
            web.internalerror()
        
    def put_key(self, key, data):
        try:
            with open(self.file_name(key), 'wb') as f:
                f.write(data)
        except:
            web.internalerror()
    
    def delete_key(self, key):
        try:
            os.remove(self.file_name(key))
        except:
            web.internalerror()
    
    def keys(self):
        return os.listdir(self.db_dir)
    
    def file_name(self, key):
        return os.path.join(self.db_dir, key)

class ShelveDB(MemoryDB):
    """Storage engine based upon the Python shelve module.
    All documents persisted.
    """
    database = shelve.open('shelve.db', writeback=True)
    
    def put_key(self, key, data):
        super(ShelveDB, self).put_key(key, data)
        self.commit()
    
    def delete_key(self, key):
        super(ShelveDB, self).delete_key(key)
        self.commit()
        
    def commit(self):
        self.database.sync()

#class HgShelveDB(ShelveDB):
#    database = hgshelve.open('hgrepo')

if __name__ == "__main__": 
    web.run(urls, globals())

