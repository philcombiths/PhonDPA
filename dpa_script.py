# -*- coding: utf-8 -*-
# python v2.7, 3.8 compatible
"""
## Phon DPA Script version 1.4.3

The purpose of this script is to transform a directory of XLSX files 
(containing phonetic transcriptions of single-word utterances) into CSV files 
compatible for import into Phon, a phonological analysis software.
In order to run succcessfully, this script is packaged with a directory "dict" 
of CSV files used as dictionaries to translate characters incompatible with 
Phon to Phon-readable equivalents. 

This translation of data is designed to transfer original XLSX files from the 
Learnability Project into Phon format for phonological analysis:

# Disclaimer
Phon_DPA was created by Philip Combiths, Jessica Barlow, and the Phonological 
Typologies Lab at San Diego State University.

Archival data were retrieved from the Gierut / Learnability Project collection 
of the IUScholarWorks repository at 
https://scholarworks.iu.edu/dspace/handle/2022/20061 
The archival data were original to the Learnability Project and supported by 
grants from the National Institutes of Health to Indiana University 
(DC00433, RR7031K, DC00076, DC001694; PI: Gierut). The views expressed herein 
do not represent those of the National Institutes of Health, Indiana University, 
or the Learnability Project. The author(s) assume(s) sole responsibility for any 
errors, modifications, misapplications, or misinterpretations that may have been 
introduced in extraction or use of the archival data

"""

#### Step 0: Preliminaries
from __future__ import absolute_import
from __future__ import print_function
import pandas as pd
# May also require xlrd install as dependency for pandas
import numpy as np
import os
import csv
import sys
import re
from collections import Counter
from collections import OrderedDict
from contextlib import contextmanager
import six
from six.moves import zip
from six.moves import input


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

#### Step 1: Get list of illegal characters. This step is optional 
#### if "other_chars_translate_dict.csv", "superscript_dict_initial.csv", 
#### and "superscript_dict_noninitial.csv" already exist in "dicts" directory.

print('**********Step 1: Check for translation dictionaries**********')
assert os.path.isfile(os.path.join(cwd,r'dicts\other_chars_translate_dict.csv')), 'superscript_dict_noninitial.csv not found. Exiting script.'
assert os.path.isfile(os.path.join(cwd,r'dicts\superscript_dict_initial.csv')), 'superscript_dict_initial.csv.csv not found. Exiting script.'
assert os.path.isfile(os.path.join(cwd,r'dicts\superscript_dict_noninitial.csv')), 'other_chars_translate_dict.csv not found. Exiting script.'
print(r'other_chars_translate_dict.csv, superscript_dict_initial.csv, and superscript_dict_noninitial.csv found in directory dicts')
print(r'Proceeding to Excel edits using these dictionaries')
   
#### Step 2: Work with Excel files as DataFrames
print('**********Step 2: Work with Excel files as DataFrames**********')

## Defined variables
word_list = []

# Create dictionary other_chars_dict from csv
other_chars_path = os.path.join(cwd,r"dicts\other_chars_translate_dict.csv")
reader1 = csv.DictReader(open(other_chars_path, encoding = 'utf-8')) 
for row in reader1:
    other_chars_dict = OrderedDict(row)

# Create ordered dictionary superscript_dict_initial from csv
superscript_dict_initial_path = os.path.join(cwd,r"dicts\superscript_dict_initial.csv")
dummylist = []
with open(superscript_dict_initial_path, 'r', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)
    for row in reader:
        dummylist.append(OrderedDict(list(zip(headers, row))))
superscript_dict_initial = dummylist[0]

# Create ordered dictionary superscript_dict_initial2 from csv
superscript_dict_initial_path2 = os.path.join(cwd,r"dicts\superscript_dict_initial_2.csv")
dummylist = []
with open(superscript_dict_initial_path2, 'r', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)
    for row in reader:
        dummylist.append(OrderedDict(list(zip(headers, row))))
superscript_dict_initial2 = dummylist[0]

# Create ordered dictionary superscript_dict_initial3 from csv
superscript_dict_initial_path3 = os.path.join(cwd,r"dicts\superscript_dict_initial_3.csv")
dummylist = []
with open(superscript_dict_initial_path3, 'r', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)
    for row in reader:
        dummylist.append(OrderedDict(list(zip(headers, row))))
superscript_dict_initial3 = dummylist[0]

# Create dictionary superscript_dict_noninitial from csv
superscript_dict_noninitial_path = os.path.join(cwd,r"dicts\superscript_dict_noninitial.csv")  
dummylist = []
with open(superscript_dict_noninitial_path, 'r', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)
    for row in reader:
        dummylist.append(OrderedDict(list(zip(headers, row))))
superscript_dict_noninitial = dummylist[0]

# Create dictionary notes_dict from csv
notes_dict_path = os.path.join(cwd,r"dicts\notes_dict.csv")
reader3 = csv.DictReader(open(notes_dict_path, encoding = 'utf-8')) 
for row in reader3:
    notes_dict = dict(row)
    
# Create word index for df
word_dict_path = os.path.join(cwd,r"dicts\word_dict.csv")
reader4 = csv.reader(open(word_dict_path, encoding = 'utf-8')) 
for row in reader4:
    word_dict = list(row)
    
# Create dictionary target_dict from csv
target_dict_path = os.path.join(cwd,r"dicts\target_dict.csv")
reader5 = csv.DictReader(open(target_dict_path, encoding = 'utf-8')) 
for row in reader5:
    target_dict = dict(row)

# Preset xls directory
xls_dir = os.path.join(cwd,r'excel')

# If preset directory is not present, get user input
try:
    xls_dir
except NameError:
    xls_dir = os.path.normpath(input('xls directory not specified. Enter xls directory path: '))
with change_dir(os.path.normpath(xls_dir)):
    print("XLS Directory set to: ", os.getcwd())
    
    print("""
    \n1) Iterate through Excel directory 
    \n2) generate subdirectory (Participant num.) for given file 
    \n3) generate dictionary of Pandas DataFrames for each sheet in file 
    \n4) iterate through each DataFrame in dictionary 
    \n    4.1) skip Copyright sheet and Probe Schedule Sheet
    \n5) perform cleanup and editing actions on each probe administration for Phon compatibility
    \n    5.11) Remove/replace instances of"""+r" ̹ ɑ ɢ \n  i"+" in Orthography")
    """
    \n    5.12) Replace thiers, moustach, loag typos in Orthography
    \n    5.21) create DI column
    \n    5.22) create Multiple Productions column using word counts to indicate number of repeated productions
    \n    5.23) create Notes column populated with No Response
    \n    5.24) create Probe and Participant Number Columns
    \n    5.25) create CA (chronological age) column using dictionary derived from Probe Schedule tab
    \n    5.31) replace characters in other_chars_dict.csv
    \n    5.32) delete extra whitespaces and []
    \n    5.33) replace characters in superscript_dict_initial.csv and superscript_dict_noninitial.csv
    \n    5.4)  populate IPA Target for each unique word with dictionary "target_dict.csv"
    \n6) save csv for each sheet in file in subdirectory
    \n7) return to base directory and repeat
    \n8 ) save csv of replacement/deletion counts
    """   
        
    # Create empty DataFrame for replace counts for each participant
    df_replace_counts = pd.DataFrame()    
   
    # for each file in list of files in directory xls_dir...
    for file in os.listdir(xls_dir):        
        # Read Excel file as dictionary of Pandas DataFrames (data_xls) Key = sheet name
        try:
            data_xls = pd.read_excel(file, None)
        except:
            print(sys.exc_info()[1])
            print('Unable to read {} {}'.format(file, type(file)))
            print('{} skipped'.format(file))
            break

        #Extract/create Probe:CA dictionary
        CA_dict = data_xls['Probe Schedule'].set_index('Probe').T.to_dict('records')[0]
        
        # Extract participant number from file name
        name = file[:file.find('_')]
        # Create new subdirectory to place csv files
        try:
            os.makedirs(os.path.join(cwd,'csv'))
            print('Working with participant', name)
        except WindowsError:
            print('Working with participant', name)
        
        # Change to new subdirectory
        with change_dir(os.path.join(cwd, 'csv')):
            print("Saving in directory: ", os.getcwd())
            # Get list of sheets as xls_keys
            xls_keys = list(data_xls.keys())
            for sheet in data_xls:
                # Define working Excel tab as DataFrame
                df_sheet = data_xls[sheet]
                
                # Define counting dictionary for replacements in current DataFrame
                sheet_rep_dict = Counter()
                
                # Skip Copyright and Probe schedule sheets
                if sheet == 'Copyright':
                    print(name, "Copyright sheet excluded")
                if sheet == 'Probe Schedule':
                    print(name, "Probe Schedule sheet excluded")
                    ### TODO get index of notes: accomplished with auxiliary.py
                else:                
                    for col in df_sheet.columns:
                        if col == 'Target':
                            print('Target skipped')
                        ## Working with Word column (replacements)
                        elif col =='Word':                            
                            # Replace ' i' with "-i"
                            cur_rep_count = df_sheet[col].str.count(u' i', re.UNICODE).sum()
                            sheet_rep_dict[u' i Ortho'+u'_to_-i'] += cur_rep_count                            
                            # replace all instances
                            df_sheet[col] = df_sheet[col].str.replace(u' i', u'-i', re.UNICODE)
                            if cur_rep_count > 0:
                                print('************************************')
                                print(u'{} instances of {} removed'.format(cur_rep_count, u'̹'))
                                                            
                            # Remove instances '\u0339' 
                            # cur_rep_count to track instances of replacements. In unicode
                            cur_rep_count = df_sheet[col].str.count(u'̹', re.UNICODE).sum()
                            sheet_rep_dict[u'̹ Ortho'+u'_removed'] += cur_rep_count                            
                            # replace all instances
                            df_sheet[col] = df_sheet[col].str.replace(u'̹', u'', re.UNICODE)
                            if cur_rep_count > 0:
                                print('************************************')
                                print(u'{} instances of {} removed'.format(cur_rep_count, u'̹'))
                                                                                                                                                               
                            # Replace 'ɑ' with 'a'
                            # cur_rep_count to track instances of replacements. In unicode
                            cur_rep_count = df_sheet[col].str.count(u'ɑ', re.UNICODE).sum()
                            sheet_rep_dict[u'ɑ Ortho'+u'_to_'+u'a'] += cur_rep_count                            
                            # replace all instances
                            df_sheet[col] = df_sheet[col].str.replace(u'ɑ', u'a', re.UNICODE)
                            if cur_rep_count > 0:
                                print('************************************')
                                print(u'{} instances of {} removed'.format(cur_rep_count, u'ɑ'))  
                        
                            # Replace ɢ in orthography with 'G'
                            # cur_rep_count to track instances of replacements. In unicode
                            cur_rep_count = df_sheet[col].str.count(u'ɢ', re.UNICODE).sum()
                            sheet_rep_dict[u'ɢ Ortho'+u'_to_'+u'G'] += cur_rep_count                            
                            # replace all instances
                            df_sheet[col] = df_sheet[col].str.replace(u'ɢ', u'G', re.UNICODE)
                            if cur_rep_count > 0:
                                print('************************************')
                                print(u'{} instances of {} replaced with {}'.format(cur_rep_count, u'ɢ', u'G'))                                                      
                            
                            # Replace '\r' with blank
                            # cur_rep_count to track instances of replacements. In unicode
                            cur_rep_count = df_sheet[col].str.count(u'\n', re.UNICODE).sum()
                            sheet_rep_dict[u'\n Ortho'+u'_to_'+u''] += cur_rep_count                            
                            # replace all instances
                            df_sheet[col] = df_sheet[col].str.replace(u'\n', '', re.UNICODE)
                            if cur_rep_count > 0:
                                print('************************************')
                                print(u'{} instances of {} removed'.format(cur_rep_count, u'new line'))
                            
                            # Replace 'thiers' with 'theirs'
                            # cur_rep_count to track instances of replacements. In unicode
                            cur_rep_count = df_sheet[col].str.count(r'^thiers$', re.UNICODE).sum()
                            sheet_rep_dict[r'^thiers$'+u'_to_'+u'theirs'] += cur_rep_count                            
                            # replace all instances
                            df_sheet[col] = df_sheet[col].str.replace(r'^thiers$', u'theirs', re.UNICODE)
                            if cur_rep_count > 0:
                                print('************************************')
                                print(u'{} instances of {} replaced with {}'.format(cur_rep_count, u'thiers', u'theirs'))
                                
                            # Replace 'moustach' with 'moustache'
                            # cur_rep_count to track instances of replacements. In unicode
                            cur_rep_count = df_sheet[col].str.count(r'^moustach$', re.UNICODE).sum()
                            sheet_rep_dict[r'^moustach$'+u'_to_'+u'moustache'] += cur_rep_count                            
                            # replace all instances
                            df_sheet[col] = df_sheet[col].str.replace(r'^moustach$', u'moustache', re.UNICODE)
                            if cur_rep_count > 0:
                                print('************************************')
                                print(u'{} instances of {} replaced with {}'.format(cur_rep_count, u'moustach', u'moustache'))                                                               

                            # Replace 'loag' with 'loaf'
                            # cur_rep_count to track instances of replacements. In unicode
                            cur_rep_count = df_sheet[col].str.count(r'^loag$', re.UNICODE).sum()
                            sheet_rep_dict[r'^loag$'+u'_to_'+u'loaf'] += cur_rep_count                            
                            # replace all instances
                            df_sheet[col] = df_sheet[col].str.replace(r'^loag$', u'loaf', re.UNICODE)
                            if cur_rep_count > 0:
                                print('************************************')
                                print(u'{} instances of {} replaced with {}'.format(cur_rep_count, u'loag', u'loaf'))                                                                                                                                 

                            # Update unique word_list
                            word_list = list(set(word_list+df_sheet[col].tolist()))
                           
                        else:                                               
                            ## Working with current probe administration column
                            
                            # Populate DI column (delayed/direct imitation) locating [] in cells.
                            df_sheet['DI'] = np.where(df_sheet[col].str.contains(u'\[\]|□', re.UNICODE, regex=True).fillna(False), 1, '')
                            
                            # Number of Productions Tier
                            df_sheet['NumProductions'] = np.where(df_sheet[col].str.contains('    [^\s](?! *\])', regex=True).fillna(False), 1.0+df_sheet[col].str.count('    [^\s](?! *\])', re.UNICODE), '')                       
                        
                            # NR "denotes 'no response'" - new column entry (Notes
                            df_sheet['Notes'] = np.where(df_sheet[col].str.contains(r'NR|ɴʀ', re.UNICODE, regex=True).fillna(False), 'No Response', "") 
                            
                            # Add participant number to metadata, participant tier, and name of file
                            df_sheet['Speaker'] = name
                            
                            # Add Probe to new tier and to name of file
                            df_sheet['Probe'] = sheet
                            
                            # Add Session to new tier and to name of file
                            df_sheet['Session'] = col
                            
                            # Add CA from CA_Dict to new tier and to session metadata 
                            try:
                                df_sheet['CA'] = CA_dict[col]
                            # Condition A and Condition B are not specified in column heading. Workaround follows:
                            except KeyError:
                                if ' A ' in sheet:
                                    try:
                                        df_sheet['CA'] = CA_dict['Cond A ' + col]
                                    except KeyError:
                                        df_sheet['CA'] = CA_dict['Ver A ' + col]
                                if ' B ' in sheet:
                                    try:
                                        df_sheet['CA'] = CA_dict['Cond B ' + col]
                                    except KeyError:
                                        df_sheet['CA'] = CA_dict['Ver B ' + col]                                                                                                                                                                                                                               
                            
                            # Populate IPA Target Tier with target_dict.csv
                            df_sheet = df_sheet.set_index('Word', drop=False)
                            df_sheet['IPA Target'] = pd.Series(target_dict, name='IPA Target')
                            
                            # Populate Notes Tier... other stuff?                
                            
                            
                            ## Replacements applying to all data go here:
                            
                            # Replace [] and □ with blank
                            # cur_rep_count to track instances of replacements. In unicode
                            cur_rep_count = df_sheet[col].str.count('\[\]', re.UNICODE).sum()
                            cur_rep_count += df_sheet[col].str.count('□', re.UNICODE).sum()
                            sheet_rep_dict[u'\[\] or □'+u'_to_'+u''] += cur_rep_count                            
                            # replace all instances of space ' {1,2}(?! )' with blank.
                            df_sheet[col] = df_sheet[col].str.replace('\[\]', '', re.UNICODE)
                            if cur_rep_count > 0:
                                print('************************************')
                                print(u'{} instances of {} removed'.format(cur_rep_count, '[]'))     
                            
                            # replace other translated segments other_chars_translate_dict.csv
                            # Also addresses " line parsing error with extra return in cell. Possible solution: remove /n before creating csv
                            # Also addresses removal of [] and some whitespaces
                            for key in other_chars_dict:
                                # cur_rep_count to track instances of replacements. In unicode
                                cur_rep_count = df_sheet[col].str.count(six.text_type(key), re.UNICODE).sum()
                                sheet_rep_dict[key+u'_to_'+ other_chars_dict[key]] += cur_rep_count             
                                # replace all instances of dictionary key with corresponding value. In unicode
                                df_sheet[col] = df_sheet[col].str.replace(six.text_type(key), six.text_type(other_chars_dict[key]), re.UNICODE)
                                if cur_rep_count > 0:
                                    print('************************************')
                                    print(u'{} instances of {} replaced with {}'.format(cur_rep_count, key, other_chars_dict[key]))                      
                                                                    
                            # Replace whitespaces, but leave space between multiple productions
                            # Mask excluding cells with multiple productions (these white spaces should remain)
                            mask = df_sheet.filter(['Word',col,'NumProductions'], axis=1).NumProductions == ''                           
                            # cur_rep_count to track instances of replacements. In unicode
                            cur_rep_count = df_sheet.loc[mask, col].str.count(' ', re.UNICODE).sum()
                            sheet_rep_dict[u' '+u'_to_'+u''] += cur_rep_count                            
                            # replace all instances of space ' ' with blank.
                            df_sheet.loc[mask, col] = df_sheet.loc[mask, col].str.replace(' ', '', re.UNICODE) 
                            if cur_rep_count > 0:
                                print('************************************')
                                print(u'{} instances of {} removed'.format(cur_rep_count, 'whitespace'))
                                                                                                              
                            # Replace single whitespaces in instances with multiple productions
                            mask = df_sheet.filter(['Word',col,'NumProductions'], axis=1).NumProductions != ''
                            # cur_rep_count to track instances of replacements. In unicode
                            cur_rep_count = df_sheet.loc[mask, col].str.count(' {1,3}(?! )', re.UNICODE).sum()
                            sheet_rep_dict[u' {1,3}(?! )'+u'_to_'+u''] += cur_rep_count                            
                            # replace all instances of space ' {1,2}(?! )' with blank.
                            df_sheet.loc[mask, col] = df_sheet.loc[mask, col].str.replace(' {1,3}(?! )', '', re.UNICODE)                             
                            if cur_rep_count > 0:
                                print('************************************')
                                print(u'{} instances of {} removed from records with multiple utterances'.format(cur_rep_count, 'whitespace'))                          
                            
                            # replace superscripts superscript_dict_initial.csv                
                            for key in superscript_dict_initial:
                                # cur_rep_count to track instances of replacements. In unicode
                                cur_rep_count = df_sheet[col].str.count(six.text_type(key), re.UNICODE).sum()
                                sheet_rep_dict[key+u'_to_'+ superscript_dict_initial[key]] += cur_rep_count             
                                # replace all instances of dictionary key with corresponding value. In unicode
                                df_sheet[col] = df_sheet[col].str.replace(six.text_type(key), six.text_type(superscript_dict_initial[key]), re.UNICODE)                               
                                if cur_rep_count > 0:
                                    print('************************************')
                                    print(u'{} instances of {} (initial) replaced with {}'.format(cur_rep_count, key, superscript_dict_initial[key]))

                            # replace superscripts superscript_dict_initial_2.csv                
                            for key in superscript_dict_initial2:
                                # cur_rep_count to track instances of replacements. In unicode
                                cur_rep_count = df_sheet[col].str.count(six.text_type(key), re.UNICODE).sum()
                                sheet_rep_dict[key+u'_to_'+ superscript_dict_initial2[key]] += cur_rep_count             
                                # replace all instances of dictionary key with corresponding value. In unicode
                                df_sheet[col] = df_sheet[col].str.replace(six.text_type(key), six.text_type(superscript_dict_initial2[key]), re.UNICODE)                               
                                if cur_rep_count > 0:
                                    print('************************************')
                                    print(u'{} instances of {} (initial) replaced with {}'.format(cur_rep_count, key, superscript_dict_initial2[key]))
                                    
                            # replace superscripts superscript_dict_initial_3.csv                
                            for key in superscript_dict_initial3:
                                # cur_rep_count to track instances of replacements. In unicode
                                cur_rep_count = df_sheet[col].str.count(six.text_type(key), re.UNICODE).sum()
                                sheet_rep_dict[key+u'_to_'+ superscript_dict_initial3[key]] += cur_rep_count             
                                # replace all instances of dictionary key with corresponding value. In unicode
                                df_sheet[col] = df_sheet[col].str.replace(six.text_type(key), six.text_type(superscript_dict_initial3[key]), re.UNICODE)                               
                                if cur_rep_count > 0:
                                    print('************************************')
                                    print(u'{} instances of {} (initial) replaced with {}'.format(cur_rep_count, key, superscript_dict_initial3[key]))
                                     
                            # replace superscripts superscript_dict_noninitial.csv                
                            for key in superscript_dict_noninitial:
                                # cur_rep_count to track instances of replacements. In unicode
                                cur_rep_count = df_sheet[col].str.count(six.text_type(key), re.UNICODE).sum()
                                sheet_rep_dict[key+u'_to_'+ superscript_dict_noninitial[key]] += cur_rep_count             
                                # replace all instances of dictionary key with corresponding value. In unicode
                                df_sheet[col] = df_sheet[col].str.replace(six.text_type(key), six.text_type(superscript_dict_noninitial[key]), re.UNICODE)                               
                                if cur_rep_count > 0:
                                    print('************************************')
                                    print(u'{} instances of {} (noninitial) replaced with {}'.format(cur_rep_count, key, superscript_dict_noninitial[key]))

                            # Duplicate words in 'Word' column according to how many repetitions of the word are recorded                                          
                            ########## Also, don't remove spaces in multiple words.
                                                        
                            # cur_rep_count to track instances of replacements. In unicode
                            cur_rep_count = df_sheet['NumProductions'].str.count('2.0', re.UNICODE).sum()                            
                            sheet_rep_dict[u'ortho x 2'] += cur_rep_count
                            cur_rep_count = df_sheet['NumProductions'].str.count('3.0', re.UNICODE).sum()                            
                            sheet_rep_dict[u'ortho x 3'] += cur_rep_count
                            cur_rep_count = df_sheet['NumProductions'].str.count('4.0', re.UNICODE).sum()                            
                            sheet_rep_dict[u'ortho x 4'] += cur_rep_count                                
                            cur_rep_count = df_sheet['NumProductions'].str.count('5.0', re.UNICODE).sum()                            
                            sheet_rep_dict[u'ortho x 5'] += cur_rep_count   
                                                                                    
                            # Multiply orthography instances by number of productions
                            
                            df_sheet['Orthography'] = df_sheet['Word']
                            mask = df_sheet.filter(['Orthography',col,'NumProductions'], axis=1).NumProductions == '2.0'                            
                            df_sheet.loc[mask, 'Orthography'] = df_sheet.loc[mask, 'Orthography']+' '+df_sheet.loc[mask, 'Orthography']                            
                            mask = df_sheet.filter(['Orthography',col,'NumProductions'], axis=1).NumProductions == '3.0'                            
                            df_sheet.loc[mask, 'Orthography'] = df_sheet.loc[mask, 'Orthography']+' '+df_sheet.loc[mask, 'Orthography']+' '+df_sheet.loc[mask, 'Orthography']                             
                            mask = df_sheet.filter(['Orthography',col,'NumProductions'], axis=1).NumProductions == '4.0'                            
                            df_sheet.loc[mask, 'Orthography'] = df_sheet.loc[mask, 'Orthography']+' '+df_sheet.loc[mask, 'Orthography']+' '+df_sheet.loc[mask, 'Orthography']+' '+df_sheet.loc[mask, 'Orthography']
                            mask = df_sheet.filter(['Orthography',col,'NumProductions'], axis=1).NumProductions == '5.0'                            
                            df_sheet.loc[mask, 'Orthography'] = df_sheet.loc[mask, 'Orthography']+' '+df_sheet.loc[mask, 'Orthography']+' '+df_sheet.loc[mask, 'Orthography']+' '+df_sheet.loc[mask, 'Orthography']\
                            +' \ '+df_sheet.loc[mask, 'Orthography']
                            
                            # Multiply IPA Target instances by number of productions
                            
                            df_sheet['IPA Target_dup'] = df_sheet['IPA Target']
                            mask = df_sheet.filter(['IPA Target_dup',col,'NumProductions'], axis=1).NumProductions == '2.0'                            
                            df_sheet.loc[mask, 'IPA Target_dup'] = df_sheet.loc[mask, 'IPA Target_dup']+' '+df_sheet.loc[mask, 'IPA Target_dup']                            
                            mask = df_sheet.filter(['IPA Target_dup',col,'NumProductions'], axis=1).NumProductions == '3.0'                            
                            df_sheet.loc[mask, 'IPA Target_dup'] = df_sheet.loc[mask, 'IPA Target_dup']+' '+df_sheet.loc[mask, 'IPA Target_dup']+' '+df_sheet.loc[mask, 'IPA Target_dup']                             
                            mask = df_sheet.filter(['IPA Target_dup',col,'NumProductions'], axis=1).NumProductions == '4.0'                            
                            df_sheet.loc[mask, 'IPA Target_dup'] = df_sheet.loc[mask, 'IPA Target_dup']+' '+df_sheet.loc[mask, 'IPA Target_dup']+' '+df_sheet.loc[mask, 'IPA Target_dup']+' '+df_sheet.loc[mask, 'IPA Target_dup']
                            mask = df_sheet.filter(['IPA Target_dup',col,'NumProductions'], axis=1).NumProductions == '5.0'                            
                            df_sheet.loc[mask, 'IPA Target_dup'] = df_sheet.loc[mask, 'IPA Target_dup']+' '+df_sheet.loc[mask, 'IPA Target_dup']+' '+df_sheet.loc[mask, 'IPA Target_dup']+' '+df_sheet.loc[mask, 'IPA Target_dup']\
                            +' \ '+df_sheet.loc[mask, 'IPA Target_dup']                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                                                                                                                               
                            # Create DataFrame Series from replace counts for current column/probe administration
                            probe_counts = pd.Series(sheet_rep_dict)
                            # Add current column Series replace counts to DataFrame of counts for this participant
                            df_replace_counts[col] = probe_counts
                            df_replace_counts.rename(columns={col:name+' '+col}, inplace=True)
                            print(name, col, 'column complete.')
                            
                            ## Save CSV of transcription data for current probe administration
                            # Change to new subdirectory
                            #raise Exception
                            with change_dir(os.path.join(cwd)):                                 
                                # Create new subdirectory to place csv files
                                try:
                                    os.makedirs(os.path.join('csv'))
                                    print('Created:', os.path.join(os.getcwd(),'csv'))
                                except WindowsError:
                                    print('saving to csv directory')
                                # Change to new subdirectory
                                with change_dir(os.path.join(cwd, 'csv')):                                
                                    df_sheet.filter(['Target','Orthography','IPA Target_dup', col, 'DI', 'Notes', 'NumProductions','Speaker', 'CA', 'Probe', 'Session'], axis=1).rename(columns={'IPA Target_dup':'IPA Target', col:'IPA Actual'}).to_csv(name + '_' + sheet + '_' + col + '.csv', encoding = 'utf-8', index = False)        
            print(name,sheet, "Done")
        print(name, "Done")     
    print("All files in directory complete")
                            
    ## Save CSV of replacement counts
    # Change to new subdirectory
    with change_dir(os.path.join(cwd)):                                 
        # Create new subdirectory to place csv files
        try:
            os.makedirs('info')
            print('Created:', os.path.join(os.getcwd(),'info'))
        except WindowsError:
            print('info directory already created.')
        # Change to new subdirectory
        with change_dir(os.path.join(cwd, 'info')):                                            
                df_replace_counts.T.to_csv('replacement_counts.csv', encoding = 'utf-8')
    print('replacement_counts.csv created')
                            
    ### Other features to implement in future:                     
    # Add info from notes_dict to participant metadata/phon corpus, CA
    # Add CA from CA_Dict to session metadata
    # If participant_num in notes_dict, insert dictionary entry to notes Tier. Also add to corpus notes
    # Check for errors against illegal characters key. Search for illegal characters in DataFrame. Create error log                                                                                                                                                                                                                                                                                    
    
    # Create csv of unique orthography items
    with change_dir(os.path.join(cwd)):                                 
        # Create new subdirectory to place csv file
        try:
            os.makedirs('info')
            print('Created:', os.path.join(os.getcwd(),'info'))
        except WindowsError:
            print('info/{} directory already created.'.format(name))
        # Change to new subdirectory
        with change_dir(os.path.join(cwd, 'info')):                                            
                pd.DataFrame(word_list).to_csv('word_list.csv', header = ['Orthography'], 
                            encoding = 'utf-8', index = False)
    print('word_list.csv created')    


