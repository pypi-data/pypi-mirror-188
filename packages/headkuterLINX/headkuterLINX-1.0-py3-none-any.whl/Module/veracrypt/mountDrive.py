"""
    Title: HeadKuarter
    Module Name: mountDrive
    Language: Python
    Date Created: 7-05-2022
    Date Modified: 7-05-2022
    Description:
        ###############################################################
        ##  mounting Veracrypt Encrypted container                   ## 
        ###############################################################
 """

import subprocess 
import logging
import json
import os

creat_at = "C:\\privateVdisk\\encryptvdisk1.vc"
drive = "X" # any letter
master_password = "MySuperSecurePassword1!"

def mount_drive(creat_at,slot,master_password,pim):
    
    '''
    mount the encryted file to the drive
    '''
    success = False
    
    if slot != None:
        script = f"sudo veracrypt --text --mount {creat_at} /mnt --password {master_password} --pim {pim} --keyfiles \"\" --protect-hidden no --slot {slot} --verbose"
    else :
        script = f"sudo veracrypt --text --mount {creat_at} /mnt --password {master_password} --pim {pim} --keyfiles \"\" --protect-hidden no --verbose"
        
    result = subprocess.run(script,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
    #print(result)
    if result.returncode:
            return success
        
    success = True
    return success

def unmount(creat_at):
    #unmount encrypted drive
    success = False
    script = f"sudo veracrypt --text --dismount \"{creat_at}\""
    result = subprocess.run(script,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
    #print(result)
    if result.returncode:
            return success
        
    success = True
    return success

def unmount_at(drive):
    #unmount encrypted drive
    success = False
    script = f"sudo veracrypt --text --dismount {drive} --verbose "
    result = subprocess.run(script,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
    #print(result)
    if result.returncode:
            return success
        
    success = True
    return success