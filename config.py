# TODO: add settings
header = """
  ,ad8888ba,  88
 d8"'    `"8b ""                         ,d
d8'                                      88
88            88 ,adPPYYba, 8b,dPPYba, MM88MMM
88      88888 88 ""     `Y8 88P'   `"8a  88
Y8,        88 88 ,adPPPPP88 88       88  88
 Y8a.    .a88 88 88,    ,88 88       88  88,
  `"Y88888P"  88 `"8bbdP"Y8 88       88  "Y888
______________________________________________
Version 0.3     http://www.github.com/gitgiant
Thank you for contributing to the virus total community.
Please be patient as scans may take awhile to complete."""
def configure_settings():
    choice = '0'

    while choice != '5':
        # TODO: configure settings
        print("Please select from the following options:")
        print("1: Purge lists.")
        print("2: Print lists.")
        print("3: Change API key.")
        print("5: Return to main menu.")
        choice = input()
        if choice == '1':
            choice = input("This will clear all lists including already scanned files.  Are you sure? [y/n]: ").lower()
            if choice == 'y':
                print("Purging resource_list.txt, sha256_list.txt, and URL_list.txt")
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
            elif choice == 'n':
                # exits
                pass
            else:
                print("Invalid input")
                pass
        elif choice == '2':
            try:
                print("Printing resource_list.txt:")
                f = open('resource_list', 'r')
                print(f.read().replace(",", "\n"))
                print("Printing sha256_list.txt:")
                f = open('sha256_list', 'r')
                print(f.read().replace(",", "\t"))
                print("Printing URL_list.txt:")
                f = open('URL_list', 'r')
                print(f.read().replace(",", "\n"))
                f.close()
            except Exception as e:
                print(e)
        # TODO: allow user to change API key
        elif choice == '3':
            print("Please ")
        elif choice == '5':
            return
def display_usage():
    print("""Usage main.py [option] <argument>\nOptions:
-f, --file   <File Path>      Upload a File.
-d, --dir    <Directory Path> Upload a Directory.
-u, --url    <URL>            Upload a URL.
-r, --report                  Check Reports.
-h, --help                    Show Help.""")