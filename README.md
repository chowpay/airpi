#Requirements
#tested on python3.8
pip install pyserial adafruit-io requests pyyaml

Small changes to : https://www.raspberrypi.org/blog/monitor-air-quality-with-a-raspberry-pi/ 

1.add username and aio key to sample_config.yml  
2.rename sample_config.yml to config.yml  
3.chown root cron.d/airpi  
4.create a symlink from /etc/cron.d/ to cron.d/airpi or just copy the file to cron.d   
