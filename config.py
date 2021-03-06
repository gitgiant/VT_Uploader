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
Version 0.4     http://www.github.com/gitgiant

             Virus Total Uploader

Thank you for contributing to the virus total community."""

# Used for key check
from tokens import key

# TODO: Add aws key?

def configure_settings():
    choice = '0'

    while choice != '5':
        print("Please select from the following options:")
        print("1: Purge lists.")
        print("2: Print lists.")
        print("3: Change API key.")
        print("5: Return to main menu.")
        choice = input()
        if choice == '1':
            choice = input("This will clear all lists including already scanned files.  Are you sure? [y/n]: ").lower()
            if choice == 'y':
                print("Purging resource_list, sha256_list, URL_list, completed_list, and positive_list")
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
                f = open('completed_list', 'r+')
                f.seek(0)
                f.truncate()
                f.close()
                f = open('positive_list', 'r+')
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
                print("Printing resource_list:")
                f = open('resource_list', 'r')
                print(f.read().replace(",", "\n"))
                print("Printing sha256_list:")
                f = open('sha256_list', 'r')
                print(f.read().replace(",", "\t"))
                print("Printing URL_list:")
                f = open('URL_list', 'r')
                print(f.read().replace(",", "\n"))
                print("Printing completed_list:")
                f = open('completed_list', 'r')
                print(f.read())
                print("Printing positive_list:")
                f = open('positive_list', 'r')
                print(f.read())
                f.close()
            except Exception as e:
                print(e)
        # TODO: allow user to change API key
        elif choice == '3':
            key = input("Please Enter a valid API key:\n")
        elif choice == '5':
            return
def display_usage():
    print("""Usage main.py [option] <argument>\nOptions:
-f, --file   <File Path>      Upload a File.
-d, --dir    <Directory Path> Upload a Directory.
-w, --watch  <Directory Path> Watch a Directory and upload new files.
-u, --url    <URL>            Upload a URL.
-s, --scrape <URL>            Scrape a webpage, uploading all found URLs
-r, --report                  Check Reports.
-q, --quiet                   Check Reports but do not display.
-h, --help                    Show Help.""")


def display_help():
    print(header)
    print("""
What is the Virus Total Uploader?

Uploads a target file, directory, or URL to Virus Total.
If the target is not in the VT database, your scan will
be queued and completed shortly.

This tool is used to upload jobs and check if jobs have
completed, as well as display reports on completed jobs.

What is Virus Total?
Virus Total is a website where you can upload a file or
supply a URL, and VT will scan the target with around
60 different virus scanners from industry

Uploading to VT expands the database, discovers more
malicious files and false positives, and helps the
security community.

https://www.virustotal.com/en/about/

Requirements:

Virus Total public/private API key.
Python 3+.
Requests Python Module:
http://docs.python-requests.org/en/master/
Windows Forensics options available only on Windows.""")

    display_instructions()

    print("""
Performing a Manual Scan:

1. Run `main.py` and provide a valid target
(File path, Directory path, or URL)

2. If a target is not in the Virus Total database,
you will be placed in a queue

3. Queue should take anywhere from a minute to an hour,
depends on traffic and size of jobs

4. Select `Check if queued scans have completed`
in the main menu to see reports on completed jobs

5. The system keeps track of:
    * Waiting file jobs in the `resource_list` file.
    * Waiting URL jobs in the `URL_list` file.
    * Hashes of already uploaded jobs in the `sha256_list` file.
    * Completed reports in the `completed_list` file.
    * Positive reports in the `positive_list` file.

6. To purge the queued jobs list, go into
`Configure settings` and select `Purge lists`

About Scans, and public API rules:
Uploading to Virus Total and getting reports is an asynchronous process.
This means that an uploaded target's report is not immediately available.
Come back later and select the "check if queued scans have completed"
option to see completed reports.

Using a public API key, you are limited to 4 requests per minute.
A 'request' is either an upload, or 4 returned reports.
If you have a private API key, the request rate is greatly
increased (600 requests per minute).

To find out more about the Virus Total Public API rules:
https://www.virustotal.com/en/documentation/public-api/

Command Line usage:

main.py [option] <argument>
Options:
-f, --file   <File Path>      Upload a File.
-d, --dir    <Directory Path> Upload a Directory.
-u, --url    <URL>            Upload a URL.
-r, --report                  Check Reports.
-h, --help                    Show Help.""")

def display_instructions():
    print("""Set Up Instructions:

Using this tool requires a Virus Total key which is
linked with a VT account, in order to interact with
the API.

To obtain a VT account and public API key,
follow these instructions:

1. https://www.virustotal.com/en/documentation/virustotal-community/#dlg-join

2. Click 'Join our community'

3. Once an account has been set up and you are logged in,
click on the profile picture in the upper right corner

4. Select 'My API Key'

5. Edit the `giant_VT/tokens.py` file, insert your
API key into the key field (key='YOUR KEY GOES HERE')
""")

# Check for default key
if key == 'YOUR KEY GOES HERE':
    print('Virus Total Public API key needs to be correctly inputted into tokens.py file.')
    display_instructions()
    exit()