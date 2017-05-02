# Checks if target file is a file, opens the file, checks size of file
# Calls calculate_sha256, which checks if file is already in sha256_list
# If everything succeeds, uploads file to Virus Total
import math
import os
import time

# check if requests module installed
try:
    import requests
except ImportError:
    print("Requests Module required.  Attempting to install using pip.")
    try:
        import pip
        pip.main(['install', requests])
    except Exception as e:
        print(e)
        print("Pip module not found!  Please go to http://docs.python-requests.org/en/master/ to install requests Module.")

from report import display_URL_report
from tokens import key

from calc_sha import calculate_sha256

MAX_FILE_SIZE = 32000000 # 32 megabytes


# TODO: Implement threading, exception handling when connection refused, repair lists if failed upload, return time taken to upload (subtract from API timer)
def upload_file(targetFile):
    start = time.time()
    # Set API key to token key
    params = {'apikey': key}
    uploadTime = int()
    # Open target file
    if os.path.isfile(targetFile):
        print("Filename: " + os.path.basename(targetFile))
        files = {'file': (os.path.basename(targetFile), open(targetFile, 'rb'))}
    else:
        print("Error: File Not Found.")
        # return a uploadTime of '15' seconds to make waitTime 0 for next job (15 - uploadTime = 0)
        return 15

    # Check if file is greater than max file size
    size = os.path.getsize(targetFile)
    if size > MAX_FILE_SIZE:
        print("Error file size " + str(round(size/1000000,2))+ " MB is greater than 32 MB (virustotal public API filesize limit.)")
        # return a uploadTime of '15' seconds to make waitTime 0 for next job (15 - uploadTime = 0)
        return 15
    else:
        print("Filesize: " + str(round(size/1000000,2)) + " MB.")

    # If file has passed checks, sha256 and check sha256_list.txt
    found = calculate_sha256(targetFile)
    # If file not in sha256_list.txt
    if found:
        print("File " + targetFile + " is present in local queue, it has already been uploaded to virus total")
        print("Please check if queued scans have completed and view their reports.")
        # return a uploadTime of '15' seconds to make waitTime 0 for next job (15 - uploadTime = 0)
        return 15
    # File has not been found in sha256_list.txt
    else:
        print("Uploading, please wait...")
        print("______________________________________________")
        try:
            response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=files, params=params)
            # TODO: Whenever you exceed the public API request rate limit a 204 HTTP status code is returned.
            # TODO: If you try to perform calls to functions for which you do not have the required privileges
            # TODO: an HTTP Error 403 Forbidden is raised.
            json_response = response.json()
            end = time.time()
            uploadTime = math.floor(end - start)
            print("Upload Complete @ " + str(uploadTime) + " seconds.")

            # display information from returned json document
            # display_file_report(json_response)
        except Exception as e:
            print(e)
        # add response to the csv response file to scan later
        with open('resource_list', "a") as fileWrite:
            fileWrite.write(json_response['resource'] + '\n')

    return uploadTime

# TODO implement
def upload_URL(targetURL):
    # Sets API key to key token, sets URL
    params = {'apikey': key, 'url': targetURL}
    print("Target URL: " + targetURL)

    # Search URL_list.txt to see if this URL has already been uploaded
    with open('URL_list', "r") as URLRead:
        for line in URLRead:
            if targetURL in line:
                print("URL is present in local queue, it has already been uploaded to virus total")
                print("Please check if queued scans have completed and view their reports.")
                print("Returning to main menu")
                return
    # Upload to virustotal
    print("Uploading, please wait...")
    print("______________________________________________")
    response = requests.post('https://www.virustotal.com/vtapi/v2/url/scan', data=params)
    # TODO: Whenever you exceed the public API request rate limit a 204 HTTP status code is returned.
    # TODO: If you try to perform calls to functions for which you do not have the required privileges
    # TODO: an HTTP Error 403 Forbidden is raised.
    json_response = response.json()

    display_URL_report(json_response)
    with open('URL_list', "a") as URLWrite:
        URLWrite.write(json_response['resource'] + ',')

def upload_directory(targetDirectory):
    # walk through directory
    for folder, subs, files in os.walk(targetDirectory):
        for fileName in files:
            upload_file(os.path.join(folder, fileName))
            # API limits 600 uploads / minute
            time.sleep(.1)