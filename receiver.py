#!/usr/bin/python3

import serial
import time
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

EXPECTED_CNT = 100 * MB

PKT_SIZE = 256

total = 0
try:
    s = serial.Serial('/dev/ttyACM0', 9600, timeout=0.1)
    s.flushInput()

    time.sleep(1)
    print('Start')
    t_last = time.time()
    reading = False

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
            reading = False
            
            err = total - EXPECTED_CNT
            if not err:
                result = Fore.GREEN + '[OK]'
            else:
                result = Fore.RED + '[FAILED] ' + str(err) +\
                    '  bytes ({} %)'.format(err/EXPECTED_CNT*100)
            
            speed = total / MB / (t_last - t_start)
            
            print('Received: {} bytes at {} MB/s - {}'.format(total,speed,result))
            total = 0

    #s.close()
        
except:
    print('\nReceived {}'.format(total))
    print('Closing serial...')
    s.close()
    print('Serial closed')