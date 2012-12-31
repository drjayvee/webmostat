from web import application, webapi, template
import json
import subprocess

# to import thermostat, we have to add parent path, because this module is run as __main__
if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.abspath(os.path.dirname(__file__) + '../'))
import thermostat

urls = (
    '/(|temperature|schedule)', 'ShowPage',
    '/ajax/(\w+)', 'Ajax'
)

render = template.render(
    'templates/', base='base',
    globals={'thermostats': thermostat.config['thermostats']}
)

class ShowPage:
    def GET(self, page):
        return getattr(render, page or 'control')()


class Ajax:
    def POST(self, operation):
        params = webapi.input()

        if hasattr(self, operation) and callable(getattr(self, operation)):     # there is a function for operation
            args = {}
            for k, v in params.iteritems():                                     # json-decode parameters, and
                args[k] = json.loads(v)

            getattr(self, operation)(**args)                                    # call it with unpacked params
        else:
            raise webapi.BadRequest('Invalid method')

        return 'ok'

    def setThermostat(self, pin, active):
        try:
            thermostat.setThermostat(pin, active)
        except thermostat.ThermostatException as ex:
            raise webapi.InternalError(ex)

if __name__ == "__main__":
    app = application(urls, globals())
    app.run()
