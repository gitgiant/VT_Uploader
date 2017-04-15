# Used to display returned reports in JSON files
import webbrowser
import os

def display_file_report(json_response):
    print("Message: " + json_response['verbose_msg'])
    print("Sha256: " + json_response['sha256'])
    print("Permalink: " + json_response['permalink'])
    print("______________________________________________")
    handle_response_code(json_response)


def display_URL_report(json_response):
    print("Message: " + json_response['verbose_msg'])
    print("Permalink: " + json_response['permalink'])
    print("______________________________________________")
    handle_response_code(json_response)


def handle_response_code(json_response):
    response_code = str(json_response['response_code'])
    # response code of 1 means scans are finished and report is ready
    if response_code == '1':
        print("Response Code: " + response_code + ", Target is already present in virustotal database.")
        launch_permalink(json_response)
        return
    # response code of -2 means the job is still queued
    elif response_code == '-2':
        print("Response Code: " + response_code + ", Target is queued for analysis.")
        launch_permalink(json_response)
        return
    # response code of 0 means virus total has never seen the file and is still scanning it
    elif response_code == '0':
        print("Response Code: " + response_code + ", Target was not present in virustotal database.")
        launch_permalink(json_response)
        return
    else:
        print("ERROR: Invalid Response Code!")
        return


def launch_permalink(json_response):
    openURL = input("Would you like to open the upload's permalink? (y/n):").lower()
    while openURL != 'n':
        if openURL == 'y':
            print("Opening permalink...")
            webbrowser.open(json_response['permalink'])
            print("Returning to main menu.")
            return
        else:
            openURL = input("Please enter correct input:").lower()

    print("Returning to main menu.")
    return


# TODO: Document, currently only reports on resource_list, not URL_list
def display_scan_report(json_response):
    if not is_non_zero_file('resource_list'):
        print("resource_list.txt is either empty or not found.")
        return

    response_list =[]   # used to handle cases where there is one returned dict vs many dicts in a list
    # if json_response is a dict, then it is only 1 report, pack it into a list
    if isinstance(json_response, dict):
        response_list.append(json_response)
    # if json_response is a list, there are many reports, pack them into to a new list
    elif isinstance(json_response, list):
        for entry in json_response:
            response_list.append(entry)
    else:
        print("Returned Report is Malformed.")

    print("Reporting on status of queued scans:")
    for dicts in response_list:
        print("______________________________________________")
        print("Status: " + dicts['verbose_msg'])

        # Response code of 1 means the report is finished
        if dicts['response_code'] == 1:
            print("Filename: " + return_filename(dicts['sha256']))
            print("sha256: " + dicts['sha256'])
            print(dicts['permalink'])
            print("Total Positives: " + str(dicts['positives']))
            print("Total Negatives: " + str(dicts['total'] - dicts['positives']))

            choice = input("Would you like to display results from ([P]ositive Scans / [A]ll scans / [N]one):").lower()
            while choice != 'n':
                # print only detected results
                if choice == 'p':
                    # filter based on detected being TRUE
                    for keys, values in ((k, v) for k, v in dicts['scans'].items() if v['detected']):
                        print("{} {}".format(keys, values['version']))
                        print("Detected: " + str(values['detected']) + "\t\tResult: " + str(values['result'])+'\n')
                    break
                # print all results
                elif choice == 'a':
                    for keys, values in dicts['scans'].items():
                        print("{} {}".format(keys, values['version']))
                        print("Detected: " + str(values['detected']) + "\t\tResult: " + str(values['result']) + '\n')
                    break
                # exit
                elif choice == 'n':
                    break
                else:
                    print("Invalid input.")
                    choice = input("Would you like to display results from ([P]ositive Scans / [A]ll scans / [N]one):")
        # TODO: present more information to the user about queued jobs
        # response code of -2 means the job is queued and still processing
        elif dicts['response_code'] == -2:
            pass
        # response code of 0 means virus total has never seen this file and has just added it to queue
        elif dicts['response_code'] == 0:
            pass


def is_non_zero_file(fpath):
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


# go into sha256_list and return the file name that matches the sha hash that is on file
def return_filename(sha256):
    with open('sha256_list', "r") as sha256Read:
        for line in sha256Read:
            splitLine = line.split(',')
            if sha256 == splitLine[0]:
                sha256Read.close()
                return splitLine[1].rstrip('\n')
        print("sha256 not found in sha256_list.txt")
        return "NULL"
