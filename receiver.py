#!/usr/bin/python3

'''
This script will start reading data from the serial port.
Once a data transfer i complete, it will print results
and start from beginning.

Author: Tomas Vavra <tomasxvavra@gmail.com>
'''

import serial
import time
import sys
try:
    import colorama
    from colorama import Fore, Back, Style
    colorama.init(autoreset=True)
except:
    print('python-colorama not availabe.')
    class Object:
        pass
    Fore = Object()
    Fore.RED = ''
    Fore.GREEN = ''

kB = 1024
MB = 1024 * 1024


### Configuration

# Serial port
PORT = '/dev/ttyACM0'       # If on host side
#PORT = '/dev/ttyGS0'       # If on device side

EXPECTED_CNT = 100 * MB     # Number of bytes expected to receive
PKT_SIZE = 256              # Number of bytes to read at once

STOP_ON_ERROR = False

total = 0   # RX bytes counter
try:
    s = serial.Serial(PORT, 9600, timeout=0.1)

    time.sleep(1)
    print('Start')
    t_last = time.time()
    
    reading = False     # When True, the transfer is in progress

    while True:
        #data = s.readall()
        data = s.read(PKT_SIZE)
        if data:
            if not reading:
                print('Transfer started')
                reading = True
                t_start = time.time()
            total += len(data)
            t_last = time.time()
        elif reading and time.time() - t_last > 1:
            # Transfer finished
            err = total - EXPECTED_CNT  # Number of missing bytes
            if not err:
                result = Fore.GREEN + '[OK]'
            else:
                result = Fore.RED + '[FAILED] ' + str(err) +\
                    '  bytes ({} %)'.format(err/EXPECTED_CNT*100)
            
            speed = total / MB / (t_last - t_start)
            
            print('Received: {} bytes at {} MB/s - {}'.format(total,speed,result))
            # Restart - get ready for new transfer
            reading = False
            total = 0
            if STOP_ON_ERROR and err:
                s.close()
                sys.exit(1)
                
except:
    print('\nReceived {}'.format(total))
    print('Closing serial...')
    s.close()
    print('Serial closed')