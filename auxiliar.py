# -*- coding: utf-8 -*-
"""
Created on Sat May 30 16:14:18 2020

@author: Philip Combiths

Phon DPA Script Auxiliar Functions
"""
from __future__ import absolute_import
from __future__ import print_function
import os
import sys
from contextlib import contextmanager
import pandas as pd
# May also require xlrd install as dependency for pandas
import regex as re
from six.moves import input
import unicodecsv as csv


def genRawCSV():    
    """
    From a directory of xls files from the Developmental Phonologies Archive
    (DPA; Gierut, 2015), extracts probe transcription data and exports as csv files,
    organized by participant ID.
    
    Requires:
        'xls' directory containing DPA xls files in current working directory
    
    Generates:
        'raw_csv' directory containing data in csv files, in current working 
        directory
    """
    
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
        
    ### Step 1a: Create raw csv files
    print('**********Create raw, untranslated csv files from xls files**********')
    # Preset xls_dir
    xls_dir = os.path.join(cwd,r'excel')
    root_dir = cwd
    # If directory is not preset, get user input
    try:
        xls_dir
    except NameError:
        xls_dir = os.path.normpath(input('xls directory not specified. Enter xls directory path: '))
    
    with change_dir(os.path.normpath(xls_dir)):
        print("XLS Directory set to: ", os.getcwd())
        # for each file in list of files in directory xls_dir...
        for file in os.listdir(xls_dir):
            # Read Excel file as dictionary of Pandas DataFrames (data_xls) Key = sheet name
            try:
                data_xls = pd.read_excel(file, None)
            except:
                print(sys.exc_info()[1])
                print('Unable to read {}'.format(file))
            # Extract participant number from file name
            name = file[:file.find('_')]
            with change_dir(os.path.normpath(root_dir)):            
                # Create new subdirectory to place csv files
                try:
                    os.makedirs(os.path.join('rawCSV', name))
                except WindowsError:
                    print(sys.exc_info()[1])
                    print('rawCSV/{} directory already created.'.format(name))
                # Change to new subdirectory
                with change_dir(os.path.join(root_dir, 'rawCSV', name)):
                    print("Working in directory: ", os.getcwd())
                    # Get list of sheets as xls_keys
                    xls_keys = list(data_xls.keys())
                    # For each sheet in file...
                    for sheet in data_xls:
                        # create Probe:CA dictionary
                        if sheet == 'Probe Schedule':
                            continue
                        # Exclude 'Copyright' sheet
                        if sheet == 'Copyright':
                            continue
                        else: 
                            # Save DataFrame for sheet to CSV. Set name, encode as UTF-8, omit row index
                            data_xls[sheet].to_csv(sheet +'.csv', encoding = 'utf-8', index = False)
                    print('{} raw csv files complee'.format(name)) 
    print("All raw csv files created in rawCSV folder")


def combiningStrip(text):
    """
    From a string, remove combining diacritics and modifiers.
    
    Parameters:
        text : string
    
    Return string with combining characters removed
    """
    assert type(text) is str   
    
    unicodeBlockList = [r'\p{InCombining_Diacritical_Marks_for_Symbols}',
                        r'\p{InSuperscripts_and_Subscripts}',
                        r'\p{InCombining_Diacritical_Marks}',
                        r'\p{InSpacing_Modifier_Letters}',
                        r'\p{InCombining_Diacritical_Marks_Extended}'
                        r'\p{InCombining_Diacritical_Marks_Supplement}']

    pattern = r'(' + r'|'.join(unicodeBlockList) + r')'
    pattern = re.compile(pattern)
    # re.search(pattern, text)
    result = re.subn(pattern, '', text)
    
    return result[0]


def findCompoundPhones():
    """
    From a directory of xls files from the Developmental Phonologies Archive
    (DPA; Gierut, 2015), return all unique compound phones.
    
    Requires:
        'xls' directory containing DPA xls files in current working directory
        combiningStrip()
    
    Return list of unique compound phones 
    """
    # Set default directory to location of script
    os.chdir(os.path.dirname(sys.argv[0]))
    cwd = os.getcwd()        
    rootDir = cwd
    xlsDir = os.path.join(rootDir, r'excel')
    result = set()
    # for each file in list of files in directory xls_dir...
    for fName in os.listdir(xlsDir):        
        # Read Excel file as dictionary of Pandas DataFrames (data_xls) Key = sheet name
        try:
            data_xls = pd.read_excel(os.path.join(xlsDir, fName), None)
        except:
            print(sys.exc_info()[1])
            print('Unable to read {} {}'.format(fName, type(fName)))
            print('{} skipped'.format(fName))
            break        
        xls_keys = list(data_xls.keys())
        for sheet in data_xls:
            # Define working Excel tab as DataFrame
            df_sheet = data_xls[sheet]
           
            # Skip Copyright and Probe schedule sheets
            if sheet == 'Copyright' or sheet == 'Probe Schedule':
                continue
            else:                
                for col in df_sheet.columns:
                    if col == 'Target':
                        continue
                    if col == 'Word':
                        continue
                    df_sheet[col] = df_sheet[col].map(lambda x: combiningStrip(str(x)))
                    dfReduced = df_sheet[col].str.findall(r'\S+', re.UNICODE)
                    for item in dfReduced:
                        if type(item) == str:
                            result.add(item)
                        if type(item) == list:
                            for i in item:
                                result.add(i)
        print(f'{fName} searched')
        
    # Save result to csv in 'info' directory
    try:
        os.makedirs('info')
        print('Created:', os.path.join(os.getcwd(),'info'))
    except WindowsError:
        pass
    with open(os.path.join('info','compoundPhones.csv'), 'wb') as csvOutput:
        writer = csv.writer(csvOutput, encoding = 'utf-8')
        writer.writerow(list(set(result)))
    
    return list(result)

findCompoundPhones()

### Testing


"""
text = '◌̐  fg ak ◌̬sk gj◌⃰'
result = combiningStrip(text)

genRawCSV()

allText = findCompoundPhones()



with open('compoundPhones.csv', 'wb') as csvOutput:
    writer = csv.writer(csvOutput, encoding = 'utf-8')
    writer.writerow(list(allText))
"""
                
    
    