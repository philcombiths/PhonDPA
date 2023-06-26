"""
With a specified Phon Project directory containing at least one corpus,
generates new corpora and filters Phon sessions into those corpora
based on specified keywords and filter words.

This generates new corpora folders. Does NOT modify original corpora folders.

organize_project() is the most current function for automatic organization by participant number.


Designed for use with DPA Project.

pre_select: This option determines how the function handles files with "Pre" in their names. It can take the following values:
0: No action is taken regarding "Pre" files. All Pre files are incldued
1: If any "Pre 2" files exist in the session_directory, they will be excluded from being copied to the corpus folders.
2: If any "Pre 2" files exist in the session_directory, they will be renamed "Pre" and included. The original "Pre" file is excluded (i.e. replaced)
The purpose of the pre_select option is to handle scenarios where there are multiple versions of "Pre" files and control whether they should be included in the corpus or not.

post_select: This option determines how the function handles files with "Post II" in their names. It can take the following values:
0: No action is taken regarding "Post II" files. All Post files are included.
1: If any "Post II" files exist in the session_directory, they will be excluded from being copied to the corpus folders.
2: If any "Post II" files exist in the session_directory, they will be renamed as "Post" and included. The original "Post" file is excluded.
The purpose of the post_select option is to handle scenarios where there are multiple versions of "Post II" files and control whether they should be included in the corpus or not.

@author: Philip Combiths
@created: 2020-11-25
@modified: 2023-06-26
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


# Helper function for organize_corpus()
def organize_files_by_regex(project_directory, keyword):
    """Create a new corpus filtered to one of 1000s, 2000s, 3000s, etc.

    Args:
        keyword (_type_): Single digit to specify sessions. Example: (1)000s, (2)000s.

    Returns:
        STR: String of corpus name.
    """
    # Working in corpus folder
    projectDir = project_directory
    PhonDir = os.path.dirname(projectDir)
    # Create the new corpus name based on the keyword
    newCorpusName = keyword + "000s"
    newCorpusDir = os.path.join(projectDir, newCorpusName)

    try:
        os.mkdir(newCorpusDir)
    except FileExistsError:
        print(f"{newCorpusName} directory already exists. Adding to folder")

    # Iterate over files in the current directory
    for File in os.listdir(project_directory):
        file_path = os.path.join(project_directory, File)
        reg_exp = re.compile(keyword + r"\d{3}")
        # If the name of the file contains a keyword
        if re.search(reg_exp, File):
            # If the file is truly a file...
            if os.path.isfile(file_path):
                try:
                    shutil.copy(file_path, newCorpusDir)
                    print(f"{File} Copied to {newCorpusName} Directory")
                except shutil.SameFileError:
                    print(f"{File} already exists. Not copied")
                    continue
    return newCorpusName


# Helper function for organize_corpus()
def organize():
    """
    Creates new corpora in the current folder based on groups of participant
    numbers (1000s, 2000s, etc.).

    Returns:
        list: A list of corpus names created based on participant numbers.
    """

    corpusNames = []
    for keyword in range(1, 10):
        keyword = str(keyword)
        corpusNames.append(organize_files_by_regex(keyword))
        # Calls the helper function 'organize_files_by_regex' for each participant number keyword
        # Appends the returned corpus name to the 'corpusNames' list
    return corpusNames
    # Returns the list of corpus names created based on participant numbers


# Use this function to organize a corpusby 1000s, 2000s, etc.
def organize_corpus(corpus_directory):
    corpusNames = []
    for keyword in range(1, 10):
        keyword = str(keyword)
        corpusNames.append(organize_files_by_regex(corpus_directory, keyword))
    return


# Use this function to filter and organize an entire project by keyword lists
def derive_project(
    session_directory, corpus_filter, session_filter, pre_select=1, post_select=0
):
    """
    Derives a project based on the given filters.

    Args:
        session_directory (str): The directory path of the session.
        corpus_filter (list): A list of corpus filters. Sessions will be organized into these corpora folders.
        session_filter (list): A list of session filters. Only filtered sessions will be included.
        pre_select (int, optional): The pre-select option. Defaults to 1.
        post_select (int, optional): The post-select option. Defaults to 0.

    Raises:
        FileNotFoundError: Raised when 'project.xml' is not found in the parent project directory.
    """
    # Change to the session directory
    with change_dir(session_directory):
        # Get the parent directory of the session directory
        parent_directory = os.path.dirname(session_directory)

        # Check if 'project.xml' exists in the parent directory
        if "project.xml" not in os.listdir(parent_directory):
            raise FileNotFoundError("project.xml not found in parent project directory")

        # Determine excluded 'Pre' files based on the pre-select option
        if pre_select == 1:
            # Exclude 'Pre' files with a single digit
            exclude_pre_list = [
                e for e in os.listdir(session_directory) if re.search(r"Pre\s?\d", e)
            ]
        if pre_select == 2:
            # Exclude 'Pre' files with a single digit and rename files with ' 2' suffix
            multi_pre_list = [
                e for e in os.listdir(session_directory) if re.search(r"Pre\s?\d", e)
            ]
            exclude_pre_list = [e.replace(" 2", "") for e in multi_pre_list]

        # Determine excluded 'Post' files based on the post-select option
        if post_select == 1:
            # Exclude 'Post II' files
            exclude_post_list = [
                e for e in os.listdir(session_directory) if re.search(r"Post\s?II", e)
            ]
        if post_select == 2:
            # Exclude 'Post II' files and remove ' II' suffix
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
                # Don't include excluded Pre files specified by pre-select option
                if pre_select > 0:
                    if e in exclude_pre_list:
                        continue
                # Don't include excluded Post files specified by pre-select option
                if post_select > 0:
                    if e in exclude_post_list:
                        continue
                # Copy the file to the appropriate corpus folder if it matches the filters
                if fnmatch.fnmatch(e, "*" + corpus + "*"):
                    for key in session_filter:
                        if fnmatch.fnmatch(e, "*" + key + "*"):
                            shutil.copy(e, os.path.join(parent_directory, corpus, e))

                        else:
                            continue
                else:
                    continue

    return


## Input must be a PROJECT folder
# derive_project(
#     r"R:\Admin\Alt Workspace\DPA v1_4 all - Copy",
#     ["Pre", "Post"],
#     ["PKP", "OCP", "CCP", "GFTA"],
#     pre_select=1,
#     post_select=0,
# )

## The directory path given here must a CORPUS directory (Phon sessions inside)
organize_corpus(r"R:\Admin\Alt Workspace\DPA v1_6_PrePost\Pre")

### ToDo
# Output to a new Phon project, rather than inside the same directory
# Accept input from a Phon base project, rather than a corpus folder
# Allow organizing/filtering by multiple layers
