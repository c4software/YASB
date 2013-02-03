import logging
import shutil

class Plugin():
	def __init__(self, settings):
		pass

	def run(self, settings, content, fields):
		pass

	def teardown(self, settings):
		logging.info("[Static] Moving static files")
		if settings.get("static_settings") != "":
			# Remove old previous files
			shutil.rmtree(settings.get("output")+"/static/", ignore_errors=True)

			# If a static folder is specified we move all static file to the output folder
			logging.info("[Static] Move static files ({0}) to {1}static/".format(settings.get("static_settings"), settings.get("output")))
			shutil.copytree(settings.get("static_settings"), settings.get("output")+"/static/")
		else:
			logging.warn("[Static] No static folder specify.")