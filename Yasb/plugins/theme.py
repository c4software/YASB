import logging
import shutil

class Plugin():
	def __init__(self, settings):
		pass

	def run(self, settings, content, fields):
		pass

	def teardown(self, settings):
		logging.info("[Theme] Moving theme static files")
		# Remove old previous files
		shutil.rmtree(settings.get("output")+"/theme/", ignore_errors=True)

		# Move all files from the theme to the output folder
		logging.info("[Theme] Move theme files ({0}static/) to {1}theme/".format(settings.get("theme"), settings.get("output")))
		shutil.copytree(settings.get("theme")+"/static/", settings.get("output")+"/theme/")