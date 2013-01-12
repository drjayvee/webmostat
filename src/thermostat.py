import os
import subprocess
import time
import logger.logger as logger

config = {
    'thermostats': (
        (13, 'Living room'),
        (15, 'Bathroom')
    ),
    'gpioCommand': 'sudo gpiocli.py {action} {pin} {setting} -v -q',
    'tempCommand': 'cat /sys/bus/w1/devices/28-0000042c0c6f/w1_slave |tail -1 |grep -Eo "[0-9]{4}"',
    'thermSensorOffset': 4,
    'logFile': os.path.abspath(os.path.dirname(__file__) + '/..') + '/log.sqlite3'
}

class ThermostatException(Exception):
    pass

def getPin(pin):
    command = config['gpioCommand'].format(
        action='get', pin=pin, setting=''
    )
    try:
        out = subprocess.check_output([command], shell=True)[:-1]   # range cuts off newline (and looks like a smiley)
        return True if out == 'HIGH' else False
    except subprocess.CalledProcessError:
        raise ThermostatException('Call to gpiocli failed')

def setPin(pin, active):
    command = config['gpioCommand'].format(
        action='set', pin=pin, setting='HIGH' if active else 'LOW'
    )
    try:
        subprocess.check_call([command], shell=True)
    except subprocess.CalledProcessError:
        raise ThermostatException('Call to gpiocli failed')

def getCurrentTemp():
    try:
        reading = subprocess.check_output(config['tempCommand'], shell=True)[:-1]
        return (int(reading) / 100.0) - config['thermSensorOffset']
    except subprocess.CalledProcessError:
        raise ThermostatException('Could not read temperature')

def logCurrentTemp():
    temp = getCurrentTemp()
    dbl = logger.DBLogger(config['logFile'])
    dbl.logEvent('temp', temp)
    return temp

def getTempsForLastDay():
    dbl = logger.DBLogger(config['logFile'])
    ts = int(time.time()) - 24*60*60    # now - one day's seconds
    dbl.getEvents('temp', ts)
