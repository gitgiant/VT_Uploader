from giant_VT.config import *
from giant_VT import uploader
from giant_VT.calc_sha import calculate_sha256
from giant_VT import file_retriever
from giant_VT.shimCache import *
import time

# TODO: Clean up output, add progress bar for uploads
if __name__ == '__main__':
    print(header)
    time.sleep(.4)

    userChoice = '0'
    while userChoice != '6':
        print("______________________________________________")
        print("Please select from the following options:")
        print("1: Select a file.")
        print("2: Select a URL.")
        print("3: Check if queued scans have completed.")
        print("4: Pull recently executed files from Windows shim cache.")
        print("5: Configure settings.")
        print("6: Exit.")

        userChoice = input()
        # File
        if userChoice == '1':
            targetFile = input("Please enter path of file:")
            uploader.upload_file(targetFile)

        # URL
        elif userChoice == '2':
            targetURL = input("Please enter URL of file:")
            uploader.upload_URL(targetURL)

        # Check Scans
        elif userChoice == '3':
            print("Checking resource_list.txt for targets that have completed scanning.")
            file_retriever.check_file_scans()

        elif userChoice == '4':
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
        elif userChoice == '5':
            configure_settings()

        elif userChoice == '6':
            print("Exiting.")
            exit(1)
        # Whoops
        else:
            print("Incorrect input.")

