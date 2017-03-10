import requests
from tokens import key
import report


# TODO: Scan resource_list.txt, find files that are completed and remove them
def check_file_scans():
    fileResourceList = open('resource_list', 'rb')

    params = {'apikey': key, 'resource': fileResourceList}

    headers = {
      "Accept-Encoding": "gzip, deflate",
      "User-Agent": "gzip,  My Python requests library example client or username"
      }
    response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params, headers=headers)
    json_response = response.json()
    report.display_scan_report(json_response)
