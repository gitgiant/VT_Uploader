import webbrowser


def display_file_report(json_response):
    print("Message: " + json_response['verbose_msg'])
    print("Sha256: " + json_response['sha256'])
    print("Permalink: " + json_response['permalink'])
    response_code = str(json_response['response_code'])
    print("______________________________________________")

    handle_response_code(json_response)


def display_URL_report(json_response):
    print("Message: " + json_response['verbose_msg'])
    print("Permalink: " + json_response['permalink'])
    print("______________________________________________")

    handle_response_code(json_response)


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
