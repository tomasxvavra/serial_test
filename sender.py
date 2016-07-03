#!/usr/bin/python3

import serial
import time
import os
import threading
import io
import random

# Generate random file

kB = 1024
MB = 1024 * 1024

FILE_NAME = 'data100.bin'
CNT = 100 * MB

if not os.path.isfile(FILE_NAME):
    print('Creating random file once')
    with open(FILE_NAME, 'wb') as f:
        f.write(os.urandom(CNT))

N = 100 * MB
N = int(N)

PKT_SIZE = 256

try:
    s = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    
    with open('data100.bin', 'rb') as f:
        data = io.BytesIO(f.read(N))
    
    time.sleep(0.5)

    if True:
        print('Sending data100.bin')
        print('Data length: {}'.format(N))
        t0 = time.time()
        cnt = 0
        while True:
            #to_write = data.read(random.randint(1,PKT_SIZE))
            to_write = data.read(PKT_SIZE)
            
            if not to_write:
                break       # End of data
            
            cnt += s.write(to_write)
            
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
