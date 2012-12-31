import subprocess

config = {
    'thermostats': (
        (13, 'Living room'),
        (15, 'Bathroom')
    ),
    'gpioCommand': 'sudo /usr/bin/gpiocli.py {pin} {setting} -v -q'
}

class ThermostatException(Exception):
    pass

def setThermostat(pin, active):
    command = config['gpioCommand'].format(
        pin=pin, setting='HIGH' if active else 'LOW'
    )
    try:
        subprocess.check_call([command], shell=True)
    except subprocess.CalledProcessError:
        raise ThermostatException('Call to gpiocli failed')