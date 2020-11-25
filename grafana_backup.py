#!/usr/bin/env python
import os
import subprocess
import logging
import sys
import bcolors as b

logging.basicConfig(filename="/var/log/grafana_dashboard_bkp.out",level = logging.INFO,format = '%(levelname)s %(asctime)s %(message)s',datefmt = '%Y-%m-%d %H:%M:%S',filemode = 'a')
logger = logging.getLogger()

#set environment variable for ignoring https 
os.environ['NODE_TLS_REJECT_UNAUTHORIZED']='0'

#change backup directory and  make sure that backup directory having write premission for taking backup
BKP_DIR="/opt/GRAFANA-BKP"


print("""{}

====================  Grafana Dashboard Backup using wizzy ====================

Make sure that wizzy installed and  wizzy initialisation and configuration done 
in backup directory.
==============================================================================

{}""".format(b.WARN,b.END))

def check_bkp_dir():
    try:
        if not os.path.isdir(BKP_DIR):
            print("{} Mentioned backup path :{} ,not present,create Backup path,or specify other backup path and initailsze wizzy setup in same backup path  {}".format(b.ERRMSG,BKP_DIR,b.END))            
            sys.exit(2)
        else:
            print("{} Backup path: {} present {}".format(b.OKMSG,BKP_DIR,b.END))
    except Exception as e:
        logger.error("Exception occoured in check_bkp_dir:{}".format(e))


def check_wizzy():
    try:
        
        check_stdout=subprocess.run(['wizzy', 'version'], stdout=subprocess.PIPE)
        print(r"{} wizzy already present, starting taking backup {}".format(b.OKMSG,b.END))

    except FileNotFoundError:
        logger.error("Wizzy not installed,Install and configure wizzy first ")
        print("{} Wizzy not installed,Install and configure wizzy first {}".format(b.ERRMSG,b.END))
        sys.exit(2)



def  take_wizzy_dashboard_backup():
    try:
        
        os.chdir(BKP_DIR)
        
        check_stdout=subprocess.run(['wizzy', 'import','dashboards'], stdout=subprocess.PIPE)
        
        if check_stdout.returncode !=0:
            
            logger.error("Error while  taking dashboards backup")
            print("{} Error while  taking dashboard backup {}".format(b.ERRMSG,b.END))
        
        else:
            logger.info("Backup for dashboards Taken successfully")
            print("{} Backup for dashboards Taken successfully {}".format(b.OKMSG,b.END))
        
        
    except Exception as e:
        logger.error('Exception occoured while taking grafana dashboard backup:{}'.format(e))    
        print("{} Exception occoured while taking grafana dashboard backup {}".format(b.ERRMSG,b.END))

def  take_wizzy_datasource_backup():
    try:
        
        os.chdir(BKP_DIR)
        
        check_stdout=subprocess.run(['wizzy', 'import','datasources'], stdout=subprocess.PIPE)
        
        if check_stdout.returncode !=0:
            
            logger.error("Error while  taking datasources backup")
            print("{} Error while  taking datasources backup {}".format(b.ERRMSG,b.END))
        else:
            logger.info("Backup for datasources successfully")
            print("{} Backup for datasources Taken successfully {}".format(b.OKMSG,b.END))
        
        
    except Exception as e:
        logger.error('Exception occoured while taking grafana datasources backup:{}'.format(e))    
        print("{} Exception occoured while taking grafana datasources backup {}".format(b.ERRMSG,b.END))

def Main():
    try:
        
        check_bkp_dir()
        check_wizzy()
        take_wizzy_dashboard_backup()
        take_wizzy_datasource_backup()
        
        
    except Exception as e:
        logger.error("Exception occured in main:{}".format(e))
        print("{} Exception occoured in Main {}".format(b.ERRMSG,b.END))

if __name__=='__main__':
    Main()
