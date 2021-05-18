#aho Chan
#Modified script from https://www.raspberrypi.org/blog/monitor-air-quality-with-a-raspberry-pi/
#11/03/2020

import os
import sys
sys.path.append("/home/pi/scripts/airpi/venv38/lib/python3.8/site-packages")
import yaml
import serial
import time
import argparse
from Adafruit_IO import Client


#flag parser configs
prog_name = os.path.basename(__file__)
usage = "\n"+"Example:"+"\n"+"python "+prog_name+" --a"
parser = argparse.ArgumentParser(description=usage)
parser.add_argument("--d", action = 'store_true' , help='displays debugging code on screen ie --d')
args = parser.parse_args()


#Disable display on screen for debugging
def display(msg):
    if args.d:
        print (msg)
    else:
        pass


display(sys.path)

#Load yaml configuration file
try:
    with open('/home/pi/scripts/airpi/config.yml') as f:
        #Keys : ['username', 'password', ]
        yaml_data = yaml.load(f,Loader=yaml.FullLoader)
except Exception as e :
    #logging.error('missing config.yml file: {0}'.format(str(e)),exc_info=True)
    print ('missing config.yml file: {0}'.format(str(e)))

username = yaml_data['username']
password = yaml_data['password']

#aio = Client('username','adafurit-key')
aio = Client(username,password)

#Check what feeds are available:
#curl -H "X-AIO-Key: {adafruit-key}" https://io.adafruit.com/api/v2/{username}/feeds/

ser = serial.Serial('/dev/ttyUSB0')

while True:
    try:
        data = []
        for index in range(0,10):
            datum = ser.read()
            data.append(datum)

        pmtwofive = int.from_bytes(b''.join(data[2:4]),byteorder = 'little') / 10
        aio.send('kingswoodtwofive', pmtwofive)
        pmten = int.from_bytes(b''.join(data[4:6]),byteorder = 'little') / 10
        aio.send('kingswoodten', pmten)
        display('PM2.5 = {0}\nPM10 = {1}'.format(pmtwofive,pmten))
        time.sleep(10)
    except:
        print("issue connecting")


