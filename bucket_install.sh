#!/bin/bash
echo "This tool allows the user to mount an Amazon S3 bucket as a local drive using s3fs."
echo "If you do not already have an S3 bucket, please log into to https://aws.amazon.com/console/,"
echo "Under All Services > Storage, select S3 and then select '+ Create Bucket'."
echo "Please enter the bucket name and then press [ENTER]:"
read BucketName
echo "To obtain a new AWS Access Key, please log into AWS management Console @ https://aws.amazon.com/console/"
echo "Click on the account name in the top right corner, then select 'My Security Credentials'."
echo "Then select 'Access Keys' and then 'Create New Access Key'."
echo "Download the key .csv file, and open it to obtain the Access Key ID and Secret Key."
echo "Please enter the AWS Access Key ID, followed by [ENTER]:"
read AccessKeyID
echo "Please enter the AWS Secret Key ID, followed by [ENTER]:"
read SecretKey
echo "Creating ~/.passwd-s3fs file."
echo $AccessKeyID:$SecretKey > ~/.passwd-s3fs
chmod 600 ~/.passwd-s3fs
echo "Creating mountpoint /mnt/s3/ and temp cache /tmp/cache/"
sudo mkdir /mnt/s3/
sudo mkdir /tmp/cache/
chmod 770 /tmp/cache/
echo "Downloading Dependencies with either apt-get or yum."
if [ -n "$(command -v apt-get)" ]; then
	echo "apt-get detected."
	sudo apt-get install automake autotools-dev g++ git libcurl4-gnutls-dev libfuse-dev libssl-dev libxml2-dev make pkg-config
if [ -n "$(command -v yum)" ]: then
	echo "yum detected."
	sudo yum install automake fuse fuse-devel gcc-c++ git libcurl-devel libxml2-devel make openssl-devel
echo "Pulling and installing s3fs from github."
cd ~/
git clone https://github.com/s3fs-fuse/s3fs-fuse.git
cd s3fs-fuse
./autogen.sh
./configure
make
sudo make install
echo "Mounting the drive to /mnt/s3/."
/usr/local/bin/s3fs -o allow_other,passwd_file=~/.passwd-s3fs,use_cache=/tmp/cache/ $BucketName /mnt/s3/ 
echo "Adding mount cronjob."
crontab -l > mycron
echo "59 * * * * /usr/local/bin/s3fs -o allow_other,passwd_file=~/.passwd-s3fs,use_cache=/tmp/cache/ $BucketName /mnt/s3/" >> mycron
crontab mycron
rm mycron