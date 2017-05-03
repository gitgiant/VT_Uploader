#! /bin/bash
cd "$(dirname "$0")";
echo $PWD$;
sudo python3 ~/mattias-huber-capstone2017/main.py -r;
cat ~/mattias-huber-capstone2017/completed_list;

