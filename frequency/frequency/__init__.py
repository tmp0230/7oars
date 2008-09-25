# -*- coding: utf-8 -*-
#
# Copyright (C) 2008 John Paulett (john -at- 7oars.com)
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

import re
import operator
import random

from genetic import organism, lifecycle

def standardize(text):
    """Converts text into a basic form, with only alpha 
    characters, all lower case.  It is possible that
    the current implementation does not work with 
    unicode.
    
    >>> standardize('Hello World!\r')
    'helloworld'
    >>> standardize('12345')
    ''
    """
    # FIXME regex restricts us to only ascii
    # FIXME move regex compilation outside
    p = re.compile('[^a-zA-Z]')
    retval = p.sub('', text)
    retval = retval.lower()
    return retval

def relative(dict):
    """Finds the relative values of each value in a dictionary
    based upon the total sum of the values.  Non-destructive 
    operation on the dict.
    
    >>> import math
    >>> d = {'a':7, 'b':3}
    >>> r = relative(d)
    >>> math.floor(r['a']*100)
    70.0
    >>> math.floor(r['b']*100)
    30.0
    """
    retval = {}
    count = float(sum(dict.values()))
    for k, v in dict.iteritems():
        retval[k] = v / count
    return retval
    
def find_frequency(text, n=1):
    """Finds the raw frequencies of all the n-grams in text.
    The n sets the size of the n gram.  n=1 is a unigram, 
    n=2 is a bigram, etc.
    
    >>> f = find_frequency('aba')
    >>> f['a']
    2
    >>> f['b']
    1
    >>> f = find_frequency('ababa', n=2)
    >>> f['ab']
    2
    >>> f['ba']
    2
    """
    freqs = {}
    length = len(text)
    for i in xrange(0, length):
        upper = i+n
        if upper > length:
            break
        gram = text[i:upper]
        dict_operate(freqs, gram, 1, operator.add)
    return freqs
    
def dict_operate(dict, key, value, operation=None):
    """Performs an operation on a specific key of the dict,
    using the existing value of that key. If the key does
    not exist, the value is set into the key. Also, if
    the operation is None, the value is set into the key,
    no matter what exists at that key.  Destructive 
    operation on the dict.
    
    >>> d = {'a':10, 'b':12, 'c':3}
    >>> dict_operate(d, 'a', 5, operator.add)
    >>> d['a']
    15
    >>> dict_operate(d, 'b', 2, operator.mul)
    >>> d['b']
    24
    >>> dict_operate(d, 'd', 25)
    >>> d['d']
    25
    >>> dict_operate(d, 'c', 1.5)
    >>> d['c']
    1.5
    """
    if key in dict and operation is not None:
        dict[key] = operation(dict[key], value)
    else:
        dict[key] = value

def important_words(words):
    """Filters a list of words to those are are valuable.
    Currently only makes sure that words are at least
    three characters.
    
    >>> w = ['hello', 'world', 'the', 'a', 'an']
    >>> important_words(w)
    ['hello', 'world', 'the']
    """
    return [x for x in words if len(x) >= 3]

def match_dictionary(text, common_words):
    if text is None:
        return 0

    found_words = {}
    for word in common_words:
        count = text.count(word)
        if count > 1:
            # discount words that are found more than once
            found_words[word] = count * 0.75 
        elif count == 1:
            found_words[word] = 1
             
    return sum(found_words.values())

published_frequencies = {'a':0.12, 'b':0.07}

def create_translation(experimental, known):
    """Given a known and experimental pair of letter-frequency
    dictionaries, a translation table is constructed with the 
    experimental letter as the key and the known letter as the value.
    
    >>> e = {'a':10, 'b':7, 'c':3}
    >>> k = {'a':2, 'b':3, 'c':1}
    >>> t = create_translation(e, k)
    >>> t['a']
    'b'
    >>> t['b']
    'a'
    >>> t['c']
    'c'
    """
    f = lambda x: sorted(x.items(), key=operator.itemgetter(1))
    g = lambda y: [x[0] for x in f(y)]
    
    exp_list = g(experimental)
    known_list = g(known)
    retval = {}
    limit = min([len(exp_list), len(known_list)])
    for i in xrange(0, limit):
        retval[exp_list[i]] = known_list[i]
    return retval    
    
    
def translate(text, translation):
    """Translates the text based upon the lookup dictionary.
    The translation dictionary holds to original value as the key
    and the translate to value as the value.
    
    >>> translation = {'a':'g', 'b':'i', 'y':'t'}
    >>> translate('abyby', translation)
    'gitit'
    >>> translate('abybyhelloab', translation)
    'gitit_____gi'
    """
    new = [] 
    for i in xrange(0, len(text)):
        char = text[i]
        try:
            new.append(translation[char])
        except KeyError:
            new.append('_')
    return ''.join(new)

def kasiski():
    pass

def euclid(a, b):
    while b != 0:
        r = a % b
        a = b
        b = r
    return a
    
def pollard_rho(n):
    """Modified from http://snippets.dzone.com/posts/show/4201
    
    >>> r=pollard_rho(100)
    >>> print r
    'a'
    """
    retval = []
    i = 1
    x = random.randint(0, n - 1)
    y = x
    k = 2
    tried = set()
    tried.add(x)
    while True:
        i = i + 1
        x = (x ** 2 - 1) % n
        if x in tried:
            break
        tried.add(x)
        d = euclid(y - x, n)
        if d != 1 and d != n:
            # factor
            #retval.append(d)
            print d
        if i == k:
            y = x
            k = 2 * k
    return retval    
