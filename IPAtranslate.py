# -*- coding: utf-8 -*-
"""
Modification/addition to code created by Mark Hasegawa-Johnson @jhasegaw
Purpose: From a directory containing text files, translate symbols in 
         each text file to/from IPA/X-SAMPA and save as new txt
         file (filename appended with new symbol type).
         
Usage Instructions:
    In console, execute translateFiles().
        In fx, you may specify parameter permittedExts (list of extensions to include).
            default = ['.txt', '.csv']
        In fx, you may specify parameter translateTo ('xsampa' or 'ipa')
            default = 'xsampa'
    When prompted, enter directory of text files to translate.

"""

import re

###############################################################
# X-SAMPA / IPA conversion dictionaries and translation functions
# created by Mark Hasegawa-Johnson @jhasegaw

_xsampa2ipa = {
    k:re.sub(r'◌','',v) for (k,v) in {
        '#':'#',
        '=':'◌̩',
        '>':'◌ʼ',
        '`':'◌˞',
        '~':'◌̃',
        'a':'a',
        'b':'b',
        'b_<':'ɓ',
        'c':'c',
        'd':'d',
        'd`':'ɖ',
        'd_<':'ɗ',
        'e':'e',
        'f':'f',
        'g':'ɡ',
        'g_<':'ɠ',
        'h':'h',
        'h\\':'ɦ',
        'i':'i',
        'j':'j',
        'j\\':'ʝ',
        'k':'k',
        'l':'l',
        'l`':'ɭ',
        'l\\':'ɺ',
        'm':'m',
        'n':'n',
        'n_d':'nd',
        'n`':'ɳ',
        'o':'o',
        'p':'p',
        'p\\':'ɸ',
        'p_<':'ɓ̥',
        'q':'q',
        'r':'r',
        'r`':'ɽ',
        'r\\':'ɹ',
        'r\\`':'ɻ',
        's':'s',
        's`':'ʂ',
        's\\':'ɕ',
        't':'t',
        't`':'ʈ',
        'u':'u',
        'v':'v',
        'v\\':'ʋ',
        'w':'w',
        'x':'x',
        'x\\':'ɧ',
        'y':'y',
        'z':'z',
        'z`':'ʐ',
        'z\\':'ʑ',
        'A':'ɑ',
        'B':'β',
        'B\\':'ʙ',
        'C':'ç',
        'D':'ð',
        'E':'ɛ',
        'F':'ɱ',
        'G':'ɣ',
        'G\\':'ɢ',
        'G\\_<':'ʛ',
        'H':'ɥ',
        'H\\':'ʜ',
        'I':'ɪ',
        'I\\':'ɪ̈ ',
        'J':'ɲ',
        'J\\':'ɟ',
        'J\\_<':'ʄ',
        'K':'ɬ',
        'K\\':'ɮ',
        'L':'ʎ',
        'L\\':'ʟ',
        'M':'ɯ',
        'M\\':'ɰ',
        'N':'ŋ',
        'N_g':'ŋɡ',
        'N\\':'ɴ',
        'O':'ɔ',
        'O\\':'ʘ',
        'P':'ʋ',
        'Q':'ɒ',
        'R':'ʁ',
        'R\\':'ʀ',
        'S':'ʃ',
        'T':'θ',
        'U':'ʊ',
        'U\\':'ʊ̈ ',
        'V':'ʌ',
        'W':'ʍ',
        'X':'χ',
        'X\\':'ħ',
        'Y':'ʏ',
        'Z':'ʒ',
        '.':'.',
        '"':'ˈ',
        '%':'ˌ',
        '\'':'ʲ',
        ':':'ː',
        ':\\':'ˑ',
        '-':'',
        '@':'ə',
        '@\\':'ɘ',
        '{':'æ',
        '}':'ʉ',
        '1':'ɨ',
        '2':'ø',
        '3':'ɜ',
        '3\\':'ɞ',
        '4':'ɾ',
        '5':'ɫ',
        '6':'ɐ',
        '7':'ɤ',
        '8':'ɵ',
        '9':'œ',
        '&':'ɶ',
        '?':'ʔ',
        '?\\':'ʕ',
        '*':'',
        '/':'',
        '<\\':'ʢ',
        '>\\':'ʡ',
        '^':'ꜛ',
        '!':'ꜜ',
        '!\\':'ǃ',
        '|':'|',
        '|\\':'ǀ',
        '||':'‖',
        '|\\|\\':'ǁ',
        '=\\':'ǂ',
        '-\\':'‿'
    }.items()
}

_xsampa_vowels=set('aeiouyAEIOUYQV@123}{6789&')|set(('I\\','U\\','@\\','3\\'))

_xdiacritics2ipa = {
    k:re.sub(r'◌','',v) for (k,v) in {
        '"':'◌̈',
        '+':'◌̟',
        '-':'◌̠',
        '/':'◌̌',
        '0':'◌̥',
        '=':'◌̩',
        '>':'◌ʼ',
        '?\\':'◌ˤ',
        '\\':'◌̂',
        '^':'◌̯',
        '}':'◌̚',
        '`':'◌˞',
        '~':'◌̃',
        'A':'◌̘',
        'a':'◌̺',
        'B':'◌̏',
        'B_L':'◌᷅',
        'c':'◌̜',
        'd':'◌̪',
        'e':'◌̴',
        'F':'◌̂',
        'G':'◌ˠ',
        'H':'◌́',
        'H_T':'◌᷄',
        'h':'◌ʰ',
        'j':'◌ʲ',
        'k':'◌̰',
        'L':'◌̀',
        'l':'◌ˡ',
        'M':'◌̄',
        'm':'◌̻',
        'N':'◌̼',
        'n':'◌ⁿ',
        'O':'◌̹',
        'o':'◌̞',
        'q':'◌̙',
        'R':'◌̌',
        'R_F':'◌᷈',
        'r':'◌̝',
        'T':'◌̋',
        't':'◌̤',
        'v':'◌̬',
        'w':'◌ʷ',
        'X':'◌̆',
        'x':'◌̽',
        '1':'˥',
        '2':'˦',
        '3':'˧',
        '4':'˨',
        '5':'˩',
    }.items()
}

# Create and _xsampa2ipa with '_'+k for each diacritic
_xsampa_and_diac2ipa = _xsampa2ipa.copy()
_xsampa_and_diac2ipa.update({ ('_'+k):v for (k,v) in _xdiacritics2ipa.items() })

_ipa2xsampa = { v:k for (k,v) in _xsampa_and_diac2ipa.items() }



def translate_string(s, d):
    '''(tl,ttf)=translate_string(s,d):
    Translate the string, s, using symbols from dict, d, as:
    1. Min # untranslatable symbols, then 2. Min # symbols.
    tl = list of translated or untranslated symbols.
    ttf[n] = True if tl[n] was translated, else ttf[n]=False.
'''
    N = len(s)
    symcost = 1    # path cost per translated symbol
    oovcost = 10   # path cost per untranslatable symbol
    maxsym = max(len(k) for k in d.keys())  # max input symbol length
    # (pathcost to s[(n-m):n], n-m, translation[s[(n-m):m]], True/False)
    lattice = [ (0,0,'',True) ]
    for n in range(1,N+1):
        # Initialize on the assumption that s[n-1] is untranslatable
        lattice.append((oovcost+lattice[n-1][0],n-1,s[(n-1):n],False))
        # Search for translatable sequences s[(n-m):n], and keep the best
        for m in range(1,min(n+1,maxsym+1)):
            if s[(n-m):n] in d and symcost+lattice[n-m][0] < lattice[n][0]:
                lattice[n] = (symcost+lattice[n-m][0],n-m,d[s[(n-m):n]],True)
    # Back-trace
    tl = []
    translated = []
    n = N
    while n > 0:
        tl.append(lattice[n][2])
        translated.append(lattice[n][3])
        n = lattice[n][1]
    return((tl[::-1], translated[::-1]))
    
# X-SAMPA
def ipa2xsampa(x,language):
    '''Attempt to return X-SAMPA equivalent of an IPA phone x.'''
    (tl,ttf) = translate_string(x, _ipa2xsampa)
    return(''.join(tl))

def xsampa2ipa(x,language):
    '''Return the IPA equivalent of X-SAMPA phone x.'''
    (tl,ttf) = translate_string(x, _xsampa_and_diac2ipa)
    return(''.join(tl))


###############################################################
# Use translation functions to revise a directory of text files

import io
import os
from contextlib import contextmanager

@contextmanager
def change_dir(newdir):
    prevdir = os.getcwd()
    try:
        yield os.chdir(os.path.expanduser(newdir)) 
    finally:
        os.chdir(prevdir)




def translateFiles(permittedExts=['.txt', '.csv'], 
                   transTo='xsampa'):
    
    """
    From a directory containing text files, translate symbols in 
    each text file to/from IPA/X-SAMPA and save as new txt
    file (filename appended with _REV).
    """
    
    dirPath = input("Enter directory of text files to translate: ")
    
    if transTo == 'xsampa':
        transType = '_ipa2xsampa'
    if transTo == 'ipa':
        transType = '_xsampa_and_diac2ipa'
    
    # Translate each file with permitted extension in directory
    with change_dir(dirPath):
        for fname in os.listdir(os.getcwd()):
            if fname.endswith(tuple(permittedExts)):
                translateFile(os.path.abspath(fname), transType)
        
        # generate IPA/XSAMPA key
        with io.open(dirPath+'\\IPA_XSAMPA_key.txt', 'a', encoding='utf-8') as outfile:
            for transPair in _ipa2xsampa.items():
                outfile.write(f"{transPair[0]},{transPair[1]}\n")
                
    
def translateFile(fpath, transType):
    
    """
    Translate symbols in a text file to/from IPA/X-SAMPA and save as new txt
    file (filename appended with new symbol type).
    """
    
    with io.open(fpath, 'r', encoding = 'utf-8') as infile:
        fstr = infile.read()
        fext= fpath.split('.')[-1]
        fname = fpath.split('.')[-2].split('\\')[-1]
        fpathNoExt = '\\'.join(fpath.split('.')[-2].split('\\'))
        
        if transType == '_ipa2xsampa':
            fstr_REV = ipa2xsampa(fstr, transType)
        if transType == '_xsampa_and_diac2ipa':
            fstr_REV = xsampa2ipa(fstr, transType)
    
    if transType == '_ipa2xsampa':    
        with io.open(fpathNoExt + '_XSAMPA.' + fext, 'w', encoding = 'utf-8') as outfile:
            outfile.write(fstr_REV)
    if transType == '_xsampa_and_diac2ipa':
        with io.open(fpathNoExt + '_IPA.' + fext, 'w', encoding = 'utf-8') as outfile:
            outfile.write(fstr_REV)
            
            
def translateStr(string, transTo):
    if transTo == 'ipa':
        return xsampa2ipa(string, '_xsampa_and_diac2ipa')
    if transTo == 'xsampa':
        return ipa2xsampa(string, '_ipa2xsampa')
