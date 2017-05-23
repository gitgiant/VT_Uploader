Virus Total Automated Upload System
---
Uploads a target file, directory, or URL to Virus Total.  If the target is not in the VT database, your scan will be queued and completed shortly.

This system is used to upload jobs and check if jobs have completed, as well as display reports on completed jobs.

Utilizing Amazon Web Services (AWS), Elastic Compute Cloud (EC2), and Simple Storage Service (S3), this system can be set up allow users to place files into a S3 bucket which will then be scanned automatically and user can be notified of any possible positives found.  

#### Requirements

* Virus Total public/private API key.

* Python 3+.

* <a href="http://docs.python-requests.org/en/master/" title="Requests Python Module"> Requests Python Module. </a>

* AWS integration requires an AWS account, S3 bucket, a set of access keys, and [s3fs](https://github.com/s3fs-fuse/s3fs-fuse).

#### What is Virus Total?
Virus Total is a website where you can upload a file or supply a URL, and VT will scan the target with around 60 different virus scanners from industry

Uploading to VT expands the database, discovers more malicious files and false positives, and helps the security community.

<a href="https://www.virustotal.com/en/about/" title="About Virus Total">
Click here to find out more about Virus Total.</a>

#### Virus Total API Key Installation Instructions
Using this tool requires a Virus Total key which is linked with a VT account, in order to interact with the API.  To obtain a VT account and public API key, follow these instructions:

1. <a href="https://www.virustotal.com/en/documentation/virustotal-community/#dlg-join">Click here to learn about joining the Virus Total community.</a>

2. Click `Join our community`.

3. Once an account has been set up and you are logged in, click on the profile picture in the upper right corner.

4. Select `My API Key`.

5. Edit the `tokens.py` file, insert your API key into the key field (key='YOUR KEY GOES HERE').

#### Performing a Manual Scan
1. Run `main.py` and provide a valid target (File path, Directory path, or URL).

2. If a target is not in the Virus Total database, you will be placed in a queue.

3. Queued job should take anywhere from a few seconds to an minute, depends on traffic and file size (Public API is limited to a file size less than 32 MB).

4. Select `Check if queued scans have completed` in the main menu to see reports on completed jobs .

5. The system keeps track of:
    * Waiting file jobs in the `resource_list` file.
    * Waiting URL jobs in the `URL_list` file.
    * Hashes of already uploaded jobs in the `sha256_list` file.
    * Completed reports in the `completed_list` file.
    * Positive reports in the `positive_list` file.
6. To purge these lists, go into `Configure settings` and select `Purge lists`.

#### Amazon Web Services Functionality:
Utilizing Amazon Web Services (AWS), Elastic Compute Cloud (EC2), and Simple Storage Service (S3), this system can be set up allow users to place files into a S3 bucket which will then be scanned automatically and user can be notified of any possible positives found.  All of this is possible utilizing AWS free tier.

1. The User places a file they wish to scan into the S3 bucket, such as `http://testbucket.s3.amazonaws.com`
2. A dedicated EC2 instance watches the bucket, detects the new file, and uploads the file to Virus Total.
3. The EC2 instance waits until Virus Total returns a completed report.
4. If any positives are found the instance notifies the user, otherwise the report is added to the completed list.

![AWS Functionality](http://i.imgur.com/NYX6LWV.png "AWS Functionality")

#### Setting Up AWS Functionality
1. If you do not already have an S3 bucket, please log into to the [AWS Management Console](https://aws.amazon.com/console/). Under `All Services > Storage`, select `S3` and then select `+ Create Bucket`.

2. On an EC2 instance, extract this repository to a public folder, such as `/home/` (installing into a user's private folder will not work).

3. Change directory into the directory where you extracted the repository, with a command such as `cd /home/VT_uploader`.

4. Make the `mount_bucket.sh` script executable, by doing `sudo chmod 700 ./mount_bucket.sh`.

5. Run `sudo ./mount_bucket.sh`.  This will mount the S3 bucket into the filesystem using [s3fs](https://github.com/s3fs-fuse/s3fs-fuse).

6. Enter your bucket name (note: this is just the name of the bucket, not the URL path of the bucket).

7. To obtain a new AWS Access Key, please log into [AWS Management Console](https://aws.amazon.com/console/).  Click on the account name in the top right corner, then select `My Security Credentials`.  Then select `Access Keys` and then `Create New Access Key`.  

8. A prompt shows an Access Key and its corresponding Secret Key only once.  To save the keys for later, download the key .csv file, and open it to obtain the Access Key ID and Secret Key.

9. Entered the access key, followed by the secret key.

10. Enter a mount-point to mount the S3 bucket (suggested: `/mnt/s3`).

11. If you want the EC2 instance to automatically upload files found in the bucket and pull reports, select `y` when prompted.  This will add an automated cron job task that makes the system scan the bucket and get reports every minute.

#### About Scans, and public API rules

Uploading to Virus Total and getting reports is an asynchronous process.  This means that an uploaded target's report is not immediately available.  Come back later and select the `Check if queued scans have completed` option to see completed reports.  

Using a public API key, you are limited to 4 requests per minute (once every 15 seconds).  A 'request' is either an upload, or 4 returned reports.  If you have a private API key, the request rate is greatly increased (600 requests per minute).

[Click here to find out more about the Virus Total public API rules.](https://www.virustotal.com/en/documentation/public-api/)

#### Command Line usage:
```
main.py [option] <argument>
Options:
-f, --file   <File Path>      Upload a File. 
-d, --dir    <Directory Path> Upload a Directory.  
-u, --url    <URL>            Upload a URL.
-r, --report                  Check Reports.
-h, --help                    Show Help.
```
