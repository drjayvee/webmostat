#!/usr/bin/python -tt

from web import application, webapi, template
import subprocess

urls = (
    '/(|temperature|schedule)', 'ShowPage',
    '/ajax', 'Ajax'
)

render = template.render('templates/', base='base')

class ShowPage:
    def GET(self, page):
        return getattr(render, page or 'control')()

class Ajax:
    def POST(self):
        params = webapi.input()

        try:
            operation = params.operation
            if operation == 'setThermostat':
                self.setThermostat(
                    13 if params.room == 'living' else 15,
                    True if params.setting == 'on' else False
                )
            else:
                raise webapi.BadRequest()
        except AttributeError:
            raise webapi.BadRequest()

        return 'ok'

    #TODO: move this to Thermostat class in parent package
    def setThermostat(self, pinId, active):
        command = 'sudo /usr/bin/gpiocli.py {pinId} {setting} -q'.format(
            pinId=pinId, setting='HIGH' if active else 'LOW'
        )
        try:
            subprocess.check_call([command], shell=True)
        except subprocess.CalledProcessError:
            raise webapi.InternalError()

if __name__ == "__main__":
    app = application(urls, globals())
    app.run()
