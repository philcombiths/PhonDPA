# Simple script to open and merge all csv files in a single folder into a single
# csv file. 
### Note: Files must have same header structure
### Note: Cannot set output directory to same folder as input directory

import io
import shutil
import glob
import csv
import os

#import csv files from folder specified below
path = os.path.normpath(input('Input CSV directory'))

# save combined Master csv to folder specified below
Master_path = os.path.normpath(input('Input combined CSV output directory')) 

assert path != Master_path, "Cannot set output directory to same folder as input directory"

allFiles = glob.glob(path + "/*.csv")
with io.open(Master_path+r'/'+path.split('\\')[-1]+'.csv', 'wb') as outfile:
    print (outfile)
    for i, fname in enumerate(glob.glob(path + "\*.csv")):
        with io.open(fname, 'rb') as infile:
            if i != 0:
                infile.readline()  # Throw away header on all but first file
            # Block copy rest of file from input to output without parsing
            shutil.copyfileobj(infile, outfile)C:\Users\Philip\test1
            print(fname + " has been imported.")
    csv.writer(outfile)

    

