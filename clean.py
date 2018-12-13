import sys, glob, shutil, os, re

def main():
    downloads = sys.argv[1]
    #structured = sys.argv[2]
    regex_tvs_file = tv_show_patterns_file()
    regex_tvs_folder = tv_show_patterns_folder()

    # Traverse recursively through root directory
    traverse_root(downloads, regex_tvs_file, regex_tvs_folder)


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
                    regex_tv_shows_pattern5,
                    regex_tv_shows_pattern6]
    return regex_patterns


def tv_show_patterns_folder():
    # Accepts S09E04, s09e112, S1, S02
    regex_tv_shows_pattern1 = re.compile(r"([Ss]{1}[0-9]{1,2}|[Ee]{1}[0-9]{1,3})")

    # Accpets Season 1, Season.05, Season.4, Season 1998
    regex_tv_shows_pattern2 = re.compile(r"(Season\s*\.?[0-9]{1,4})")

    # Accepts 4, 10 as season folders
    regex_tv_shows_pattern3 = re.compile(r"(^[0-9]{1,2}$)")

    # Accpets 4. Season
    regex_tv_shows_pattern4 = re.compile(r"([0-9]{1,2}\.\s+[Ss]{1}eason)")

    # Accpets 4. ser.a, Ser.a 6 where "." can be any letter
    regex_tv_shows_pattern5 = re.compile(r"([0-9]{1,2}?\.\s*?[Ss]{1}er.a|[Ss]{1}er.a\s*[0-9]{1,2})")

    # Accepts Series 1, series 2
    regex_tv_shows_pattern6 = re.compile(r"([Ss]{1}eries\s?[0-9]{1,2})")

    # Accepts Episode 2
    regex_tv_shows_pattern7 = re.compile(r" (Episode\s?[0-9]{1,3})")

    regex_patterns = [regex_tv_shows_pattern1,
                    regex_tv_shows_pattern2,
                    regex_tv_shows_pattern3,
                    regex_tv_shows_pattern4,
                    regex_tv_shows_pattern5,
                    regex_tv_shows_pattern6,
                    regex_tv_shows_pattern7]
    return regex_patterns


# TODO: regex for movies
# TODO: regex for Movie folders


def traverse_root(folder_structure, regex_tvs_file, regex_tvs_folder):
    for root, dirs, files in os.walk(folder_structure):
        try:
            path = root.split(os.sep)
            for pattern in regex_tvs_folder:
                if (pattern.findall(os.path.basename(root))):
                    print((len(path) - 1) * '---', os.path.basename(root))
                    # TODO: code that gets folder name, season and creates folder/-s from the data (also check if the folder has alread been created)
                    for file in files:
                        try:
                            extension = file.split(".")[-1]
                            if (validate_extension(extension)):
                                for pattern in regex_tvs_file:
                                    if pattern.findall(file):
                                        # TODO: code that gets file name and season and does stuff with it
                                        print(len(path) * '---', file)
                                        break
                        except UnicodeEncodeError:
                            pass       
                    break             
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