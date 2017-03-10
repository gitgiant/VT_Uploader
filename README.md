###Virus Total Uploader
#### 
Uploads a target file or URL to Virus Total.  If the target is not in the VT database, your scan will be queued and completed shortly.
This tool is used to upload jobs and check if jobs have completed, as well as display reports on completed jobs.
####What is Virus Total?
Virus Total is a website where you can upload a file or supply a URL, and VT will scan the target with around 60 different virus scanners from industry

Uploading to VT expands the database, discovers more malicious files and false positives, and helping the security community.

<a href="https://www.virustotal.com/en/about/" title="About Virus Total">
Click here to find out more about Virus Total</a>

####Instructions
Using this tool requires a Virus Total key which is linked with a VT account, in order to interact with the API.

1.) <a href="https://www.virustotal.com/en/documentation/virustotal-community/#dlg-join" title=Join our Community">
Click here to learn about joining the Virus Total community</a>

2.) Click 'Join our community'

3.) Once an account has been set up and you are logged in, click on the profile picture in the upper right corner

4.) Select 'My API Key'

5.) Edit the `giant_VT/tokens.py` file, insert your API key into the key field

`key='YOUR KEY GOES HERE'`

6.) Run `main.py` and provide a valid file path (less than 32 MB) or URL

7.) If a target is not in the Virus Total database, you will be placed in a queue

8.) Queue should take anywhere from a minute to an hour, depends on traffic and size of jobs

9.) Select `Check if queued scans have completed` in the main menu to see reports on completed jobs 

10.) To purge the queued jobs list, go into `Configure settings` and select `Purge lists`
