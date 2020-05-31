# -*- coding: utf-8 -*-
"""
Created on Sat May 30 16:14:18 2020

@author: Philip
"""
import os
import sys
from contextlib import contextmanager
import pandas as pd
# May also require xlrd install as dependency for pandas
import unicodecsv as csv
import io
import re



def genRawCSV():    
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
    print '**********Create raw, untranslated csv files from xls files**********'
    # Preset xls_dir
    xls_dir = os.path.join(cwd,r'excel')
    root_dir = cwd
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
            with change_dir(os.path.normpath(root_dir)):            
                # Create new subdirectory to place csv files
                try:
                    os.makedirs(os.path.join('raw_csv', name))
                except WindowsError:
                    print sys.exc_info()[1]
                    print 'raw_csv/{} directory already created.'.format(name)
                # Change to new subdirectory
                with change_dir(os.path.join(root_dir, 'raw_csv', name)):
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

genRawCSV()

def findCompoundPhones():
    """
    Locate all unique compound phones from original dataset.
    """
    # Set default directory to location of script
    os.chdir(os.path.dirname(sys.argv[0]))
    cwd = os.getcwd()        
    rootDir = cwd
    xlsDir = os.path.join(rootDir, r'excel')
    result = []
    # for each file in list of files in directory xls_dir...
    for fName in os.listdir(xlsDir):        
        # Read Excel file as dictionary of Pandas DataFrames (data_xls) Key = sheet name
        try:
            data_xls = pd.read_excel(os.path.join(xlsDir, fName), None)
        except:
            print sys.exc_info()[1]
            print 'Unable to read {} {}'.format(fName, type(fName))
            print '{} skipped'.format(fName)
            break        
        xls_keys = data_xls.keys()
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
                    dfReduced = df_sheet[col].str.findall(r'\S\S', re.UNICODE)
                    for item in dfReduced:
                        if type(item) == str:
                            result.append(item)
                        if type(item) == list:
                            for i in item:
                                result.append(i)
    return set(result)
"""
    text = []
    for dirName, subDirList, fileList in os.walk(csvDir):
        for fName in fileList:
            with io.open(os.path.join(dirName, fName), mode='r', 
                         encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for i, row in enumerate(reader):
                    if i == 1:
                        continue
                    else:
                        text.append(row[2:])
    return text
"""

allText = findCompoundPhones()
with open('compoundPhones.csv', 'wb') as csvOutput:
    writer = csv.writer(csvOutput, encoding = 'utf-8')
    writer.writerow(list(allText))
                
    
    