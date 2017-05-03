#! /bin/bash
sudo /usr/local/bin/s3fs -o allow_other,use_cache=/tmp/cache,passwd_file=/home/ec2-user/aws mattias.huber /mnt/s3
