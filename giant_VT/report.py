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
    if response_code == '1':
        print("Response Code: " + response_code + ", Target is already present in virustotal database.")
        launch_permalink(json_response)
        return
    elif response_code == '-2':
        print("Response Code: " + response_code + ", Target is queued for analysis.")
        launch_permalink(json_response)
        return
    elif response_code == '0':
        print("Response Code: " + response_code + ", Target was not present in virustotal database.")
        launch_permalink(json_response)
        return
    else:
        print("Invalid Response Code!")
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


# TODO: Document
def display_scan_report(json_response):
    if not is_non_zero_file('resource_list'):
        print("resource_list.txt is either empty or not found.")
        return

    #Crashes when only 1 dict in resource_list
    print("Reporting on status of queued scans:")
    if len(json_response) < 12:
        for dicts in json_response:
            print("______________________________________________")
            print("Status: " + dicts['verbose_msg'])

            if dicts['response_code'] == 1:
                print("Filename: " + return_filename(dicts['sha256']))
                print("sha256: " + dicts['sha256'])
                print(dicts['permalink'])
                print("Total Positives: " + str(dicts['positives']))
                print("Total Negatives: " + str(dicts['total'] - dicts['positives']))

                choice = input("Would you like to display results from ([P]ositive Scans / [A]ll scans / [N]one):")
                while choice.lower != 'n':
                    if choice.lower() == 'p':
                        # filter based on detected being TRUE
                        for keys, values in ((k, v) for k, v in dicts['scans'].items() if v['detected']):
                            print("{} {}".format(keys, values['version']))
                            print("Detected: " + str(values['detected']) + "\t\tResult: " + str(values['result'])+'\n')
                        break
                    elif choice.lower() == 'a':
                        for keys, values in dicts['scans'].items():
                            print("{} {}".format(keys, values['version']))
                            print("Detected: " + str(values['detected']) + "\t\tResult: " + str(values['result']) + '\n')
                        break
                    elif choice.lower() == 'n':
                        break
                    else:
                        print("Invalid input.")
                        choce = input("Would you like to display results from ([P]ositive Scans / [A]ll scans / [N]one):")
            elif dicts['response_code'] == -2:
                pass
            elif dicts['response_code'] == 0:
                pass
    else:
        print("______________________________________________")
        print("Status: " + json_response['verbose_msg'])

        if json_response['response_code'] == 1:
            print("Filename: " + return_filename(json_response['sha256']))
            print("sha256: " + json_response['sha256'])
            print(json_response['permalink'])
            print("Total Positives: " + str(json_response['positives']))
            print("Total Negatives: " + str(json_response['total'] - json_response['positives']))

            choice = input("Would you like to display results from ([P]ositive Scans / [A]ll scans / [N]one):")
            while choice.lower != 'n':
                if choice.lower() == 'p':
                    # filter based on detected being TRUE
                    for keys, values in ((k, v) for k, v in json_response['scans'].items() if v['detected']):
                        print("{} {}".format(keys, values['version']))
                        print("Detected: " + str(values['detected']) + "\t\tResult: " + str(values['result']) + '\n')
                    break
                elif choice.lower() == 'a':
                    for keys, values in json_response['scans'].items():
                        print("{} {}".format(keys, values['version']))
                        print("Detected: " + str(values['detected']) + "\t\tResult: " + str(values['result']) + '\n')
                    break
                elif choice.lower() == 'n':
                    break
                else:
                    print("Invalid input.")
                    choce = input("Would you like to display results from ([P]ositive Scans / [A]ll scans / [N]one):")
        elif json_response['response_code'] == -2:
            pass
        elif json_response['response_code'] == 0:
            pass
def is_non_zero_file(fpath):
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

def return_filename(sha256):
    with open('sha256_list', "r") as sha256Read:
        for line in sha256Read:
            splitLine = line.split(',')
            if sha256 == splitLine[0]:
                return splitLine[1].rstrip('\n')
        print("sha256 not found in sha256_list.txt")
        return "NULL"