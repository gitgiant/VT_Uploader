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
echo "Creating /etc/passwd-s3fs file."
sudo echo "$AccessKeyID:$SecretKey" > /etc/passwd-s3fs
sudo chmod 640 /etc/passwd-s3fs
echo "Please specify a path for the bucket to be mounted (suggested: /mnt/s3/), followed by [ENTER]:"
read MountPoint
echo "Creating mountpoint ${MountPoint} and temp cache /tmp/cache/"
sudo mkdir $MountPoint
sudo mkdir /tmp/cache/
sudo chmod 770 /tmp/cache/
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
git clone https://github.com/s3fs-fuse/s3fs-fuse.git
cd s3fs-fuse
./autogen.sh
./configure
make
sudo make install
cd ..
echo "Mounting the drive to {$MountPoint}."
sudo /usr/local/bin/s3fs -o allow_other,use_cache=/tmp/cache/,passwd_file=/etc/passwd-s3fs ${BucketName} ${MountPoint}
echo "Would you like to add automated Virus Total Uploader scans to the S3 Mount? [y/n]"
read choice
if [ ${choice} == 'y' ]; then
    echo "Adding watch and report automation to S3 mount."
    crontab -l > mycron
    echo "* * * * * /usr/local/bin/s3fs {$BucketName} {$MountPoint} -o allow_other,dbglevel=dbg,use_cache=/tmp/cache/,passwd_file=/etc/passwd-s3fs" >> mycron
    echo "* * * * * sleep 5 && cd $PWD && sudo python3 $PWD/main.py -w {$MountPoint}" >> mycron
    echo "* * * * * sleep 30 && cd $PWD && sudo python3 $PWD/main.py -q" >> mycron
    crontab mycron
    rm mycron
else
    crontab -l > mycron
    echo "* * * * * /usr/local/bin/s3fs {$BucketName} {$MountPoint} -o allow_other,dbglevel=dbg,use_cache=/tmp/cache/,passwd_file=/etc/passwd-s3fs" >> mycron
    crontab mycron
    rm mycron
fi
echo "Adding mount on boot entry to /etc/fstab/."
sudo echo "{$BucketName} {$MountPoint} fuse.s3fs _netdev,allow_other,dbglevel=dbg,retries=10,curldb,passwd_file=/etc/passwd-s3fs 0 0" >> /etc/fstab