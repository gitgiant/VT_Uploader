# Used to display returned reports in JSON files
import webbrowser
import os
import time
import boto3

client = boto3.client('sns')

# TODO only display_scan_report is used
# def display_file_report(json_response):
#     print("Message: " + json_response['verbose_msg'])
#     print("Sha256: " + json_response['sha256'])
#     print("Permalink: " + json_response['permalink'])
#     print("______________________________________________")
#     handle_response_code(json_response)
#
#
# def display_URL_report(json_response):
#     print("Message: " + json_response['verbose_msg'])
#     print("Permalink: " + json_response['permalink'])
#     print("______________________________________________")
#     handle_response_code(json_response)
#
#
# def handle_response_code(json_response):
#     response_code = str(json_response['response_code'])
#     # response code of 1 means scans are finished and report is ready
#     if response_code == '1':
#         print("Response Code: " + response_code + ", Target is already present in virustotal database.")
#         launch_permalink(json_response)
#         return
#     # response code of -2 means the job is still queued
#     elif response_code == '-2':
#         print("Response Code: " + response_code + ", Target is queued for analysis.")
#         launch_permalink(json_response)
#         return
#     # response code of 0 means virus total has never seen the file and is still scanning it
#     elif response_code == '0':
#         print("Response Code: " + response_code + ", Target was not present in virustotal database.")
#         launch_permalink(json_response)
#         return
#     else:
#         print("ERROR: Invalid Response Code!")
#         return
#
#
# def launch_permalink(json_response):
#     openURL = input("Would you like to open the upload's permalink? (y/n):").lower()
#     while openURL != 'n':
#         if openURL == 'y':
#             print("Opening permalink...")
#             webbrowser.open(json_response['permalink'])
#             print("Returning to main menu.")
#             return
#         else:
#             openURL = input("Please enter correct input:").lower()
#
#     print("Returning to main menu.")
#     return


# TODO: Document, currently only reports on resource_list, not URL_list,
# TODO: Add threading to pull reports behind while user is viewing previous reports
def display_scan_report(json_response, verbose):
    if not is_non_zero_file('resource_list'):
        print("resource_list.txt is either empty or not found.")
        return
    # appended to for positive results, completed results
    try:
        positive_list = open('positive_list', 'a+')
        completed_list = open('completed_list', 'a+')
    except Exception as e:
        print(e)

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
            print(dicts['permalink'])
            print("Total Positives: " + str(dicts['positives']))
            print("Total Negatives: " + str(dicts['total'] - dicts['positives']))

            # Argument given in main.py for verbose report output
            if verbose:
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

            # Write the completed report to positive_list (if positive) and completed_list
            reportString = ("Filename: " + return_filename(dicts['sha256']) + "\nDate/Time: " + time.asctime()
                            + "\nsha256: " + dicts['sha256'] + '\n' + dicts['permalink'] + "\nTotal Positives: "
                            + str(dicts['positives']) + " Total Negatives: " + str(dicts['total'] - dicts['positives']) + '\n')
            for keys, values in ((k, v) for k, v in dicts['scans'].items() if v['detected']):
                positive_list.write(reportString + '\n')
                publish_sns(reportString)
            completed_list.write(reportString + '\n')
            # Delete line with response code 1 as it has been reported on
            with open('resource_list', 'r') as fin:
                data = fin.read().splitlines(True)
            with open('resource_list', 'w') as fout:
                fout.writelines(data[1:])
        # response code of -2 means the job is queued and still processing
        elif dicts['response_code'] == -2:
            pass
        # response code of 0 means virus total has never seen this file and has just added it to queue
        elif dicts['response_code'] == 0:
            pass


# TODO: combine into dispaly scan report
def display_URL_report(json_response, verbose):
    if not is_non_zero_file('URL_list'):
        print("URL_list is either empty or not found.")
        return
    # appended to for positive results, completed results
    try:
        positive_list = open('positive_list', 'a+')
        completed_list = open('completed_list', 'a+')
    except Exception as e:
        print(e)

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
            print("URL: " + dicts['url'])
            print(dicts['permalink'])
            print("Total Positives: " + str(dicts['positives']))
            print("Total Negatives: " + str(dicts['total'] - dicts['positives']))

            # Argument given in main.py for verbose report output
            if verbose:
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

            # Write the completed report to positive_list (if positive) and completed_list
            reportString = ("URL: " + dicts['url'] + "\nDate/Time: " + time.asctime()
                            + '\n' + dicts['permalink'] + "\nTotal Positives: " + str(dicts['positives'])
                            + " Total Negatives: " + str(dicts['total'] - dicts['positives']) + '\n')
            for keys, values in ((k, v) for k, v in dicts['scans'].items() if v['detected']):
                positive_list.write(reportString + '\n')
                publish_sns(reportString)
            completed_list.write(reportString + '\n')
            # Delete line with response code 1 as it has been reported on
            with open('URL_list', 'r') as fin:
                data = fin.read().splitlines(True)
            with open('URL_list', 'w') as fout:
                fout.writelines(data[1:])
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


def publish_sns(msg):
    response = client.publish(
        TopicArn='arn:aws:sns:us-west-2:057468764699:VT_positives',
        Message=msg,
        Subject='Virus Total Positive Found',
        MessageStructure='string',
    )