#!/usr/bin/python
import logging
import psutil
import requests
import json

with open('keys.json') as fh:
	config = json.loads(fh.read())
stream_id = config['publicKey']
private_key = config['privateKey']

# setup log
log = logging.getLogger('')
log.setLevel(logging.DEBUG)

# create console handler and set level to info
log_format = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(log_format)
log.addHandler(ch)

# create file handler and set to debug
fh = logging.FileHandler('logger.log')
fh.setFormatter(log_format)
log.addHandler(fh)

log.info("started")

payload = { "private_key": private_key }

# pids
payload['processes'] = len(psutil.pids())

# cpu
payload['cpu_percent'] = psutil.cpu_percent(interval=2)

# disk
payload['disk_percent'] = psutil.disk_usage('/').percent

# mem
payload['memory_percent'] = psutil.virtual_memory().percent

# cpu temp
bbb_temp_file = '/sys/class/hwmon/hwmon0/device/temp1_input'
pi_temp_file  = '/sys/devices/virtual/thermal/thermal_zone0/temp'
with open(pi_temp_file, 'r') as f:
    cpu_temp = float(f.readline().split()[0]) / 1000
    payload["cpu_temp"] = cpu_temp

# uptime
with open('/proc/uptime', 'r') as f:
    uptime_seconds = float(f.readline().split()[0])
    payload["uptime"] = uptime_seconds


# log it
r = requests.get(config['inputUrl'], params=payload)
log.debug("get status = %d" % r.status_code)

log.info("finished")
