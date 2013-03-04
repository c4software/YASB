import logging

# Example of parameters you can define in your params.py:
# "scss_settings":	{
#					"files":[
#								('main.scss','main.css')
#							],
#					"path":"./theme/valentin/static/styles/"
#					}
#

class Plugin():
	css = None
	scss_set  = [] # Collection of scss to "compile"
	scss_path = ""

	def __init__(self, settings):
		try:
			from scss import Scss
			self.css = Scss(scss_opts = {'compress_reverse_colors': False})
		except Exception as e:
			logging.error("[SCSS] To use this plugin you need to install pyScss (example: pip install pyScss)")
			return None

		try:
			if settings.get("scss_settings", None):
				self.scss_set = settings.get("scss_settings")["files"]
				self.scss_path = settings.get("scss_settings")["path"]
			else:
				logging.error("[SCSS] Can't import parameters.")
		except Exception as e:
			logging.error("[SCSS] Can't import parameters.")

	def run(self, settings, content, fields):
		pass

	def teardown(self, settings):
		logging.info("[SCSS] Start Compiling CSS")
		if self.css:
			for scss,css in self.scss_set:
				logging.info("[SCSS] Compiling : {0}{1}".format(self.scss_path,scss))
				# TODO write file to disc
				try:
					f = open(self.scss_path+scss,"r")
					output_css = self.css.compile(f.read())
					f.close()
					try:
						f = open(self.scss_path+css,"w")
						f.write(output_css)
						f.close()
					except Exception as e:
						print e
						logging.error("[SCSS] Fail to write the compile CSS")
				except:
					logging.error('[SCSS] Fail to compile {0}'.format(scss))