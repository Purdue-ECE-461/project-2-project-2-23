import os  # os
import sys # sys
def get_version_info(doc_loc):
    try:
        package_json_list = []

        for dirs, dir, check_json in os.walk(doc_loc):
            for check_per in check_json:
             if 'package.json' in check_per:
                temp = (dirs + '/' + check_per)
                package_json_list.append(temp)

        counter1 = 0 # counter for ^
        counter2 = 0 # counter for ~


        for package_json in package_json_list:
            with open(package_json) as json_content:
                for line_content in json_content:
                    if "^" in line_content: counter1 = counter1 + 1
                    elif "~" in line_content: counter2 = counter2 + 1

        return {"c1":counter1,"c2":counter2} #return a dictionary where first value is counter for ^ and second one is counter for ~




    except:
        return -1


if __name__ == '__main__':
    print(get_version_info('browserify-master')) # test