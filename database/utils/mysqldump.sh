#!/bin/bash

folder="/home/giuseppe/apartments/database/"

now=$(date +"%Y%m%d%H%M") # or whatever pattern you desire

mysqldump -u root -pGg20042012!$ apartments > "${folder}apartments-$now.sql"

noOfBackups="$(ls -l ${folder}*.sql | grep -v ^l | wc -l)"

if [ "$noOfBackups" -gt "10" ]
then
    oldest="$(ls $folder -lt | grep -v '^d' | tail -1 | awk '{print $NF}')"
    rm -f "${folder}${oldest}"
fi