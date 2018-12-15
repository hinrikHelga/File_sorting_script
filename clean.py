import sys, glob, shutil, os, re, regex

def main():
    downloads = sys.argv[1]
    #downloads = r"C:\Users\Hinrik Helgason\Google Drive\HR\3. ár\Haustönn\Forritunarmalid Python\Hopverkefni_data\downloads"
    #structured = sys.argv[2]

    regex_tvs_file = tv_show_patterns_file()
    regex_tvs_folder = tv_show_patterns_folder()

    # Traverse recursively through root directory
    traverse_root(downloads, regex_tvs_file, regex_tvs_folder)



def traverse_root(folder_structure, regex_tvs_file, regex_tvs_folder):
    src_dir = sys.argv[1]
    stru_dir = sys.argv[2]
    print(src_dir)
    print(stru_dir)

    try:
        next_immediate_item = next(os.walk(src_dir))[1]

        for item in next_immediate_item:
            src_path = src_dir + item
            for patt in regex_tvs_folder:
                match_object = patt.findall(item)
                if len(match_object) > 0:

                    if os.path.isdir(src_path):
                        make_directory(item, get_show_name(item, get_all_tv_show_folder_pattern()), src_dir, stru_dir)
                break
    except StopIteration:
        pass
    
    
    
    
    for root, dirs, files in os.walk(folder_structure):
        try:
            path = root.split(os.sep)
            param_path = folder_structure.split(os.sep)

            root_index = param_path[-1]
            root_dir_index = path.index(root_index)
            dir_lis = [x for x in path[root_dir_index:]]

            for pattern in regex_tvs_folder:
                match_object = pattern.findall(os.path.basename(root))
                folder = os.path.basename(root)
                #print(folder)
                # If the folder is a TV show
                if (match_object):
                    # TODO: code that gets folder name, season and creates folder/-s from the data (also check if the folder has alread been created)
                    
                    #print(folder)
                    #make_directory(get_show_name(folder, get_all_tv_show_folder_pattern()), src_dir, stru_dir )
                    
                    #print((len(path) - 1) * '---', os.path.basename(root)) 
                    for file in files:
                        try:
                            extension = file.split(".")[-1]
                            if (validate_extension(extension)):
                                for pattern in regex_tvs_file:
                                    if pattern.search(file) != None:
                                        # TODO: code that gets file name and season and does stuff with it
                                        #print(get_show_name(file, get_all_tv_shows_file_pattern()))
                                        #print(len(path) * '---', file)
                                        break
                        except UnicodeEncodeError:
                            pass       
                    break     
        except UnicodeEncodeError:
            pass
            


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


def get_season_and_number(item):
    # Edge case
    match_object = None
    for patt in tv_show_patterns_folder():
            match_object = patt.findall(item)
            if len(match_object) > 0:
                break
    if (item[0] == "24"):
        return None
    return "Season " + get_number(match_object[0])
    

# Gets the number of a season in string
def get_number(s):
    number = ""
    for c in s:
        if (c.isdigit()):
            number += c

    number = int(number)
    if (number < 10):
        number = str(number)
        number = "0" + number
    number = str(number)
    return number
   

def get_show_name(file, reg_pat):
    words_only = regex.findall(r"[a-zA-Z0-9\p{L}]+", file)
    for i, item in enumerate(words_only):
        if reg_pat.search(item) != None:
            # So TV shows whose is name is a number is validated
            if i == 0 and item.isdigit():
                continue
            
            # If there is a number in the TV Show title but it's not the season number
            elif not regex.search(r"([Ss]{1}eason|[Ss]{1}erie|[Ss]{1}er.a)", words_only[i-1]) and item.isdigit():
                continue 

            # If the word in list before the match, i.e. if the match is "2" and word before "2" is equal to "Season", remove Season
            elif regex.search(r"([Ss]{1}eason|[Ss]{1}erie|[Ss]{1}er.a)", words_only[i-1]):
                words_only = words_only[:words_only.index(words_only[i-1])]                

            # Otherwise, get the elements before the regex match
            else:
                words_only = words_only[:words_only.index(item)]
            
            for j in range(0, len(words_only)):
                words_only[j] = words_only[j].capitalize()
            words_only = " ".join(words_only)
            break

        # If the season number is year instead of incremented numbers
        elif regex.search(r"([Ss]{1}eason|[Ss]{1}erie|[Ss]{1}er.a)", words_only[i-1]) and len(item) == 4:
            try:
                item_int = int(item)
            except ValueError:
                continue
            words_only[i - 1] = words_only[i - 1] + " " + words_only[i]
            words_only = words_only[:words_only.index(words_only[i-1])]

            for j in range(0, len(words_only)):
                words_only[j] = words_only[j].capitalize()
            words_only = " ".join(words_only)
            break
    return words_only


def get_all_tv_shows_file_pattern():
    return re.compile(r"([Ss]{1}[0-9]{1,2}|[Ee]{1}[0-9]{1,2})|(Season)\s?([0-9]{1,2})\s*[\-]*\s*(Episode)\s*([0-9]{1,2})|([0-9]{3,4}[a|b]?)|(\[[0-9]{1,2}\.[0-9]{1,2}\])|([0-9]{1,2}x[0-9]{1,2})|(hdtv|HDTV)")


def get_all_tv_show_folder_pattern():
    return re.compile(r"([Ss]{1}[0-9]{1,2}|[Ee]{1}[0-9]{1,3})|([Ss]{1}eason\s*\.?[0-9]{1,4})|(^[0-9]{1,2}$)|([0-9]{1,2}\.\s+[Ss]{1}eason)|([0-9]{1,2}?\.\s*?[Ss]{1}er.a|[Ss]{1}er.a\s*[0-9]{1,2})|([Ss]{1}eries\s?[0-9]{1,2})|(Episode\s?[0-9]{1,3})")


def validate_extension(f_extension):
    # Only validate video files
    if (f_extension == "avi" or
        f_extension == "mkv" or
        f_extension == "mp4"):
        return True
    
    return False


# TODO: structured directory functionality
def make_directory(original, folder_name, src_dir, stru_dir):
    patt = tv_show_patterns_folder
    
    print("panus")
    #print(match_object)
    #print('Original: ', original)
    #print('folder_name: ', folder_name)
    #rint('Source: ', src_dir)
    #print('Structured: ', stru_dir)
    stru_dir_absolute_path = str(stru_dir) + str(folder_name)
    src_dir_absoulute_path = src_dir + original
    if not os.path.exists(stru_dir_absolute_path):
        #print('I am now creating the path: ', stru_dir_absolute_path)
        os.makedirs(stru_dir_absolute_path)
    try:
        next_immediate_item = next(os.walk(src_dir_absoulute_path))[1]
        for item in next_immediate_item:
       
            if os.path.isdir(src_dir_absoulute_path):
                #print(item)
                print(get_show_name(item, get_all_tv_show_folder_pattern))
                make_directory(item, get_show_name(item, get_all_tv_show_folder_pattern()), src_dir_absoulute_path + "\\", stru_dir_absolute_path + "\\")
    except StopIteration:
        pass


print(main())