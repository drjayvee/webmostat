import subprocess

config = {
    'thermostats': (
        (13, 'Living room'),
        (15, 'Bathroom')
    ),
    'gpioCommand': 'sudo gpiocli.py {action} {pin} {setting} -v -q'
}

class ThermostatException(Exception):
    pass

def getThermostat(pin):
    command = config['gpioCommand'].format(
        action='get', pin=pin, setting=''
    )
    try:
        out = subprocess.check_output([command], shell=True)[:-1]   # range cuts off newline (and looks like a smiley)
        return True if out == 'HIGH' else False
    except subprocess.CalledProcessError:
        raise ThermostatException('Call to gpiocli failed')

def setThermostat(pin, active):
    command = config['gpioCommand'].format(
        action='set', pin=pin, setting='HIGH' if active else 'LOW'
    )
    try:
        subprocess.check_call([command], shell=True)
    except subprocess.CalledProcessError:
        raise ThermostatException('Call to gpiocli failed')