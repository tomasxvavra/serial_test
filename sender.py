#!/usr/bin/python3

'''
This script will send random data red from file over serial port.
It will create a 100 MB file when run for the first time.

Author: Tomas Vavra <tomasxvavra@gmail.com>
'''

import serial
import time
import os
import threading
import io
import random

kB = 1024
MB = 1024 * 1024

### Configuration

# Serial port
#PORT = '/dev/ttyACM0'      # If on host side
PORT = '/dev/ttyGS0'        # If on device side

FILE_NAME = 'data100.bin'   # Random data file name
CNT = 100 * MB              # Random data file size

N = int(100 * MB)           # Number of bytes to transfer at once
PKT_SIZE = 256              # Packet size

### Test

# Generate random file if it does not exist
if not os.path.isfile(FILE_NAME):
    print('Creating random file once')
    with open(FILE_NAME, 'wb') as f:
        f.write(os.urandom(CNT))

try:
    s = serial.Serial(PORT, 9600, timeout=1)
    
    with open(FILE_NAME, 'rb') as f:
        data = io.BytesIO(f.read(N))
    
    time.sleep(0.5)

    if True:
        # Do the transfer
        print('Sending ' + FILE_NAME)
        print('Data length: {}'.format(N))
        t0 = time.time()
        cnt = 0
        while True:
            #to_write = data.read(random.randint(1,PKT_SIZE))
            to_write = data.read(PKT_SIZE)
            
            if not to_write:
                break       # End of data
            
            cnt += s.write(to_write)
            
        # Transfer finished
        t1 = time.time()
        dt = t1 - t0
        speed = cnt/1024/1024 / dt
        print('Written {} bytes at {} MB/s'.format(cnt, speed))
        print('-Done-')
        
except:
    print('Closing serial...')
    s.close()
    print('Serial closed')
    raise
