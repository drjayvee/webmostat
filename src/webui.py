#!/usr/bin/python -tt

import web
import os
import json

urls = (
	'/', 'Control',
	'/?temp', 'Temp',
	'/?schedule', 'Schedule'
)

render = web.template.render('templates/')

class Control:
	def GET(self):
		return render.main('thermostat controls ', '/', 'Control')

class Temp:
	def GET(self):
		return render.main('current temperature', 'temp', 'Temps')

class Schedule:
	def GET(self):
		return render.main(render.schedule(), 'schedule', 'Schedule')

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
