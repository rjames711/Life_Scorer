#!/usr/bin/env bash
cp -r /var/www/Life_Scorer/Life_Scorer/db_files "/var/www/Life_Scorer/backups/db_files-$(date)"
cd /var/www/Life_Scorer/backups
sudo ls -t | tail -n +50 | xargs -d "\n" sudo rm -r
ls -lrt
ls | wc -l
cd - 
