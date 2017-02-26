#!/bin/bash 
log_name=`date +"%F_%H-%M-%S"`
python -u ./existential_rick_bot.py > ./out_$log_name.log 2> ./error_$log_name.log
