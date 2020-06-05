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
# import csv
import unicodecsv as csv

# Establish origin directory and context navigation
os.chdir(os.path.dirname(sys.argv[0])) 
owd = os.getcwd()


@contextmanager
def enter_dir(newdir):
    prevdir = os.getcwd()
    try:
        yield os.chdir(newdir) 
    finally:
        os.chdir(prevdir)
        
        
@contextmanager
def change_dir(newdir):
    prevdir = os.getcwd()
    try:
        yield os.chdir(os.path.expanduser(newdir)) 
    finally:
        os.chdir(prevdir)



excludeList = ['(clock)', '(eat it)', '(pole)', 
            '(pulling)', '(sweatshirt)', '(that one)', '(that)', '(thunder)',
            'ziggy', 'pitch', 'quɑrter', 'nose', "'fire'"]

removeList = excludeList + ["(incomplete transcription)", "ɴʀ", "NR", "\[\]", "", "ᵗ", "□", "tuntun", "goʊːt"]

def accessExcelDict(xlsDirName):
    
    """
    From a directory of xls files in the current working directory, returns 
    a dictionary of a dictionary containing each Excel sheet/tab as a 
    pandas dataframe.
    
    Parameters:
        xlsDirName : a directory name of xls files named '####_PHON.xls'
    
    Returns:
        data_xls : a dict {#### : dict{sheet : DataFrame}}
    """

    xlsDict = {}
    with enter_dir(xlsDirName):
        print('Reading xls files to pandas DataFrames...')
        # for each file in list of files in directory xls_dir...
        for file in os.listdir():
            # Read Excel file as dictionary of Pandas DataFrames (data_xls) Key = sheet name
            try:
                data_xls = pd.read_excel(file, None)
            except:
                print(sys.exc_info()[1])
                print('Unable to read {}'.format(file))
                continue
            # Extract participant number from file name
            name = file[:file.find('_')]
            # Get list of sheets as xls_keys
            xls_keys = list(data_xls.keys())
            xlsDict.update({name : data_xls})
    print('DataFrames generated')
    return xlsDict


def accessExcelGenerator(sheetSelection='probes'):
    
    """
    Generator. Continuation of accessExcelDict(). From a dictionary of 
    dictionaries of DataFrames, iterate through each DataFrame.
    
    Parameters: 
        sheetSelection : str indicating which Excel sheets to extract.
            'probes' : (default) every probe sheet    
            'allsheets' : every sheet, including 'Copyright', 'Probe Schedule'
            a probe name : matches and extracts only the given probe

    Returns tuple(partID, sheet, dfSheet)
    """ 
    
    xlsDict = accessExcelDict('excel')    
    if sheetSelection == 'probes':                  # Extract probe sheets only
        for partID in xlsDict:
            for sheet in xlsDict[partID]:
                if sheet == 'Copyright' or sheet == 'Probe Schedule':
                    continue
                dfSheet = xlsDict[partID][sheet]
                yield partID, sheet, dfSheet
                dfSheet = xlsDict[partID][sheet]
                yield partID, sheet, dfSheet
    if sheetSelection == 'allsheets':                      # Extract all sheets
        for partID in xlsDict:
            for sheet in xlsDict[partID]:        
                dfSheet = xlsDict[partID][sheet]
                yield partID, sheet, dfSheet
    else:                                        # Extract specified sheet only
        for partID in xlsDict:
            for sheet in xlsDict[partID]:
                if sheet == sheetSelection:      
                    dfSheet = xlsDict[partID][sheet]
                    yield partID, sheet, dfSheet


def genRawCSV():    
    
    """
    From a directory of xls files from the Developmental Phonologies Archive
    (DPA; Gierut, 2015), extracts probe transcription data and exports as 
    csv files, organized by participant ID.
    
    Requires:
        'xls' directory containing DPA xls files in current working directory
    
    Generates:
        'rawCSV' directory containing data in csv files, in current working 
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
        
    ## Create raw csv files
    print('********Create raw, untranslated csv files from xls files********')
    # Preset xls_dir
    xls_dir = os.path.join(cwd,r'excel')
    root_dir = cwd
    # If directory is not preset, get user input
    try:
        xls_dir
    except NameError:
        xls_dir = os.path.normpath(input(
                'xls directory not specified. Enter xls directory path: '))
    
    with change_dir(os.path.normpath(xls_dir)):
        print("XLS Directory set to: ", os.getcwd())
        # for each file in list of files in directory xls_dir...
        for file in os.listdir(xls_dir):
            # Read Excel file as dictionary of Pandas DataFrames (data_xls) 
            # Key = sheet name
            try:
                data_xls = pd.read_excel(file, None)
            except:
                print(sys.exc_info()[1])
                print('Unable to read {}'.format(file))
                continue
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
                            # Save DataFrame for sheet to CSV. 
                            # Set name, encode as UTF-8, omit row index
                            data_xls[sheet].to_csv(sheet +'.csv', 
                                    encoding = 'utf-8', index = False)
                    print('{} raw csv files complete'.format(name)) 
    print("All raw csv files created in rawCSV folder")


def participantTranscriptConv():
    
    """
    Searches 'Probe Schedule' sheets in directory of xls files for transcription
    notes. Generates notes by participant as a csv file.
    
    Returns generated DataFrame
    """
    
    dfNotes = pd.DataFrame({'CA':[],
                        'Probe':[],
                        'Participant':[]})
    
    for partID, sheet, df in accessExcelGenerator('Probe Schedule'):
        notesOnly = df[df['CA'].str.contains("Note" )]
        notesOnly['Participant'] = partID
        dfNotes = dfNotes.append(notesOnly, ignore_index = True)
    dfNotes.drop(columns = ['CA'])
    dfNotes = dfNotes[['Participant', 'Probe']]
    dfNotes = dfNotes.rename(columns={'Probe': 'Convention'})

    dfNotes.to_csv('transcriptionNotes.csv', 
                   encoding = 'utf-8', index = False)
    print("'transcriptionNotes.csv' created in 'info' folder.")
    
    return dfNotes


def combiningStrip(text):
    
    """
    From a string, remove combining diacritics and modifiers.
    
    Parameters:
        text : string
    
    Requires regex module as re
    
    Return string with combining characters removed
    """
    
    assert type(text) is str   
    
    unicodeBlockList = [r'\p{InCombining_Diacritical_Marks_for_Symbols}',
                        r'\p{InSuperscripts_and_Subscripts}',
                        r'\p{InCombining_Diacritical_Marks}',
                        r'\p{InSpacing_Modifier_Letters}',
                        r'\p{InCombining_Diacritical_Marks_Extended}'
                        r'\p{InCombining_Diacritical_Marks_Supplement}']
    
    additionalChars = [r'ᴸ', r'ᵇ', r':', r'<', r'←', r'=', r"'", r"‚"]

    pattern = r'(' + r'|'.join(unicodeBlockList+additionalChars) + r')'
    pattern = re.compile(pattern)
    # re.search(pattern, text)
    result = re.subn(pattern, '', text)
    
    return result[0]

def reDiac():
    
    """
    Generate regex pattern to locate diacritics
    
    Requires regex module as re
    
    Return compiled regex pattern
    """
    
    assert type(text) is str   
    
    unicodeBlockList = [r'\p{InCombining_Diacritical_Marks_for_Symbols}',
                        r'\p{InSuperscripts_and_Subscripts}',
                        r'\p{InCombining_Diacritical_Marks}',
                        r'\p{InSpacing_Modifier_Letters}',
                        r'\p{InCombining_Diacritical_Marks_Extended}'
                        r'\p{InCombining_Diacritical_Marks_Supplement}']

    additionalChars = [r'ᴸ', r'ᵇ', r':', r'<', r'←', r'=', r"'", r"‚"]

    pattern = r'(' + r'|'.join(unicodeBlockList+additionalChars) + r')'
    pattern = re.compile(pattern)
    
    return pattern


def extractSegments(segmentType):
    
    """
    Given user-specified segmentType, searches all transcriptions  separated 
    by whitespace.in xls files and returns unique results as a list and saves
    result as csv in 'info' directory.
    
    Parameters:
        segmentType : str
            'phones' for all unitary and multi-component phones with diacritics
            'compounds' for compound phones only
            'characters' for all characters
    
    Requires accessExcelDict(), combiningStrip()
    
    Returns list of unique results and saves as csv in 'info' directory
    """
    
    assert segmentType in ['phones', 'compounds', 'characters', 'full_compounds'], """
    segmentType must be specified as:
        'phones' for all unitary and multi-component phones with diacritics
        'compounds' for base compound phones only
        'full_compounds' for compound phones with diacritics
        'characters' for all characters"""
        
    xlsDict = accessExcelDict('excel')
    result = set() 
    for xls in xlsDict:
        for sheet in xlsDict[xls]:
            # Define working Excel tab as DataFrame
            dfSheet = xlsDict[xls][sheet]
            
            # Skip Copyright and Probe schedule sheets
            if sheet == 'Copyright' or sheet == 'Probe Schedule':
                continue
            else:                
                for col in dfSheet.columns:
                    if col == 'Target':
                        continue
                    if col == 'Word':
                        continue
                    # Remove items from excludeList
                    for item in removeList:
                        dfSheet[col] = dfSheet[col].str.replace(
                                item, '', re.UNICODE)                   
                    else:
                        if segmentType == 'phones':
                            dfSheetIPA = dfSheet[col].str.findall(
                                    r'\S+', re.UNICODE)
                        if segmentType == 'compounds':
                            dfSheetIPA = dfSheet[col].map(
                                    lambda x: combiningStrip(str(x)))
                            dfSheetIPA = dfSheetIPA.str.findall(
                                    r'(?<!=̂̂̂)\S{2,}', re.UNICODE)
                        if segmentType == 'full_compounds':
                            dfSheetIPA = dfSheet[col].str.findall(
                                    r'\S{2,}', re.UNICODE)                            
                        if segmentType == 'characters':
                            dfSheetIPA = dfSheet[col].str.findall(
                                    r'\S', re.UNICODE)
                    for item in dfSheetIPA:
                        if type(item) == str:
                            result.add(item)
                        if type(item) == list:
                            for i in item:
                                result.add(i)
        print(f'{xls} searched')
    
    # Sort list by length
    result = sorted(list(result), key=len)
    
    # Save result to csv in 'info' directory
    try:
        os.makedirs('info')
        print('Created:', os.path.join(os.getcwd(),'info'))
    except WindowsError:
        pass
    with open(os.path.join('info',f'{segmentType}.csv'), 'wb') as csvOutput:
        writer = csv.writer(csvOutput, encoding = 'utf-8')
        for e in result:
            writer.writerow([e])
    print(f"'{segmentType}.csv' created in 'info' directory.")
    return result

# IN PROGRESS
"""
def locateSegments():
    # Get list of full compound phones
    segments = []
    output = pd.DataFrame()
    with enter_dir('info'):
        with open('full_compounds.csv') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                segments.append(line[0])
    for partID, probe, df in accessExcelGenerator():        
               
        
        for col in df.columns:
            if col == 'Target' or col == 'Word':
                continue
            else:                
                for i, row in df.iterrows():
                    df[col].astype(str).str.findall(r'\S{2,}')
                
                    row = df[df[col].astype(str).str.contains(r'\S{2,}')]

    return
"""
extractSegments('compounds')

# Testing 
df = pd.DataFrame({'Word' : ['Alpha', 'Beta', 'Comma', 'Delta'], 
                   'Transcription' : ['ælfə', 'beɪɾə', 'kɑmə', "faɪjəɹ   'fire'"]})
    
newDF = df[df['Transcription'].str.contains('fire')]

df.loc[newDF.index, 'Word'] = 'fire'
