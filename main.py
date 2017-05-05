import time
from config import *
import os
import retriever
import uploader
import sys
import platform
import urllib
import watcher
# import URL_scraper

# TODO: Set up cron job for report grabber + directory watcher (watch API limits)
# TODO: Webpage portal or UI for uploading to bucket (jupyter notebook?)
# TODO: Implement Windows forensics
# TODO: Clean up and compact code, remove repeated code (URL and file upload/report), error testing, exception handling
# TODO: Script to take aws creds, create and mount s3 bucket
# TODO: Combine watch and quiet into one, or lock resource_list
# TODO: Add IP scan
# sets the current working directory to the folder which the script was run
if (platform.system()) is 'Windows':
    os.chdir(os.path.dirname(sys.argv[0]))
else:
    os.chdir(os.getcwd())

# TODO: error check (only allow one commandline argument set?)
# Command Line tools
if len(sys.argv) > 1:
    for arg in range(1, len(sys.argv)):
        # -f file upload
        if sys.argv[arg] == '-f' or sys.argv[arg] == '--file':
            # if -f is followed by a file, then upload it
            if os.path.isfile(sys.argv[arg+1]):
                uploader.upload_file(sys.argv[arg+1])
            else:
                print("Error " + sys.argv[arg+1] + " is not a file.")
        # -d directory upload
        elif sys.argv[arg] == '-d' or sys.argv[arg] == '--dir':
            if os.path.isdir(sys.argv[arg+1]):
                uploader.upload_directory(sys.argv[arg+1])
            else:
                print("Error " + sys.argv[arg+1] + " is not a directory.")
        # -u URL upload TODO: Validate urls
        elif sys.argv[arg] == '-u' or sys.argv[arg] == '--url':
            uploader.upload_URL(sys.argv[arg+1])
        # elif sys.argv[arg] == '-s' or sys.argv[arg] == '--scrape':
        #     URL_scraper(sys.argv[arg+1])
        # -r check reports
        elif sys.argv[arg] == '-r' or sys.argv[arg] == '--report':
            retriever.check_file_scans(True)
            retriever.check_URL_scans(True)
        elif sys.argv[arg] == '-q' or sys.argv[arg] == '--quiet':
            retriever.check_file_scans(False)
            retriever.check_URL_scans(False)
        elif sys.argv[arg] == '-w' or sys.argv[arg] == '--watch':
            watcher.start_watcher(sys.argv[arg+1])
        elif sys.argv[arg] == '-h' or sys.argv[arg] == '--help':
            display_help()
        # Incorrect input
        else:
            display_usage()
            exit()
# TODO: Clean up output, add progress bar for uploads,
if __name__ == '__main__':
    print(header)
    time.sleep(.4)

    userChoice = '0'
    while userChoice != '9':
        print("______________________________________________")
        print("Please select from the following options:")
        print("1: Select a file.")
        print("2: Select a Directory.")
        print("3: Select a URL.")
        print("4: Check if queued file scans have completed.")
        print("5: Check if queued URL scans have completed.")
        print("6: Watch a directory for new files.")
        print("7: Pull recently executed files from Windows shim cache.")
        print("8: Configure settings.")
        print("9: Exit.")

        userChoice = input()
        # File
        if userChoice == '1':
            targetFile = input("Please enter the path of the file:")
            uploader.upload_file(targetFile)

        # Directory
        elif userChoice == '2':
            print("Warning: This will upload all found files in this directory and subdirectories.")
            rootDir = input("Please enter path of the Directory:\n")
            # check if directory exists
            if os.path.isdir(rootDir):
                print("Uploading Directory: " + os.path.basename(rootDir))
                uploader.upload_directory(rootDir)
            else:
                print("Error: Directory Not Found.")
                continue


        # URL
        elif userChoice == '3':
            targetURL = input("Please enter a valid http, https, or ftp URL: ")
            #uploader.upload_URL(targetURL)
            URL_scraper.scrape_URLS(targetURL)

        # Check File Scans
        elif userChoice == '4':
            print("Checking resource_list for targets that have completed scanning.")
            retriever.check_file_scans(True)

        # Check URL Scans
        elif userChoice == '5':
            print("Checking URL_list for targets that have completed scanning.")
            retriever.check_URL_scans(True)
        # Watch Directory
        elif userChoice == '6':
            path = input("Please specify a path of a directory to watch for new files.")
            watcher.start_watcher(path)


        # Pull Shim Cache
        elif userChoice == '7':
            # Test for Windows
            if platform.system() is 'Windows':
                from shimCache import *
            else:
                print('OS Detected: ' + platform.system())
                print('Unfortunately, Windows forensics features are only available on Windows.')
                continue
            exeList = pull_shim_cache()
            # TODO put batch upload in pull_shim_cache(), spawn thread
            try:
                print(str(len(exeList)) + " number of files found in shim cache.  Each upload will take ~15 seconds.")
                print("Total expected upload time: " + str(int((len(exeList) * 15) / 60)) + " minutes.")
                for line in exeList:
                    if os.path.isfile(line):
                        waitTime = uploader.upload_file(line)
                        # if the upload took longer than 15 seconds
                        if(waitTime > 15):
                            waitTime = 15
                        # Virus Total API rules state you must not make more than 4 requests a minute.
                        print("Waiting " + str(15 - waitTime) +  " seconds to upload next file (Virus Total public API rules state 4 requests a minute).")
                        time.sleep(15 - waitTime)
                    else:
                        print(line + " file not found.")
            except Exception as e:
                print(e)

        # Settings
        # TODO: Allow user to change key, change from public key to private key mode
        elif userChoice == '8':
            configure_settings()

        elif userChoice == '9':
            print("Exiting.")
            exit(1)
        # Whoops
        else:
            print("Incorrect input.")