import requests
from giant_VT.tokens import key
from giant_VT import report


# TODO: Scan resource_list.txt, find files that are completed and remove them
def check_file_scans():

    fileResourceList = open('resource_list', 'rb')
    #num_lines = sum(1 for line in fileResourceList)
    linelist = fileResourceList.readlines()

    # For some reason, API doesnt like a csv of just one entry, so if resource_list.txt has only 1 entry
    # Strip the comma and feed it into API
    if len(linelist) == 1:
        sha256 = linelist[0].decode("utf-8")
        # get rid of comma
        sha256 = sha256.rstrip(',')
        params = {'apikey': key, 'resource': sha256}
    else:
        params = {'apikey': key, 'resource': fileResourceList}

    headers = {
      "Accept-Encoding": "gzip, deflate",
      "User-Agent": "gzip,  My Python requests library example client or username"
      }
    response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params, headers=headers)
    json_response = response.json()
    report.display_scan_report(json_response)

# TODO: Return a result of just a single target, not whole list
def check_single_file_scan(sha256):
    params = {'apikey': key, 'resource': sha256}
    headers = {
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "gzip,  My Python requests library example client or username"
    }
    response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params, headers=headers)
    json_response = response.json()
    report.display_scan_report(json_response)

