import logging

class Plugin():

	params = {
				"Allow":[],
				"Disallow":[],
				"Sitemap":[]
			 }

	def __init__(self, settings):
		logging.debug("[Robot] Init")
		pass

	def run(self, settings, content, fields):
		pass

	def teardown(self, settings):
		logging.debug("[Robot] Teardown")
		pass
		