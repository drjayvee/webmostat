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
		pinId = 13 if params.get('room') == 'living' else 15
		setting = 'HIGH' if params.get('setting') == 'on' else 'LOW'

		command = 'sudo /usr/bin/gpiocli.py {pinId} {setting} -v'.format(pinId=pinId, setting=setting)
		subprocess.check_call(
			[command], shell=True
		)

		return command
#		return 'ok'

if __name__ == "__main__":
	app = application(urls, globals())
	app.run()
