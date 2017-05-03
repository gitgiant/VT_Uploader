import math
import time

try:
    import requests
except ImportError:
    print("Requests Module required.  Attempting to install using pip.")
    try:
        import pip
        pip.main(['install', requests])
    except Exception as e:
        print(e)
        print("Pip module not found!  Please go to http://docs.python-requests.org/en/master/ to install requests Module.")

from tokens import key

import report


# TODO: Scan resource_list.txt, find files that are completed and remove them, create queue, ADD URL REPORT CHECK
def check_file_scans(verbose):
    try:
        fileResourceList = open('resource_list', 'rb')
    except Exception as e:
        print(e)

    reportList = fileResourceList.readlines()

    numLines = sum(1 for line in open('resource_list', 'rb'))
    print("Resource_list has " + str(numLines) + " files left to check for reports.")

    # TODO: API allows 4 reports per request, add exception handling
    while len(reportList) > 0:
        start = time.time()
        # For some reason, API doesnt like a csv of just one entry, so if resource_list.txt has only 1 entry
        # Strip the comma and feed it into API
        if len(reportList) == 1:
            sha256 = reportList[0].decode("utf-8")
            # get rid of comma
            sha256 = sha256.rstrip(',')
            params = {'apikey': key, 'resource': sha256}
            # empty the list
            reportList = []
        else:
            sendList = ""
            for i in range(0, 4):
                try:
                    sendList+=reportList[i].decode("utf-8") + ','
                # if there are less than 4 jobs left
                except:
                    pass
            sendList.rstrip(',')
            params = {'apikey': key, 'resource': sendList}
            # snip off first 4 of reportList, as they are being sent off in sendList
            reportList = reportList[4:]
        headers = {
          "Accept-Encoding": "gzip, deflate",
          "User-Agent": "gzip,  Virus Total Uploader Tool"
        }
        try:
            response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params, headers=headers)
        except Exception as e:
            print(e)
        json_response = response.json()
        report.display_scan_report(json_response, verbose)
        end = time.time()
        retrieveTime = math.floor(end - start)
        # if user took longer than 15 seconds to view report, or there was just one report
        if retrieveTime > 15 or len(reportList)==1:
            retrieveTime = 15
        print("Waiting " + str(15 - retrieveTime) + " seconds to dispatch next request (Virus Total public API rules state 4 requests a minute).")
        time.sleep(15 - retrieveTime)


        numLines = sum(1 for line in open('resource_list', 'rb'))
        print("Resource_list has " + str(numLines) + " files left to check for reports.")

def check_URL_scans(verbose):
    try:
        urlList = open('URL_list', 'rb').readlines()
    except Exception as e:
        print(e)

    numLines = sum(1 for line in open('URL_list', 'rb'))
    print("URL_list has " + str(numLines) + " URLs left to check for reports.")

    # TODO: API allows 4 reports per request, add exception handling
    while len(urlList) > 0:
        start = time.time()
        # For some reason, API doesnt like a csv of just one entry, so if resource_list.txt has only 1 entry
        # Strip the comma and feed it into API
        if len(urlList) == 1:
            params = {'apikey': key, 'resource': urlList[0].decode("utf-8")}
            # empty the list
            urlList = []
        else:
            sendList = ""
            for i in range(0, 4):
                try:
                    sendList += urlList[i].decode("utf-8")
                # if there are less than 4 jobs left
                except:
                    pass
            sendList.rstrip(',')
            params = {'apikey': key, 'resource': sendList}
            # snip off first 4 of reportList, as they are being sent off in sendList
            urlList = urlList[4:]
        headers = {
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "gzip,  Virus Total Uploader Tool"
        }
        try:
            response = requests.post('https://www.virustotal.com/vtapi/v2/url/report', params=params, headers=headers)
        except Exception as e:
            print(e)
        json_response = response.json()
        report.display_URL_report(json_response, verbose)
        end = time.time()
        retrieveTime = math.floor(end - start)
        # if user took longer than 15 seconds to view report, or there was just one report
        if retrieveTime > 15 or len(urlList)==1:
            retrieveTime = 15
        print('Waiting ' + str(15 - retrieveTime) + ' seconds to dispatch next request (Virus Total public API rules state 4 requests a minute).')
        time.sleep(15 - retrieveTime)

        numLines = sum(1 for line in open('URL_list', 'rb'))
        print('URL_LIST has ' + str(numLines) + ' URLs left to check for reports.')


# TODO: Return a result of just a single target, not whole list, probably handled in check_file_scans
# def check_single_file_scan(sha256):
#     params = {'apikey': key, 'resource': sha256}
#     headers = {
#         "Accept-Encoding": "gzip, deflate",
#         "User-Agent": "gzip,  My Python requests library example client or username"
#     }
#     response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params, headers=headers)
#     json_response = response.json()
#     report.display_scan_report(json_response)
#
