# TODO: Implement
import requests

params = {'apikey': '-YOUR API KEY HERE-', 'resource': '7657fcb7d772448a6d8504e4b20168b8'}
headers = {
  "Accept-Encoding": "gzip, deflate",
  "User-Agent" : "gzip,  My Python requests library example client or username"
  }
response = requests.post('https://www.virustotal.com/vtapi/v2/file/rescan',
 params=params)
json_response = response.json()