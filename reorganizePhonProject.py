"""
With a specified Phon Project directory containing at least one corpus,
generates new corpora and filters Phon sessions into those corpora
based on specified keywords and filter words.

This generates new corpora folders. Does NOT modify original corpora folders.

reorganizePhonProject is the most current function.

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


def organize_files_by_keyword(keyword):
    """
    Creates a new corpus filtered to session names containing the specified keyword.

    Args:
        keyword (str): String to use as the corpus name and session filter.

    Returns:
        tuple: A tuple containing the PhonDir (parent directory of the project) and the newCorpusDir (path to the created corpus directory).
    """
    # Working in corpus folder
    projectDir = os.path.dirname(os.getcwd())
    PhonDir = os.path.dirname(projectDir)
    newCorpusDir = os.path.join(projectDir, keyword)

    # Create new corpus folder from keyword
    try:
        os.mkdir(newCorpusDir)
    except FileExistsError:
        print(f"{keyword} directory already exists. Adding to folder")

    for File in os.listdir():
        # If the name of the file contains a keyword
        if fnmatch.fnmatch(File, "*" + keyword + "*"):
            print(f"{File} Copied to {keyword} Directory")
            # If the file is truly a file...
            if os.path.isfile(File):
                # Copy that file to the new corpus directory
                try:
                    shutil.copy(File, newCorpusDir)
                except shutil.SameFileError:
                    continue

    return PhonDir, newCorpusDir


def organize_files_by_regex(keyword):
    """Create a new corpus filtered to one of 1000s, 2000s, 3000s, etc.

    Args:
        keyword (_type_): Single digit to specify sessions. Example: (1)000s, (2)000s.

    Returns:
        STR: String of corpus name.
    """
    # Working in corpus folder
    projectDir = os.path.dirname(os.getcwd())
    PhonDir = os.path.dirname(projectDir)
    # Create the new corpus name based on the keyword
    newCorpusName = keyword + "000s"
    newCorpusDir = os.path.join(projectDir, newCorpusName)

    try:
        os.mkdir(newCorpusDir)
    except FileExistsError:
        print(f"{newCorpusName} directory already exists. Adding to folder")

    # Iterate over files in the current directory
    for File in os.listdir():
        reg_exp = re.compile(keyword + r"\d{3}")
        # If the name of the file contains a keyword
        if re.search(reg_exp, File):
            print(f"{File} Copied to {newCorpusName} Directory")
            # If the file is truly a file...
            if os.path.isfile(File):
                try:
                    shutil.copy(File, newCorpusDir)
                except shutil.SameFileError:
                    continue
    return newCorpusName


def organize(corpusKey=None):
    """
    Creates new corpora based on groups of participant numbers or a specified keyword.

    Args:
        corpusKey (str or list, optional): String or list of strings to use as corpus name(s) and session filter(s).
            If not specified (None), sessions are grouped into corpora based on participant numbers (e.g., 1000s, 2000s, 3000s).
            If a single string is provided, files containing the specified keyword will be organized into a corpus.
            If a list of strings is provided, files containing any of the specified keywords will be organized into separate corpora.
            Defaults to None.

    Returns:
        None or list: If corpusKey is None, it returns a list of corpus names created based on participant numbers.
            If corpusKey is specified, it returns None.
    """

    if corpusKey == None:
        # If no corpusKey is specified, sessions are grouped in corpora
        # based on participant number (e.g., 1000s, 2000s, 3000s)
        # This saves into the same folder as the current corpus.
        corpusNames = []
        for keyword in range(1, 10):
            keyword = str(keyword)
            corpusNames.append(organize_files_by_regex(keyword))
            # Calls the helper function 'organize_files_by_regex' for each participant number keyword
            # Appends the returned corpus name to the 'corpusNames' list

        return corpusNames
        # Returns the list of corpus names created based on participant numbers

    # Organize into corpora by keyword(s)
    else:
        if isinstance(corpusKey, str):
            organize_files_by_keyword(corpusKey)
            # Calls the helper function 'organize_files_by_keyword' with the provided keyword
        else:
            for corpus in corpusKey:
                organize_files_by_keyword(corpus)
                # Calls the helper function 'organize_files_by_keyword' for each keyword in the provided list

        return


corpusNames = []
for keyword in range(1, 10):
    keyword = str(keyword)
    corpusNames.append(organize_files_by_regex(keyword))


# Working in corpus folder
projectDir = os.path.dirname(os.getcwd())
PhonDir = os.path.dirname(projectDir)
newCorpusDir = os.path.join(projectDir, keyword)

# Create new corpus folder from keyword


def organize_project(project_directory):
    with change_dir(os.path.normpath(projectDir)):
        for f in os.listdir():
            if os.path.isdir(f):
                # Enter corpus folder(s)
                with enter_dir(f):
                    for corpus_name in corpusNames:
                        try:
                            os.mkdir(newCorpusDir)
                        except FileExistsError:
                            print(
                                f"{keyword} directory already exists. Adding to folder"
                            )

                        for File in os.listdir():
                            # If the name of the file contains a keyword
                            if fnmatch.fnmatch(File, "*" + keyword + "*"):
                                print(f"{File} Copied to {keyword} Directory")
                                # If the file is truly a file...
                                if os.path.isfile(File):
                                    # Copy that file to the new corpus directory
                                    try:
                                        shutil.copy(File, newCorpusDir)
                                    except shutil.SameFileError:
                                        continue

    return


def reorganizePhonProject(projectDir, corpusKey=None, filterKey=None):
    """_summary_

    Args:
        projectDir (_type_): _description_
        corpusKey (_type_, optional): _description_. Defaults to None.
        filterKey (_type_, optional): _description_. Defaults to None.
    """
    with change_dir(os.path.normpath(projectDir)):
        assert (
            "project.xml" in os.listdir()
        ), "project.xml not found in project directory"

        # First sorting pass. Organize in participant number buckets.
        for f in os.listdir():
            if os.path.isdir(f):
                # Enter corpus folder(s)
                with enter_dir(f):
                    if corpusKey == None:
                        corpusKey = organize(corpusKey)
                    else:
                        organize(corpusKey)
        # Second filter pass. Filter by filterKey.
        if filterKey != None:
            for corpus in corpusKey:
                with enter_dir(corpus):
                    print(f"Deleting {corpus} sessions not in filterKey...")
                    for f in os.listdir():
                        if any(
                            [fnmatch.fnmatch(f, "*" + fil + "*") for fil in filterKey]
                        ):
                            continue
                        else:
                            # Check if file exists:
                            if os.path.isfile(f):
                                os.remove(f)
                            else:
                                print(f"ERROR: {f} Not found in {corpus} Directory")

                    print(
                        f"{len(os.listdir())} Phon sessions copied to {corpus} corpus."
                    )

    return


def derive_corpus(
    session_directory, corpus_filter, session_filter, pre_select=1, post_select=0
):
    """
    Derives a corpus based on the given filters.

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


# derive_corpus(
#     r"R:\Admin\Alt Workspace\DPA v1_4 all - Copy",
#     ["Pre", "Post"],
#     ["PKP", "OCP", "CCP", "GFTA"],
#     pre_select=1,
#     post_select=0,
# )

organize_project(r"R:\Admin\Alt Workspace\DPA")

### ToDo
# Output to a new Phon project, rather than inside the same directory
# Accept input from a Phon base project, rather than a corpus folder
# Allow organizing/filtering by multiple layers
