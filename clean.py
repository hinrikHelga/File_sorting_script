import sys, glob, shutil, os, re

def main():
    downloads = sys.argv[1]
    #structured = sys.argv[2]

    # Work in progress...
    regex_tv_shows_pattern = re.compile(r"([Ss]{1}[0-9]{2}[Ee]{1}[0-9]{2})|(Season)\s?([0-9]{1,2})\s*[\-]*\s*(Episode)\s*([0-9]{1,2})")
    # TODO: regex for movies
    
    # Traverse recursively through root directory
    traverse_root(downloads, regex_tv_shows_pattern)

    # TODO: structured directory functionality


def traverse_root(folder_structure, regex):
    for root, dirs, files in os.walk(folder_structure):
        try:
            path = root.split(os.sep)
            # Prints folder name
            #print((len(path) - 1) * '---', os.path.basename(root))
        except UnicodeEncodeError:
            pass
        for file in files:
            try:
                extension = file.split(".")[-1]
                if (validate_extension(extension)):
                    if regex.findall(file):
                        print(len(path) * '---', file)
            except UnicodeEncodeError:
                pass


def validate_extension(f_extension):
    # Only validate video files
    if (f_extension == "avi" or 
        f_extension == "mkv" or
        f_extension == "mp4"):
        return True
    
    return False

print(main())