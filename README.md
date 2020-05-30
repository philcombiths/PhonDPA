## Phon DPA Script
Phon_DPA is a python script which converts raw data in Excel (xls) from the Developmental Phonologies Archive (Gierut, 2015)
into Phon-readable comma-separated value (csv) files. This conversion is done as faithfully as possible to the original transcriptions, although some diacritic detail is not compatible with Phon and was adapted as follows:

- For diacritic symbols incompatible with Phon, the closest symbol was used, followed by ̾
- For lengthened superscript symbols, the diacritic is followed by ͒
- Superscript ʌ is replaced with superscript ə
- Superscript [a, e, i, o, u, v] are represented with diacritics above the segment. All others are adjacent to the segment.

# Version History
*******************
1.2 [1.8.18]
dpa_script_v1-2.py

- Orthography of diminutive forms changed from ' i' to '-i'.
- IPA Target for telephone corrected from 'ˈtɛləˌfocn' to 'ˈtɛləˌfoʊn'
- PhonSessions moved into Corpus folders by participant number
- Pre Probes Corpus added. Includes all GFTA, OCP, CCP, PKP probes at 'Pre' timepoint only.
- PKP Pre Corpus added (by 1000s)

*******************
1.3.0 (deprecated dipthong ligature version) [1.12.18]
dpa_script_v1-3.py

- NR and ɴʀ removed from IPA Actual column, replaced with "No response" in Notes
- Find/replace added [other_chars_translate_dict.csv] for dipthongs in IPA Actual so all instances have ligature ͡  (better alignment in Phon)
- Manual find/replace in [target_dict.csv] to add ligature ͡  to IPA Target transcriptions

*******************
1.3.1 [1.17.2018]
dpa_script_v1-3.py

same as above (no change to script v1-3), but target_dict.csv and other_chars_translate_dict.csv reverted to prior version without ligatures for diphthongs.
- NR and ɴʀ removed from IPA Actual column, replaced with "No response" in Notes

*******************
1.4 [1.27.2018]
dpa_script_v1-3.py

- Added superscript_chars_initial_2 and superscript_chars_initial_3 to repeat find-and-replace for initial raised segments (to capture instances where multiple raised segments occur word-initially. Modifications were made to these repeated versions to this aim.
- superscript_chars_initial and superscript_chars_noninitial changed to OrderedDict to preserve original key order.
- Shell output edited for accuracy and readability
- Unused code removed for readability
- Dictionary edits: superscript_chars_initial and superscript_chars_noninitial dicts changed to convert all diacritics to Phon-compatible symbols
	Details:
	- For diacritic symbols incompatible with Phon, the closest symbol was used, followed by ̾
	- For lengthened superscript symbols, the diacritic is followed by ͒
	- Superscript ʌ is replaced with superscript ə
	- Initial diacritics (except nasals) are followed by ̵  to attach to the left of the modified segment
	- Non-initial nasal diacritics are followed by ̵  to attach to the right of the modified segment
	- [a, e, i, o, u, v] are represented with diacritics above the segment. All others are adjacent to the segment.
- Additional fixes in OrderedDicts:  
	1. Fix lengthening of initial superscript:
		Find: (?<=^̂.)(ː)
		Find: (?<=\ŝ.)(ː)
		Find: (?<=^̂.[̴̡̪̥̩̜̰͔̊͋̄̈̚̕˭̣̃˺])(ː)
		Find: (?<=\ŝ.[̴̡̪̥̩̜̰͔̊͋̄̈̚̕˭̣̃˺])(ː)
		Replace: 
	2. Fix diacritic on initial superscript:
		Find: (?:^|\s)̂(X)([̴̡̪̥̩̜̰͔̊͋̄̈̚̕˭̣̃˺]*)
		Replace: Y\1̵
	3. Add fermata to list of recognized diacritics in regex initial searches
	4. Add combining right half ring below  ̹  in regex initial searches
	5. Edit regex for initial upper segments placing upper segments after the segment they modify
		Find: (?:^|\s)(?:̂v)([̴̡̪̥̩̜̰͔͒̊͋̄̈̚̕˭̣̃˺]*)(.)
		Replace: \2ͮ\1
	6. Fix R-aligned superscript nasals on noninitial superscript:
		Find: (?<!^)ⁿ
		Replace: ⁿ̵

*******************
1.5 [in progress] Latest version available on GitHub
dpa_script.py


# Disclaimer
Phon_DPA was created by Philip Combiths, Jessica Barlow, and the Phonological Typologies Lab at San Diego State University.


Archival data were retrieved from the Gierut / Learnability Project collection of the IUScholarWorks repository at https://scholarworks.iu.edu/dspace/handle/2022/20061 The archival data were original to the Learnability Project and supported by grants from the National Institutes of Health to Indiana University (DC00433, RR7031K, DC00076, DC001694; PI: Gierut). The views expressed herein do not represent those of the National Institutes of Health, Indiana University, or the Learnability Project. The author(s) assume(s) sole responsibility for any errors, modifications, misapplications, or misinterpretations that may have been introduced in extraction or use of the archival data.
