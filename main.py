import time
from config import *
import os
import file_retriever
import uploader
import sys
import platform
import urllib

# sets the current working directory to the folder which the script was run
if (platform.system()) is 'Windows':
    os.chdir(os.path.dirname(sys.argv[0]))
else:
    os.chdir(os.getcwd())

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
        # -r check reports
        elif sys.argv[arg] == '-r' or sys.argv[arg] == '--report':
            file_retriever.check_file_scans()
        # Incorrect input
        elif sys.argv[arg] == '-h' or sys.argv[arg] == '--help':
            display_help()
        else:
            display_usage()
        exit()
# TODO: Clean up output, add progress bar for uploads,
if __name__ == '__main__':
    print(header)
    time.sleep(.4)


    userChoice = '0'
    while userChoice != '7':
        print("______________________________________________")
        print("Please select from the following options:")
        print("1: Select a file.")
        print("2: Select a Directory.")
        print("3: Select a URL.")
        print("4: Check if queued scans have completed.")
        print("5: Pull recently executed files from Windows shim cache.")
        print("6: Configure settings.")
        print("7: Exit.")

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
            # walk through directory
            # for folder, subs, files in os.walk(rootDir):
            #     for fileName in files:
            #         uploader.upload_file(os.path.join(folder,fileName))
            #         # API limits 600 uploads / minute
            #         time.sleep(.1)

        # URL
        elif userChoice == '3':
            targetURL = input("Please enter URL of file:")
            uploader.upload_URL(targetURL)


        # Check Scans
        elif userChoice == '4':
            print("Checking resource_list.txt for targets that have completed scanning.")
            file_retriever.check_file_scans()

        # Pull Shim Cache
        elif userChoice == '5':
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
        elif userChoice == '6':
            configure_settings()

        elif userChoice == '7':
            print("Exiting.")
            exit(1)
        # Whoops
        else:
            print("Incorrect input.")