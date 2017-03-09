import requests
import os

#keep key private
from tokens import key
from calc_sha import calculate_sha256
from report import display_file_report
from report import display_URL_report


MAX_FILE_SIZE = 32000000 # 32 megabytes
# Checks if target file is a file, opens the file, checks size of file
# Calls calculate_sha256, which checks if file is already in sha256_list
# If everything succeeds, uploads file to Virus Total


def upload_file(targetFile):

    # Set API key to token key
    params = {'apikey': key}

    # TODO: extract filename from targetFile
    # Open target file
    if os.path.isfile(targetFile):

        print("Filename: " + os.path.basename(targetFile))
        files = {'file': (os.path.basename(targetFile), open(targetFile, 'rb'))}
    else:
        print("Error: File Not Found.")
        exit(-1)

    # Check if file is greater than max file size
    size = os.path.getsize(targetFile)
    if size > MAX_FILE_SIZE:
        print("Error file size " + str(round(size/1000,2))+ " kB is greater than 32 MB.")
    else:
        print("Filesize: " + str(round(size/1000,2)) + " kB.")

    # If file has passed checks, sha256 and check sha256_list.txt
    found = calculate_sha256(targetFile)
    # If file not in sha256_list.txt
    if found:
        print("File has already been uploaded to virus total.")
        print("Please check if it's scan has been completed.")
    # File has not been found in sha256_list.txt
    else:
        print("Uploading, please wait...")
        print("______________________________________________")
        response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=files, params=params)
        # TODO: Whenever you exceed the public API request rate limit a 204 HTTP status code is returned.
        # TODO: If you try to perform calls to functions for which you do not have the required privileges
        # TODO: an HTTP Error 403 Forbidden is raised.
        json_response = response.json()
        print("Upload Complete")

        # display information from returned json document
        display_file_report(json_response)

        # add response to the csv response file to scan later
        with open('resource_list', "a") as fileWrite:
            fileWrite.write(json_response['resource'] + ',')


def upload_URL(targetURL):
    # Sets API key to key token, sets URL
    params = {'apikey': key, 'url': targetURL}
    print("Target URL: " + targetURL)

    # Search URL_list.txt to see if this URL has already been uploaded
    with open('URL_list', "r") as URLRead:
        for line in URLRead:
            if targetURL in line:
                print("sha256 found, this file has already been scanned and uploaded.")

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