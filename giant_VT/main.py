from giant_VT.config import *
from giant_VT import uploader
from giant_VT import file_retriever
import time

if __name__ == '__main__':
    print(header)
    time.sleep(.4)

    userChoice = '0'
    while userChoice != '5':
        print("______________________________________________")
        print("Please select from the following options:")
        print("1: Select a file.")
        print("2: Select a URL.")
        print("3: Check if queued scans have completed.")
        print("4: Configure settings.")
        print("5: Exit.")

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

        # Settings
        elif userChoice == '4':
            configure_settings()

        elif userChoice == '5':
            print("Exiting.")
            exit(1)
        # Whoops
        else:
            print("Incorrect input.")

