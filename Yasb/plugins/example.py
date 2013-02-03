import logging

class Plugin():
	def __init__(self, settings):
		logging.debug("[Example] Init")
		pass

	def run(self, settings, content, fields):
		logging.debug("[Example] Run")
		pass

	def teardown(self, settings):
		logging.debug("[Example] Teardown")
		pass
		