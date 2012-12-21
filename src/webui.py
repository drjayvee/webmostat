#!/usr/bin/python -tt

import web
import os
import json

urls = (
	'/(|temperature|schedule)', 'ShowPage'
)

render = web.template.render('templates/', base='base', globals={'script': None})

class ShowPage:
	def GET(self, page):
		return getattr(render, page or 'control')()

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
