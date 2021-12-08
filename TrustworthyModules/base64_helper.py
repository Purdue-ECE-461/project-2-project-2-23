# Citation: 
# Link: https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory 
# Needs to use code from the link above for getting the zip file of the working dir

# Link: https://stackoverflow.com/questions/11511705/base64-encode-a-zip-file-in-python
# Needs to use code from this link for converting the zip file into base64 string, the way is more efficient

import os # no coverage
import shutil # no coverage
import base64 # no coverage

def base64_helper(dir):

    # Now get the zip file of the files

    zip_file = 'temp_zip'
    shutil.make_archive(zip_file, 'zip', dir)
    
    # The output zip file will locate in the current root folder of base64_helper.py

    with open(zip_file + '.zip', 'rb') as fin, open('output.zip.b64', 'wb') as fout:
        base64.encode(fin, fout)

    # Reading the base 64 encoding string

    base_64_file = open('output.zip.b64', 'r', encoding = 'utf-8')
    base_64_code = base_64_file.read()
    base_64_file.close()

    # Deleting the temp files before return
    os.remove('output.zip.b64')
    os.remove('temp_zip.zip')

    return base_64_code