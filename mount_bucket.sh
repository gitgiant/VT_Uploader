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
echo AKIAIQBD6SPZRWHP37FQ:UmhcDk24f9dJsi+2lv6ar9HiqQ7y0ZJ9ZwEqK4FN > /etc/passwd-s3fs
sudo chmod 640 /etc/passwd-s3fs
echo "Creating mountpoint /mnt/s3/ and temp cache /tmp/cache/"
sudo mkdir /mnt/s3/
sudo mkdir /tmp/cache/
chmod 770 /tmp/cache/
echo "Downloading Dependencies with either apt-get or yum."
if [ -n "$(command -v apt-get)" ]; then
	echo "apt-get detected."
	sudo apt-get install automake autotools-dev g++ git libcurl4-gnutls-dev libfuse-dev libssl-dev libxml2-dev make pkg-config
fi
if [ -n "$(command -v yum)" ]; then
	echo "yum detected."
	sudo yum install automake fuse fuse-devel gcc-c++ git libcurl-devel libxml2-devel make openssl-devel
fi
echo "Pulling and installing s3fs from github."
cd ~/
git clone https://github.com/s3fs-fuse/s3fs-fuse.git
cd s3fs-fuse
./autogen.sh
./configure
make
sudo make install
echo "Mounting the drive to /mnt/s3/."
sudo /usr/local/bin/s3fs -o allow_other,use_cache=/tmp/cache/,passwd_file=/etc/passwd-s3fs ${BucketName} /mnt/s3/
#echo "Would you like to add automated Virus Total Uploader scans to the S3 Mount? [y/n]"
#read choice
#if [ ${choice,,} == 'y' ]; then
echo "Adding watch and report automation to S3 mount."
crontab -l > mycron
echo "* * * * * sudo python3 $PWD/main.py -w /mnt/s3/" >> mycron
echo "* * * * * sudo python3 $PWD/main.py -r" >> mycron
crontab mycron
rm mycron
#fi
echo "Adding mount cronjob."
crontab -l > mycron
echo "* * * * * /usr/local/bin/s3fs -o _netdev,allow_other,dbglevel=dbg,use_cache=/tmp/cache/,curldb,passwd_file=/etc/passwd-s3fs $BucketName /mnt/s3/ % &>/tmp/mycommand.log" >> mycron
crontab mycron
rm mycron

#echo "Adding mount on boot entry to /etc/fstab/."
#echo "$BucketName /mnt/s3 fuse.s3fs _netdev,allow_other,dbglevel=dbg,retries=10,curldb,passwd_file=/etc/passwd-s3fs 0 0" >> /etc/fstab