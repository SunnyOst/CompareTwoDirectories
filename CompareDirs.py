import os
import sys
import time
import string
import difflib

def get_paths():
    """
    Get paths from user and check if they exist.
    """
    while True:
        try:
            path1 = raw_input("Enter the path to the first directory:\n ")
            if os.path.isfile(path1):
				path1 = os.path.split(path1)[0]
            if not os.path.exists(path1):
                raise ValueError("Path does not exist!")
            break
        except ValueError as e:
            print e
			

    while True:
        try:
            path2 = raw_input("Enter the path to the second directory:\n ")
            if os.path.isfile(path2):
                path2 = os.path.split(path2)[0]
            if not os.path.exists(path2):
                raise ValueError("Path does not exist!")
            if os.path.abspath(path1)==os.path.abspath(path2):
				raise ValueError("Paths are the same!")
            return path1, path2
        except ValueError as e:
            print e

def get_ignored():
    """
    Get ignored words from user.
    """
    ignored = raw_input("Optionally, enter text strings to use as a blacklist filter(separated by a comma):\n ")
    if ignored != "":
        return list(filter(lambda a: a!= "", ignored.split(",")))
    else:
		return []

def get_files(path,ignored):
    """
    Get a list of files in a directory.
    """
    files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for dirname in dirnames:
            files.append(os.path.relpath(os.path.join(dirpath, dirname),path))
        for filename in filenames:
            files.append(os.path.relpath(os.path.join(dirpath, filename),path))
    ignore_files(files,ignored)
    return files

def get_missing(path1, path2, files1, files2):
    """
    Get a list of files that are missing from one directory.
    """
    missing1 = []
    missing2 = []
    #files1 = get_files(path1)
    #files2 = get_files(path2)
    for file1 in files1:
        if file1 not in files2:
            missing1.append(file1)
    for file2 in files2:
        if file2 not in files1:
            missing2.append(file2)
    return missing1, missing2

def get_different(path1, path2, files1, files2, missing1):
    """
    Get a list of files that have the same name but different content.
    """
    different = []
    #files1 = get_files(path1)
    #files2 = get_files(path2)
    for file1 in files1:
      if not os.path.isdir(os.path.join(path1,file1)):
        if file1 not in missing1:
            if file1 not in different:
                with open(os.path.join(path1,file1), "r") as f1:
                    with open(os.path.join(path2,file1), "r") as f2:
                        if f1.read() != f2.read():
                            different.append(file1)
    return different

def ignore_files(files, ignored):
    """
    Remove files that contain ignored words in the path or name.
    """
    ignored_files = []
    for word in ignored:
        for file in files:
            if word.lower() in file.lower():
                ignored_files.append(file)
    for file in ignored_files:
        if file in files: files.remove(file)
    #if file in files
    return files

def main():
    """
    Main Function
    """
    print "Find differences in the structures of two directories, and compare the files that have counterparts!"
    path1, path2 = get_paths()
    ignored = get_ignored()
    print "\nProcessing..."
    files1 = get_files(path1,ignored)
    files2 = get_files(path2,ignored)
    missing1, missing2 = get_missing(path1, path2, files1, files2)
    different = get_different(path1, path2, files1, files2, missing1)
    print "\n\n---   Files and folders with no counterparts:   ---\n"
    for file in missing1:
        print os.path.join(path1,file)
    for file in missing2:
        print os.path.join(path2,file)
    print "\n---   Files with different content:   ---\n"
    for file in different:
        print file
    raw_input("\nPress Enter to close...")

if __name__ == "__main__":
    main()