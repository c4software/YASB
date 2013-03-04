import logging

from Yasb.htmlbuilder import render
from Yasb.utils import truncate_html_words
import datetime

import os

class Plugin():
	""" Module generation de blog 
		/!\ a template (named blog_page.html) is needed into the theme folder.
		in the template the variable "articles" contain the articles list for 
		the current page.

		/!\ To use the RSS generator a template name blog_rss.xml is needed.

		/!\	You can overide settings by defining "blog_settings" in params of the project	
	"""

	template_string 		= ""
	rss_template_string 	= ""
	archive_template_string = ""
	current_page 			= 0
	part_article 			= []

	params = {	"index_page":"index",
				"other_page":"page-",
				"nb_per_page":10,
				"date_format":"%Y-%m-%d %H:%M:%S",
				"nbchar_resume":100,
				"template":"blog_page.html",
				"rst_type":"blog", # The RST file must conain the field blog to be processed
				"rss_template":"blog_rss.xml",
				"rss_path":"feeds/",
				"rss_file":"all.atom.xml",
				"rss":True,
				"archive":True,
				"archive_template":"archives.html",
				"archive_file":"archives.html"}

	def __init__(self, settings):
		logging.debug('[Blog] Init')
		if settings.get("blog_settings", None):
			 self.params = dict(self.params.items() + settings.get("blog_settings").items())

		if settings.get("diff_build",False):
			logging.error("[Blog] You can't set diff_build and the Blog plugin")
			raise

		# Read the template to render article list (Template for page)
		try:
			f = open(settings.get("theme")+"templates/"+self.params["template"],"r")
			self.template_string = f.read()
			f.close()
		except:
			logging.error("[Blog] Template not found for rendering. You need to add the {1} into {0}".format(settings.get("theme"), self.params["template"]))

		# Read the template to generate the RSS
		if self.params["rss"]:
			try:
				f = open(settings.get("theme")+"templates/"+self.params["rss_template"],"r")
				self.rss_template_string = f.read()
				f.close()
			except:
				logging.error("[Blog] RSS Template not found for rendering. You need to add the {1} into {0}".format(settings.get("theme"), self.params["rss_template"]))

		# Read the template to generate the archive
		if self.params["archive"]:
			try:
				f = open(settings.get("theme")+"templates/"+self.params["archive_template"],"r")
				self.archive_template_string = f.read()
				f.close()
			except:
				logging.error("[Blog] Archive Template not found for rendering. You need to add the {1} into {0}".format(settings.get("theme"), self.params["archive_template"]))


	def run(self, settings, content, fields):
		#logging.debug(fields)
		if self.params['rst_type'] in fields:
			if "date" in fields:
				try:
					if "status" in fields and fields["status"] == "draft":
						# Ignoring article with status : DRAFT
						return None
					fields_blog = fields.copy()
					#fields['datetime'] = datetime.datetime.strptime(fields['date'], self.params["date_format"])
					fields_blog['date'] 	= datetime.datetime.strptime(fields_blog['date'], self.params["date_format"]) #.date()
					fields_blog['summary']	= truncate_html_words(content, self.params["nbchar_resume"])
					#self.part_article.append([fields,content[:self.params["nbchar_resume"]] + (content[self.params["nbchar_resume"]:] and '...')])
					self.part_article.append([fields_blog,content])
				except:
					logging.error("[Blog] Bad date format")
			else:
				logging.error("[Blog] No date for the article {0} -- Ignoring".format(fields['page']))
		else:
			logging.debug("[Blog] Element : {0} not containing the field {1}".format(fields['page'], self.params['rst_type']))

	def teardown(self, settings):
		# On trie les articles par date
		self.part_article.sort(key=lambda r: r[0]['date'], reverse=True)
		self.write_page(settings)
		if self.params['rss']:
			self.write_rss(settings)
		if self.params['archive']:
			self.write_archive(settings)

	def write_rss(self, settings):
		logging.info("[Blog] Generating RSS")
		path = settings.get("output")+self.params["rss_path"]
		if not os.path.exists(path):
			os.makedirs(path)

		feed = render(self.rss_template_string, {"articles":self.part_article,"updated":datetime.datetime.now(),"settings":self.params}, settings)
		f = open(path+self.params["rss_file"],"w")
		f.write(feed.encode('utf8'))
		f.close()

	def write_archive(self, settings):
		logging.info("[Blog] Generating Archive")
		
		archive = render(self.archive_template_string, {"articles":self.part_article,"settings":self.params}, settings)
		f = open(settings.get("output")+self.params["archive_file"],"w")
		f.write(archive.encode('utf8'))
		f.close()

	def write_page(self, settings):
		logging.info("[Blog] Writing pages")

		nb_page = (len(self.part_article)/self.params['nb_per_page']) + 1

		current_page = 1
		pagination = range(0, len(self.part_article), self.params["nb_per_page"])
		for i in pagination:

			# Gestion de la pagination
			paginator = {}
			if current_page < len(pagination):
				paginator["has_next"] = True
				paginator["next_page"] = self.params["other_page"]+str(current_page+1) # Uri de la page suivante
			else:
				paginator["has_next"] = False

			if i == 0:
				paginator["has_previous"] = False
			else:
				paginator["has_previous"] = True
				if current_page-1 == 1:
					# Premiere page alors on prend la page d'index
					paginator["previous_page"] = self.params["index_page"]
				else:
					# Sinon on genere la page correspondante
					paginator["previous_page"] = self.params["other_page"]+str(current_page-1)


			# Render the template output
			output_content = render(self.template_string, {"articles":self.part_article[i:i+self.params["nb_per_page"]], "nb_page":nb_page,"current_page":current_page,"paginator":paginator}, settings) 

			if i == 0:
				logging.debug("[Blog] Output to {0}.html".format(self.params["index_page"]))
				output_file = settings.get("output")+self.params["index_page"]+".html"
			else:
				logging.debug("[Blog] Output to {0}{1}.html".format(self.params["other_page"], current_page))
				output_file = settings.get("output")+"{0}{1}.html".format(self.params["other_page"], current_page)

			# Writing file
			f = open(output_file,"w")
			f.write(output_content.encode('utf8'))
			f.close()
			current_page = current_page + 1

		#self.part_article = []
