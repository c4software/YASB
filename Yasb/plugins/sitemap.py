import logging

class Plugin():
	""" Plugins de generation de sitemap dynamique en fonction des liens """

	links = []

	xml_header = """<?xml version="1.0" encoding="UTF-8"?>
<urlset 
	xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" 
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
	xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 
						http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n"""
	xml_footer = "</urlset>"

	def __init__(self, settings):
		logging.debug("[Sitemap] : init")
		# if settings.get("diff_build",False):
		# 	logging.error("[Sitemap] : You can't set diff_build and the Sitemap plugin")
		# 	raise
		pass

	def run(self, settings, content, fields):
		if "nositemap" in fields:
			# The link is not added if we have nositemap key in fields list
			return None

		if "path" in fields:
			self.links.append(fields['path']+fields['page'])
			logging.debug("[Sitemap] : Append {0}".format(fields['path']+fields['page']))
		else:
			self.links.append(fields['page'])
			logging.debug("[Sitemap] : Append {0}".format(fields['page']))

	def teardown(self, settings):
		logging.info("[Sitemap] : Teardown - Writing sitemap to disk")
		f = open(settings.get("output")+"sitemap.xml", 'w')
		f.write(self.xml_header)
		for link in self.links:
			f.write("<url><loc>{0}/{1}</loc></url>\n".format(settings.get("url"),link))
		f.write(self.xml_footer)
		f.close()
		pass
		