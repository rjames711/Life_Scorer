#!/usr/bin/env bash
#*/30 * * * * /var/www/Life_Scorer/back_up_db.sh #copy to crontab
#Copy the contents of the db_files to backup locations
cp -r /var/www/Life_Scorer/Life_Scorer/db_files "/var/www/Life_Scorer/backups/db_files-$(date)"
cd /var/www/Life_Scorer/backups
#Get the last modified listings after 500 and remove them
sudo ls -t | tail -n +500 | xargs -d "\n" sudo rm -r
cd - 
