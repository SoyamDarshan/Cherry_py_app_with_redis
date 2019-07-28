from zipfile import ZipFile
import glob
import os


def check_most_recent_file_available(name):
    try:
        file_list_available = glob.glob('extracted_files/*')
        file_name_available = max(file_list_available, key=os.path.getctime)
        if file_name_available == ''.join(['extracted_files/', name]):
            return True
        else:
            return False
    except:
        return False


try:
    files_available = glob.glob('downloads/*')
    # print(files_available)
    # Get most recent file
    file_name = max(files_available, key=os.path.getctime)
    # print(file_name)

    with ZipFile(file_name, 'r') as zip:
        zip.printdir()
        value = zip.namelist()[0]
        print(value)
        if not check_most_recent_file_available(value):
            print(
                f'Extracting the file {file_name} to path ./extracted_files/{value}')
            zip.extract(value, path='extracted_files')
            print('Done!')
        else:
            print('Latest file is already available')
except:
    print('No files available')
