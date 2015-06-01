'''
Little utility developed to fix messy absolute links when dumping site http://www.antibioticresistance.org.uk/
via wget.

The site used strange scripts to create links to the internal pages, preventing wget to fully transform all
absolute links to relative links that may work offline.

This tool helped replace links to http://www.antibioticresistance.org.uk/ARFAQs.nsf/ and
http://www.antibioticresistance.org.uk/arfaqs.nsf/ by relative links (../ for example)

'''
import os

__author__ = 'jtorrente'

def scanDirMain(main_path, dir_to_scan):
    scanDirMain.__doc__ = "Main call to the scanDir function. \"" \
                          + "nStarts scanning the directory in level 0\n. Additional doc:" \
                          + scanDir.__doc__
    scanDir(main_path, dir_to_scan, 0, {})

def scanDir(main_path, dir_to_scan, level, levels):
    '''
    Scans the given directory (*dir_to_scan*) recursively in search for html documents that may
    have ill-formed links using absolute paths.

    In short, this will replace all occurrences of the string *main_path*, either as it is
    provided or in lower case (both cases are checked), by a relative path consisting of a
    number of ../ statements, depending on the *level* of (*dir_to_scan*) respect to the
    root directory.

    So, for example, if the root directory containing all html files to be processed is
    /rootdir/, and the absolute path to replace is http://www.url.com/main/, the next replacements
    will be made in the next files:

    /rootdir/file1.html => http://www.url.com/main/ is replaced by the empty string.
        Example of replacements in this file:
        http://www.url.com/main/image1.jpg -> image1.jpg
    /rootdir/subdir1/file2.html => http://www.url.com/main/ is replaced by "../"
        Example of replacements in this file:
        http://www.url.com/main/image2.jpg -> ../image2.jpg
    /rootdir/subdir1/subdir2/file3.html => http://www.url.com/main/ is replaced by "../../"
        Example of replacements in this file:
        http://www.url.com/main/image3.jpg -> ../../image3.jpg

    *levels* is a dictionary where relative paths to be applied are cached
    '''

    if not level in levels:
        levels[level] = relativePath(level)

    for childFile in os.listdir(dir_to_scan):
        abspath = dir_to_scan + os.sep + childFile
        if childFile.lower().endswith(".html"):
            print("Fixing file: "+abspath)
            f = open(abspath, 'r')
            file_data = f.read()
            f.close()

            new_data = file_data.replace(main_path, levels[level])
            new_data = new_data.replace(main_path.lower(), levels[level])

            f = open(abspath, "w")
            f.write(new_data)
            f.close()
        elif os.path.isdir(abspath):
            print("*******************************")
            print("Scanning directory recursively: "+abspath)
            print("*******************************")
            scanDir(main_path, abspath, level+1, levels)

def relativePath(level):
    string = ""
    for i in range(0,level):
        string += r"../"
    return string

scanDirMain("http://www.antibioticresistance.org.uk/ARFAQs.nsf/",
        r"C:\DEVELOPMENT\GnuWin32\bin\Attempt3\www.antibioticresistance.org.uk\ARFAQs.nsf")