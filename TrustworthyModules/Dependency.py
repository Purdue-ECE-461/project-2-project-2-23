from os import walk
import re

class Dependency:
    def __init__(self, module_name, url, priority):
        self.module_name = module_name
        self.url = url
        self.priority = priority
        self.score = 0


    def calculate_score(self):
        #try:
        package_json = ''
        print(((self.module_name.split('/'))[0]))

        found_json = False
        for (dirs, dir, check_json) in walk((self.module_name.split('/'))[0]):
            print(check_json)
            for check_per in check_json:
                if 'package.json' in check_per:
                    found_json = True
                    package_json = (dirs + '/' + check_per)
                    break;
            if found_json: break;

        pinned_count = 0 # counter for ^
        total_dep = 0 # counter for ~

        json_lines = open(package_json, 'r').readlines()

        dep_flag = False
        for line in json_lines:
            line = str(line.rstrip())
            print(line)

            if re.search(r'}', line) is not None:
                dep_flag = False

            if not dep_flag:
                pass
            else:
                total_dep += 1
                splitLine = (line.replace(" ", "")).split(":")
                version_search = re.compile('(~|=)?[0-9]{1,2}\.[0-9]{1,2}\.(([0-9]{1,2})|(\*)|x|X)')

                temp = splitLine[1]
                version = temp.replace(',', '').replace('\"', '')
                if (re.search(r'\^|\>|\<', line) is not None) | (re.search(version_search, line) is None):
                    pass
                elif "-" in version:
                    ver1 = (version.split("-"))[0].split(".")
                    ver2 = (version.split("-"))[1].split(".")
                    if (ver1[0] == ver2[0]) & (ver1[1] == ver2[1]):
                        pinned_count += 1
                elif re.search(version_search, line) is not None:
                    pinned_count += 1
            if 'dependencies' in line.lower():
                dep_flag = True
        
        self.score = pinned_count/total_dep

        '''except:
            self.score = 0'''
