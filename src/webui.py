#!/usr/bin/python -tt

import web
import os
import json

urls = (
	'/', 'Control',
	'/temperature', 'Temperature',
	'/schedule', 'Schedule'
)

render = web.template.render('templates/', base='base', globals={'script': None})

class Control:
	def GET(self):
		return render.control()

class Temperature:
	def GET(self):
		return render.temperature()

class Schedule:
	def GET(self):
		return render.schedule()

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
