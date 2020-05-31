# -*- coding: utf-8 -*-
"""
Created on Sat May 30 15:43:32 2020
@author: Philip
"""
#### Step 0: Preliminaries
import pandas as pd
# May also require xlrd install as dependency for pandas
import os
import io
import sys
import xml.etree.ElementTree as etree
from contextlib import contextmanager


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
    
    ### Step 1a: Create raw csv files
    print '**********Step 1a: Create raw, untranslated csv files**********'
    
    # Preset xls_dir
    xls_dir = os.path.join(cwd,r'excel')
    # If directory is not preset, get user input
    try:
        xls_dir
    except NameError:
        xls_dir = os.path.normpath(raw_input('xls directory not specified. Enter xls directory path: '))
    
    with change_dir(os.path.normpath(xls_dir)):
        print "XLS Directory set to: ", os.getcwd()
        # for each file in list of files in directory xls_dir...
        for file in os.listdir(xls_dir):
            # Read Excel file as dictionary of Pandas DataFrames (data_xls) Key = sheet name
            try:
                data_xls = pd.read_excel(file, None)
            except:
                print sys.exc_info()[1]
                print 'Unable to read {}'.format(file)
            # Extract participant number from file name
            name = file[:file.find('_')]
            # Create new subdirectory to place csv files
            try:
                os.makedirs(os.path.join('raw_csv', name))
            except WindowsError:
                print sys.exc_info()[1]
                print 'raw_csv/{} directory already created.'.format(name)
            # Change to new subdirectory
            with change_dir(os.path.join(xls_dir, 'raw_csv', name)):
                print "Working in directory: ", os.getcwd()
                # Get list of sheets as xls_keys
                xls_keys = data_xls.keys()
                # For each sheet in file...
                for sheet in data_xls:
                    # create Probe:CA dictionary
                    if sheet == 'Probe Schedule':
                        CA_dict = data_xls[sheet].set_index('Probe').T.to_dict('records')
                    # Exclude 'Copyright' sheet
                    if sheet == 'Copyright':
                        print name, "Copyright sheet excluded"
                    else: 
                        # Save DataFrame for sheet to CSV. Set name, encode as UTF-8, omit row index
                        data_xls[sheet].to_csv(sheet +'.csv', encoding = 'utf-8', index = False)
                print '{} raw csv files complete'.format(name) 
        print "All raw csv files created in raw_csv folder"
    
    ### Step 1b: Use raw csv files and ipa.xml from Phon source code to 
    ### generate list of illegal characters to be replaced
    
    print '**********Step 1b: Use raw csv files and ipa.xml from Phon source code to generate illegal_chars**********'
    
    raw_csv_dir = os.path.join(xls_dir,r'raw_csv')
    # Raw csv directory path
    try:
        raw_csv_dir
    except NameError:
        raw_csv_dir = os.path.normpath(raw_input('Enter raw csv directory path: '))
    with change_dir(os.path.normpath(raw_csv_dir)):   
        # Create list of csv files in subdirectories
        csv_files = [os.path.join(root, filename)
                    for root, dirs, files in os.walk(raw_csv_dir)
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
    print 'list of unique characters in dataset:'
    for char in csv_char_set:
        print char,
    
    # Get list of legal Phon characters by extracting character element dictionaries from ipa.xml

    if 'ipa.xml' not in os.listdir(os.path.join(cwd, r'files')):
        dir = os.path.normpath(raw_input('File ipa.xml not found. Enter directory containing ipa.xml: '))
        with change_dir(os.path.normpath(dir)):
            tree = etree.parse('ipa.xml')
    else:    
        tree = etree.parse(r'files\ipa.xml')
    root = tree.getroot()
    
    # For each element in ipa.xml, extract the unicode value and add to new list
    for char in root:
        char_hex = char.attrib.values()
        Phon_legal_chars.append(char_hex[0])
    print '\ncsv_char_set and Phon_legal_chars created'
    print 'illegal Phon characters:'
    for char in list(csv_char_set):
        if char in Phon_legal_chars:
            continue
        else:
            print char,
            illegal_chars.append(char)
            df_illegal_chars = pd.DataFrame(illegal_chars)
                ## Save CSV of replacement tracker
                # Change to new subdirectory
    with change_dir(cwd):                                 
        # Create new subdirectory to place csv files
        try:
            os.makedirs('info')
            print 'Created:', os.path.join(os.getcwd(),'info')
        except WindowsError:
            print '\ninfo/{} directory already created.'.format(name)
        # Change to new subdirectory
        with change_dir(os.path.join(cwd, 'info')):                                            
                df_illegal_chars.to_csv('illegal_chars.csv', encoding = 'utf-8')       
    print 'illegal_chars list created'
    return