import webbrowser
import pprint
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
        #display_scan_report(json_response)
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
            print("Would you like to open the upload's permalink? (y/n):")
            openURL = input("Please enter correct input.").lower()

    print("Returning to main menu.")
    return

# TODO: Document
def display_scan_report(json_response):
    if not is_non_zero_file('resource_list'):
        print("resource_list.txt is either empty or not found.")
        return

    print("Reporting on status of queued scans:")
    for dicts in json_response:
        if dicts['response_code'] == 1:
            print("______________________________________________")
            print(dicts['verbose_msg'])
            print("sha256: " + dicts['sha256'])
            print(dicts['permalink'])

            print("Total Positives: " + str(dicts['positives']))
            print("Total Negatives: " + str(dicts['total'] - dicts['positives']))

            choice = input("Would you like to display results from " + str(dicts['total']) + " scans? (y/n)")
            if choice == 'y':
                for keys, values in dicts['scans'].items():
                    print(keys)
                    print("Detected: " + str(values['detected']) + "\tVersion: " + values['version'] + '\n')

                    # print("Percent Positive: ") + float(positive/total).round(2)
            # print("Percent Negative: ") + float(negative/total).round(2)
            # if float(negative/total) > .95):
            #     print("Target is +95% negative, most likely safe.")
        elif dicts['response_code'] == -2:
            print("______________________________________________")
            print(dicts['verbose_msg'])
            print("scan_id: " + dicts['scan_id'])

def is_non_zero_file(fpath):
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0