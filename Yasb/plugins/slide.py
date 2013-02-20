import logging
from Yasb.htmlbuilder import render

"""
	Plugin de creation de presentation HTML base sur le travail de Google.
"""

class Plugin():

	slides = []
	slides_template	= ""

	def __init__(self, settings):
		logging.debug("[Slide] Init")
		try:
			f = open(settings.get("theme")+"templates/slides.html","r")
			self.slides_template = f.read()
			f.close()
		except:
			logging.error("[Blog] RSS Template not found for rendering. You need to add the {1} into {0}".format(settings.get("theme"), self.params["rss_template"]))

		pass

	def run(self, settings, content, fields):
		logging.debug("[Slide] Ajout de la slide")
		self.slides.append([fields,content])

	def teardown(self, settings):
		logging.debug("[Slide] Teardown")
		output_content = render(self.slides_template, {"slides":self.slides}, settings)
		try:
			f = open(settings.get("output")+"index.html","w")
			f.write(output_content.encode('utf8'))
			f.close()
		except:
			logging.debug("[Slide] Error when writing index.html on disk.")
