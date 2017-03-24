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
Version 0.2     http://www.github.com/gitgiant
Thank you for contributing to the virus total community.
Please be patient as scans may take awhile to complete."""

def configure_settings():
    choice = '0'

    while choice != '5':
        # TODO: configure settings
        print("Please select from the following options:")
        print("1: Purge lists.")
        print("2: Print lists.")
        # print("2: Auto check if if queued scans have completed upon launch.")
        print("5: Return to main menu.")
        choice = input()
        if choice == '1':
            choice = input("Are you sure? [y/n]: ").lower()
            if choice == 'y':
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
            elif choice == 'n':
                # exits
                choice == '5'
            else:
                print("Invalid input")
                pass
        if choice == '2':
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