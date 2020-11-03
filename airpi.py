import sys
print(sys.path)
sys.path.append("/home/pi/scripts/airpi/venv38/lib/python3.8/site-packages")
import yaml
import backoff
import serial
import time
from Adafruit_IO import Client


#Load yaml configuration file
try:
    with open('config.yml') as f:
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
    data = []
    for index in range(0,10):
        datum = ser.read()
        data.append(datum)

    pmtwofive = int.from_bytes(b''.join(data[2:4]),byteorder = 'little') / 10
    aio.send('kingswoodtwofive', pmtwofive)
    pmten = int.from_bytes(b''.join(data[4:6]),byteorder = 'little') / 10
    aio.send('kingswoodten', pmten)
    print('PM2.5 = {0}\nPM10 = {1}'.format(pmtwofive,pmten))
    time.sleep(10)

