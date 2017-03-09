from settings import header
import uploader
import file_retriever

print(header)

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
    if userChoice == '1':
        # Target = input("Please enter path of file:")
        targetFile = 'C:/Users/Giant/Desktop/HRC.exe'
        uploader.upload_file(targetFile)
    if userChoice == '2':
        target = input("Please enter URL of file:")
        targetURL = 'https://csuci.blackboard.com/branding/_1_1/logo.png'
        uploader.upload_URL(targetURL)
    if userChoice == '3':
        target = input("Checking resource_list.txt for targets that have completed scanning.")
        #TODO: Set up retriever
        file_retriever.check_file_scans()
    if userChoice == '4':
        target = input("Please select from the following options:")
        print("1: Auto check if if queued scans have completed upon launch.")
        print("2: Purge lists.")
        #TODO: configure settings

print("Exiting.")
exit(1)
