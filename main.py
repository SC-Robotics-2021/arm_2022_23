"""
AUTHOR: Max Rehm & Matin Qurbanzadeh
Project: Odrive Motor configuration
Date: 10/19/2022
"""

from calibrate import calib_motor
from configure import config_motor
from find_serial import get_all_odrives
from test_motor import test_motor
from loguru import logger
import threading
import time
import odrive



if __name__ == "__main__":

    odrv0BLAH = odrive.find_any()
    
    poo = odrv0BLAH.serial_number
    print(poo)

    poo1 = hex(odrv0BLAH.serial_number)
    print(poo1)

    poo2 = poo1.upper()
    print(poo2)

    poo3 = poo2.replace('0X','')

    odrv0 = str(poo3)
    print(odrv0)


    config_motor(odrv0, 0, True, False) 
    logger.debug("finished 00")

    
    calib_motor(odrv0, 0) 
    logger.debug("finished 00")
