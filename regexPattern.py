# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 16:47:26 2020

@author: Philip
"""
import re

def regexPattern(prefix = None, suffix = None, groups = None):

    regexEntries = input('Paste column of entries:')
    regexEntriesList = regexEntries.split("\n")
    
    revRegexList = [] 
    for entry in regexEntriesList:
        if prefix != None:
            entry = prefix + entry
        if suffix != None:
            entry = entry + suffix
        if groups == 'capture':
            entry = '('+entry+')'
        if groups == 'noncapture':
            entry = '(?:'+entry+')'
        revRegexList.append(entry)
    pattern = re.compile(r'|'.join(revRegexList))
    print("*****************************************")
    print(r'|'.join(revRegexList))
    return pattern

regexPattern(prefix = ",.*,.*", groups='noncapture')