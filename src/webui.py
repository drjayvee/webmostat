#!/usr/bin/python -tt

import web
import json

urls = (
	'/', 'index',
	'/about', 'about'
)

render = web.template.render('templates/')

class index:
	def GET(self):
		return 'GET query parameters:' + json.dumps(web.input(), indent=4)

class about:
	def GET(self):
		return render.about()

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
