# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 16:47:26 2020

@author: Philip
"""
import regex as re

def regexPattern(prefix = None, suffix = None, groups = None):

    """
    Generates a regexPattern from user input: a column of entries separated by
    newline. 
       
    Parameters:
        prefix: str. default None. prefix to each entry
        suffix: str. default None. suffix to each entry
        groups: str. default None. 
            'capture' : creates capturing groups around each entry
            'noncapture' : creates noncapturing groups around each entry
    
    Requires regex as re
    
    Returns compiled regex pattern and prints as string
    """
    
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

def elementwisePattern(between = None, frame = None):

    """
    Generates a string modifying elements of a string rom user input: 
        a column of entries separated by newline
        
    Parameters:
        between: str. default None. str to add between 1st and 2nd element
        frame: str. default None. str to add around each element
    
    Returns modified string and prints to console.
    """
    
    elementEntries = input('Paste column of entries:')
    elementEntriesList = elementEntries.split("\n")
    newEntriesList = []
    for entry in elementEntriesList:
        newEntry = ''
        for i, element in enumerate(entry):
            if frame != None:
                newElement = frame[0]+element+frame[1]
            else:
                newElement = element
            if between != None and i == 0:
                newEntry += newElement+between
            else:
                newEntry += newElement 
        newEntriesList.append(newEntry)
    print(','.join(newEntriesList))
    return ','.join(newEntriesList)
    