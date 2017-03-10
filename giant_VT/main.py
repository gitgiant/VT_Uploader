from settings import header
import uploader
import file_retriever
import time

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
        choice ='0'

        while choice != '5':
            # TODO: configure settings
            print("Please select from the following options:")
            print("1: Purge lists.")
            print("2: Print lists.")
            # print("2: Auto check if if queued scans have completed upon launch.")
            print("5: Return to main menu.")
            choice = input()
            if choice == '1':
                print("Purging resoruce_list.txt, sha256_list.txt, and URL_list.txt")
                f = open('resource_list', 'r+')
                f.seek(0)
                f.truncate()
                f = open('sha256_list', 'r+')
                f.seek(0)
                f.truncate()
                f = open('URL_list', 'r+')
                f.seek(0)
                f.truncate()
                f.close()
            if choice == '2':
                print("Printing resource_list.txt:")
                f = open('resource_list', 'r')
                print(f.read().replace(",","\n"))
                print("Printing sha256_list.txt:")
                f = open('sha256_list', 'r')
                print(f.read().replace(",","\n"))
                print("Printing URL_list.txt:")
                f = open('URL_list', 'r')
                print(f.read().replace(",","\n"))
                f.close()

    elif userChoice == '5':
        print("Exiting.")
        exit(1)
    # Whoops
    else:
        print("Incorrect input.")

