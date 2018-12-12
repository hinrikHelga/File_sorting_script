import sys, glob, shutil, os, re

def main():
    downloads = sys.argv[1]
    #structured = sys.argv[2]
    regex_tvs_file = tv_show_patterns_file()

    # Traverse recursively through root directory
    traverse_root(downloads, regex_tvs_file)


def tv_show_patterns_file():
    # Accepts S01E05, s12e21
    regex_tv_shows_pattern1 = re.compile(r"([Ss]{1}[0-9]{1,2}|[Ee]{1}[0-9]{1,2})")

    # Accepts Season 2 - Episode 01 where Season, 2, Episode and 01 are all different groups (group 1, 2, 3 and 4)
    regex_tv_shows_pattern2 = re.compile(r"(Season)\s?([0-9]{1,2})\s*[\-]*\s*(Episode)\s*([0-9]{1,2})")

    # Accpets 205.avi, 205b, 0100 (bugs needs to be fixes such as x264)
    regex_tv_shows_pattern3 = re.compile(r"([0-9]{3,4}[a|b]?)")

    # Accepts 30 Rock [1.01] Pilot.avi
    regex_tv_shows_pattern4 = re.compile(r"(\[[0-9]{1,2}\.[0-9]{1,2}\])")

    # Accepts 01x01, 1x01
    regex_tv_shows_pattern5 = re.compile(r"([0-9]{1,2}x[0-9]{1,2})")

    # Accepts hdtv, HDTV, has bugs so not included in list
    regex_tv_shows_pattern6 = re.compile(r"(hdtv|HDTV)")

    regex_patterns = [regex_tv_shows_pattern1,
                    regex_tv_shows_pattern2,
                    regex_tv_shows_pattern3, 
                    regex_tv_shows_pattern4,
                    regex_tv_shows_pattern5]
    return regex_patterns


# TODO: regex for movies
# TODO: regex for TV show folders
# TODO: regex for Movie folders


def traverse_root(folder_structure, regex_tvs_file):
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
                    for pattern in regex_tvs_file:
                        if pattern.findall(file):
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

# TODO: structured directory functionality

print(main())