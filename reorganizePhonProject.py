"""
With a specified Phon Project directory containing at least one corpus,
generates new corpora and filters Phon sessions into those corpora
based on specified keywords and filter words.

This generates new corpora folders. Does NOT modify original corpora folders.

reorganizePhonProject is the most current function.

Designed for use with DPA Project

@author: Philip Combiths
@created: 2020-11-25
@modified: 2023-06-16
"""

import fnmatch
import os
import os.path
import re
import shutil
from contextlib import contextmanager

# ------------------------------------------------------------------------------


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


def derive_corpus(
    session_directory, corpus_filter, session_filter, pre_select=1, post_select=0
):
    with change_dir(session_directory):
        parent_directory = os.path.dirname(session_directory)
        if "project.xml" not in os.listdir(parent_directory):
            raise FileNotFoundError("project.xml not found in parent project directory")
        if pre_select == 1:
            exclude_pre_list = [
                e for e in os.listdir(session_directory) if re.search(r"Pre\s?\d", e)
            ]
        if pre_select == 2:
            multi_pre_list = [
                e for e in os.listdir(session_directory) if re.search(r"Pre\s?\d", e)
            ]
            exclude_pre_list = [e.replace(" 2", "") for e in multi_pre_list]
        if post_select == 1:
            exclude_post_list = [
                e for e in os.listdir(session_directory) if re.search(r"Post\s?II", e)
            ]
        if post_select == 2:
            multi_post_list = [
                e for e in os.listdir(session_directory) if re.search(r"Post\s?II", e)
            ]
            exclude_post_list = [e.replace(" II", "") for e in multi_post_list]
        # Create corpus folders
        for corpus in corpus_filter:
            try:
                os.mkdir(os.path.join(parent_directory, corpus))
            except FileExistsError:
                print(f"{corpus} directory already exists. Adding to folder")
        # Organize all files
        for e in os.listdir(session_directory):
            assert os.path.isfile(e), "Error: Subdirectory found."
            for corpus in corpus_filter:
                # Don't copy original Pre files when later pre files exist
                if pre_select > 0:
                    if e in exclude_pre_list:
                        continue
                if post_select > 0:
                    if e in exclude_post_list:
                        continue
                if fnmatch.fnmatch(e, "*" + corpus + "*"):
                    for key in session_filter:
                        if fnmatch.fnmatch(e, "*" + key + "*"):
                            shutil.copy(e, os.path.join(parent_directory, corpus, e))

                        else:
                            continue
                else:
                    continue

    return


# Examples
# reorganizePhonProject('DPA 3.0 - Original - Copy', ['Pre', 'Post'], ['PKP', 'OCP', 'CCP'])
# reorganizePhonProject('DPA 3.0 - Original - Copy', filterKey=['PKP', 'GFTA'])
# reorganizePhonProject('/Users/pcombiths/Documents/DPA v1_4 all 2', filterKey=['PKP'])

derive_corpus(
    "/Users/pcombiths/Documents/DPA v1_4 all 2/Data",
    ["Pre", "Post"],
    ["PKP", "OCP", "CCP", "GFTA"],
    pre_select=1,
    post_select=0,
)

### ToDo
# Output to a new Phon project, rather than inside the same directory
# Accept input from a Phon base project, rather than a corpus folder
# Allow organizing/filtering by multiple layers
