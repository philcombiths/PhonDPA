# -*- coding: utf-8 -*-
"""
Created on Sat May 30 15:43:32 2020
@author: Philip
"""
#### Step 0: Preliminaries
from __future__ import absolute_import
from __future__ import print_function
import pandas as pd
# May also require xlrd install as dependency for pandas
import os
import io
import sys
import xml.etree.ElementTree as etree
from contextlib import contextmanager
from six.moves import input
from auxiliar import genRawCSV


def illegalChars():    
    # Set default directory to location of script
    os.chdir(os.path.dirname(sys.argv[0]))
    cwd = os.getcwd()  

    # Create contextmanager function that changes directory then returns to 
    # original directory upon completion
    
    @contextmanager
    def change_dir(newdir):
        prevdir = os.getcwd()
        try:
            yield os.chdir(os.path.expanduser(newdir)) 
        finally:
            os.chdir(prevdir)
    """
    Steps to create list of characters illegal in Phon:
    Create csv versions of excel files
    iterate through every CSV DPA file
        iterate through every row
            skip first row
                iterate through every column
                create a list of every segment
                turn list into a set
    convert ipa.xml to a list of the values of char values
    create a list of all the items in CSV set that do not occur in ipa.xml list
    """
    # Defined variables
    csv_char_list = []
    HTML_char_set = set()
    Phon_legal_chars = []
    csv_char_set = set()
    illegal_chars = []
    
    ### Create raw csv files if not in directory
    if os.path.isdir('rawCSV'):
        print("'rawCSV' folder already created.")
    else:
        genRawCSV()
        
    # Preset xls_dir
    xls_dir = os.path.join(cwd,r'excel')
    
    ### Use raw csv files and ipa.xml from Phon source code to 
    ### generate list of illegal characters to be replaced    
    raw_csv_dir = 'rawCSV'
    # Raw csv directory path
    try:
        raw_csv_dir
    except NameError:
        raw_csv_dir = os.path.normpath(input('Enter raw csv directory path: '))
    with change_dir(raw_csv_dir):   
        # Create list of csv files in subdirectories
        csv_files = [os.path.join(root, filename)
                    for root, dirs, files in os.walk(os.getcwd())
                    for filename in files
                    if filename.endswith((".csv"))]
        # Loop through files in directory
        for cur_csv in csv_files:
            # open CSV file in read mode with UTF-8 encoding
            with io.open(cur_csv, mode='r', encoding='utf-8') as current_csv:
                # Create string variable from CSV
                csv_str = current_csv.read()
                # Create a list of all the characters in the string
                for char in csv_str:
                    csv_char_list
                    csv_char_list.append(char)
        # Create a set of all the unique characters csv_char_set
        csv_char_set
        csv_char_set = set(csv_char_list)
    print('list of unique characters in dataset:')
    for char in csv_char_set:
        print(char, end=' ')
    
    # Get list of legal Phon characters by extracting character element dictionaries from ipa.xml

    if 'ipa.xml' not in os.listdir(os.path.join(cwd, r'files')):
        dir = os.path.normpath(input('File ipa.xml not found. Enter directory containing ipa.xml: '))
        with change_dir(os.path.normpath(dir)):
            tree = etree.parse('ipa.xml')
    else:    
        tree = etree.parse(r'files\ipa.xml')
    root = tree.getroot()
    
    # For each element in ipa.xml, extract the unicode value and add to new list
    for char in root:
        char_hex = list(char.attrib.values())
        Phon_legal_chars.append(char_hex[0])
    print('\ncsv_char_set and Phon_legal_chars created')
    print('illegal Phon characters:')
    for char in list(csv_char_set):
        if char in Phon_legal_chars:
            continue
        else:
            print(char, end=' ')
            illegal_chars.append(char)
            df_illegal_chars = pd.DataFrame(illegal_chars, columns = ['Illegal Characters'])
                ## Save CSV of replacement tracker
                # Change to new subdirectory
    with change_dir(cwd):                                 
        # Create new subdirectory to place csv files
        try:
            os.makedirs('info')
            print('Created:', os.path.join(os.getcwd(),'info'))
        except WindowsError:
            print('\ninfo/ directory already created.')
        # Change to new subdirectory
        with change_dir(os.path.join(cwd, 'info')):                                            
                df_illegal_chars.to_csv('illegal_chars.csv', encoding = 'utf-8', index = False)       
    print('illegal_chars list created')
    return

illegalChars()