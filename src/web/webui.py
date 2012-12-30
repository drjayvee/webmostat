#!/usr/bin/python -tt

from web import application, webapi, template
import json
import subprocess

urls = (
    '/(|temperature|schedule)', 'ShowPage',
    '/ajax/(\w+)', 'Ajax'
)

render = template.render('templates/', base='base')

class ShowPage:
    def GET(self, page):
        return getattr(render, page or 'control')()

class Ajax:
    def POST(self, operation):
        params = webapi.input()

        try:
            if hasattr(self, operation) and callable(getattr(self, operation)):     # there is a function for operation
                args = {}
                for k, v in params.iteritems():                                     # json-decode parameters, and
                    args[k] = json.loads(v)

                getattr(self, operation)( **args )                                  # call it with unpacked params
            else:
                raise webapi.BadRequest()
        except AttributeError:
            raise webapi.BadRequest()

        return 'ok'

    #TODO: move this to Thermostat class in parent package
    def setThermostat(self, pin, active):
        print 'setThermostat:', pin, active
        command = 'sudo /usr/bin/gpiocli.py {pin} {setting} -v -q'.format(
            pin=pin, setting='HIGH' if active else 'LOW'
        )
        try:
            subprocess.check_call([command], shell=True)
        except subprocess.CalledProcessError:
            raise webapi.InternalError()

if __name__ == "__main__":
    app = application(urls, globals())
    app.run()
