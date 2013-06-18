#!/usr/bin/env python
import readline
import os, sys

sys.path.append(os.getcwd())

import json
import shutil

def wait_for_input(prompt, default=""):
	val = raw_input(prompt)
	if val == "":
		return default
	else:
		return val

def main():
	print ""
	print ""
	print "8b        d8   db        ad88888ba  88888888ba"   
	print " Y8,    ,8P   d88b      d8'     '8b 88      '8b " 
	print "  Y8,  ,8P   d8'`8b     Y8,         88      ,8P  "
	print "   '8aa8'   d8'  `8b    `Y8aaaaa,   88aaaaaa8P'  "
	print "    `88'   d8YaaaaY8b     `''''''8b,88''''''8b,  "
	print "     88   d8''''''''8b          `8b 88      `8b  "
	print "     88  d8'        `8b Y8a     a8P 88      a8P  "
	print "     88 d8'          `8b 'Y88888P'  88888888P'   "
	print ""
	print ""

	# Template pour les settings
	settings_template = {	"site_title":"", 
							"author":"",
							"url":"",
							"input":"",
							"output":"",
							"plugins":[],
							"theme":"",
							"diff_build":False,
							"title_as_name":False}

	# Base settings
	print "\nBase settings :"
	print "---------------\n"
	while settings_template["site_title"] is "":
		settings_template["site_title"] = wait_for_input("Site title : ")

	settings_template["author"] 	= wait_for_input("Author : ")
	settings_template["url"] 		= wait_for_input("Url (http://) : ","http://")
	settings_template["input"] 		= wait_for_input("Input folder (Where you rst files will be) : (./source/) ","./source/")
	settings_template["output"] 	= wait_for_input("Output folder (Where the result will be put) : (./output/) ","./output/")
	#settings_template["theme"] 		= wait_for_input("Emplacement of the theme : (./theme/classic/)","./theme/classic/")

	settings_template["diff_build"] = wait_for_input("Build only new RST file (Speed up the process, but create a file to memorize old article) ? (N/y) ","n")
	if settings_template["diff_build"].lower() == "y":
		settings_template["diff_build"] = True
	else:
		settings_template["diff_build"] = False

	settings_template["title_as_name"] 	= wait_for_input("Use title from fields for the output html filename (If title is defined in fields only)? (Y/n) ","Y")
	if settings_template["title_as_name"].lower() == "y":
		settings_template["title_as_name"] = True
	else:
		settings_template["title_as_name"] = False

	# Plugins settings
	print "\nPlugin settings :"
	print "-----------------\n"
	available_plugins = [("blog","A simple blog plugin. Provide Pagination, rss, archive, draft"),("pyscss","SCSS compiler. REQUIRE PyScss"),("sitemap","Sitemap generator"),("static","Move defined static folder content to the output"),("theme","Move the user theme to the output folder.")]
	selected_plugins = []
	for plugin,description in available_plugins:
		choice = None
		while choice is not "y" and choice is not "n" and choice is not "":
			choice = wait_for_input("Enable plugin : {0} - {1} ? (Y/n)".format(plugin,description),"y")

		if choice == "y":
			selected_plugins.append(plugin)

	# static settings
	if "static" in selected_plugins:
		static_settings = wait_for_input("Emplacement of static file (./static/): ","./static/")
		if not os.path.exists(static_settings):
			os.makedirs(static_settings)

	if "blog" in selected_plugins:
		settings_template['blog_settings'] = {}	

	if "pyscss" in selected_plugins:
		settings_template['scss_settings'] = {"files":[('main.scss','main.css')],"path":"./theme/classic/static/styles/"}

	settings_template["plugins"] = selected_plugins

	# Demande du theme
	print "\Choose your theme :"
	print "-----------------\n"
	choosen_theme = 0
	theme = ["classic","slide"]
	while choosen_theme not in ["1","2"]:
		choosen_theme 	= wait_for_input("Theme : \n 1 - Classic (default) \nYour choice : ","1")
	settings_template["theme"] = "./theme/"+theme[int(choosen_theme)-1]+"/"

	# Init de quelques lien pour de la demo
	settings_template["links"] = (('Home', '/'),('Yasb', 'https://github.com/c4software/YASB'))

	# Creation du fichier params.py sur disque
	output_settings = "settings = {0}".format(json.dumps(settings_template, separators=(',', ': '), indent=4, sort_keys=True))
	# Ecriture du fichier params.py sur disque
	f = open("params.py","w")
	f.write(output_settings.replace("false","False").replace("true","True"))
	f.close()

	# Creation des dossiers input_folder / output_folder / plugins (si non existant)
	if not os.path.exists(settings_template["input"]):
		os.makedirs(settings_template["input"])

	if not os.path.exists(settings_template["output"]):
		os.makedirs(settings_template["output"])

	if not os.path.exists(settings_template["theme"]):
		shutil.copytree(os.path.dirname(__file__)+"/yasb_init_ressources/theme/"+theme[int(choosen_theme)-1]+"/", "./theme/"+theme[int(choosen_theme)-1])

	if not os.path.exists("./plugins/"):
		os.makedirs("./plugins/")
	try:
		f = open("./plugins/__init__.py","w")
		f.close()
	except:
		pass

def main_script():
	try:
		main()
	except:
		pass

if __name__ == "__main__":
	try:
		main()
	except:
		pass