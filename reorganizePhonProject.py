# -*- coding: utf-8 -*-
# Python 3.7
"""
With a specified Phon Project directory containing at least once corpus,
generates new corpora and filters Phon sessions into those corpora
based on specified keywords and filter words.

This generates new corpora folders. Does NOT modify original corpora folders.

Designed for use with DPA Project
"""

import os,os.path,shutil,fnmatch
from contextlib import contextmanager
import re


#------------------------------------------------------------------------------


# Create contextmanagers
@contextmanager
def change_dir(newdir):
    prevdir = os.getcwd()
    try:
        yield os.chdir(os.path.expanduser(newdir)) 
    finally:
        os.chdir(prevdir)


@contextmanager
def enter_dir(newdir):
    prevdir = os.getcwd()
    try:
        yield os.chdir(newdir) 
    finally:
        os.chdir(prevdir)
        
    
def organize_files_by_keyword(keyword):
    # Working in corpus folder
    projectDir = os.path.dirname(os.getcwd())
    PhonDir = os.path.dirname(projectDir)
    newCorpusDir = os.path.join(projectDir, keyword)
    
    # Create new corpus folder from keyword
    try:
        os.mkdir(newCorpusDir)
    except FileExistsError:
        print(f"{keyword} directory already exists. Adding to folder")
    
    for File in os.listdir():
        # If the name of the file contains a keyword
        if fnmatch.fnmatch(File,'*' + keyword + '*'):
            print(f"{File} Copied to {keyword} Directory")          
            # If the file is truly a file...
            if os.path.isfile(File):
                # Copy that file to the new corpus directory            
                try:
                    shutil.copy(File,newCorpusDir)
                except shutil.SameFileError:
                    continue
                    
                
    return PhonDir, newCorpusDir
                
            
def organize_files_by_regex(keyword):
    # Working in corpus folder
    projectDir = os.path.dirname(os.getcwd())
    PhonDir = os.path.dirname(projectDir)
    newCorpusName = keyword + '000s'
    newCorpusDir = os.path.join(projectDir, newCorpusName)
    
    try: 
        os.mkdir(newCorpusDir)
    except FileExistsError:
        print(f"{newCorpusName} directory already exists. Adding to folder")
        
    for File in os.listdir():
        reg_exp = re.compile(keyword+r'\d{3}')
        # If the name of the file contains a keyword
        if re.search(reg_exp, File):
            print(f"{File} Copied to {newCorpusName} Directory")        
            # If the file is truly a file...
            if os.path.isfile(File):
                try:
                    shutil.copy(File,newCorpusDir)
                except shutil.SameFileError:
                    continue
    return newCorpusName
                
            
def organize(corpusKey = None):
       
    # If no corpusKey is specified, sessions are grouped in corpuses
    # by participant number (e.g., 1000s, 2000s, 3000s)
    # This saves into the same folder as the current corpus.   
    if corpusKey == None:
        
        corpusNames = []
        for keyword in range(1,10):
                keyword = str(keyword)
                corpusNames.append(organize_files_by_regex(keyword))
        
        return corpusNames
    
    # Organize into corpora by keyword(s)
    else:
        if isinstance(corpusKey, str):
            organize_files_by_keyword(corpusKey)
        else:
            for corpus in corpusKey:
                organize_files_by_keyword(corpus)
        
        return

def reorganizePhonProject(projectDir, corpusKey=None, filterKey=None):

    with enter_dir(os.path.join('Phon', projectDir)):
        
        assert 'project.xml' in os.listdir(), "project.xml not found in project directory"
        
        # First sorting pass
        for f in os.listdir():
            if os.path.isdir(f):
                # Enter corpus folder
                with enter_dir(f):
                    if corpusKey == None:
                        corpusKey = organize(corpusKey)
                    else:
                        organize(corpusKey)
                    

                   
        # Second filter pass
        if filterKey != None:            
            
            for corpus in corpusKey:
                with enter_dir(corpus):
                    print(f"Deleting {corpus} sessions not in filterKey...")
                    for f in os.listdir():
                        if any([fnmatch.fnmatch(f,'*' + fil + '*') for fil in filterKey]):
                            continue
                        else:
                            # Check if file exists:
                            if os.path.isfile(f):
                                os.remove(f)
                            else:
                                print(f"ERROR: {f} Not found in {corpus} Directory")
                
                    print(f"{len(os.listdir())} Phon sessions copied to {corpus} corpus.")
    
    return



#reorganizePhonProject('DPA 3.0 - Original - Copy', ['Pre', 'Post'], ['PKP', 'OCP', 'CCP'])
reorganizePhonProject('DPA 3.0 - Original - Copy', filterKey=['PKP', 'GFTA'])

#with change_dir(os.path.normpath(root_directory)):
#    organize(7) # Set option number


### ToDo
# Output to a new Phon project, rather than inside the same directory
# Accept input from a Phon base project, rather than a corpus folder
# Allow organizing/filtering by multiple layers

