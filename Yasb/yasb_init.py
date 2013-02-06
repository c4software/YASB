#!/usr/bin/env python
import readline
import os, sys

sys.path.append(os.getcwd())

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

	# Base settings
	print "\nBase settings :"
	print "---------------\n"
	project_name = ""
	while project_name is "":
		project_name = wait_for_input("Name of project : ")

	author 			= wait_for_input("Author : ")
	url 			= wait_for_input("Url (http://) : ","http://")
	input_folder 	= wait_for_input("Input folder (Where you rst files will be) : (./source/)","./source/")
	output_folder 	= wait_for_input("Output folder (Where the result will be put) : (./output/)","./output/")
	theme_folder 	= wait_for_input("Emplacement of the theme : (./theme/classic/)","./theme/classic/")


	# Plugins settings
	print "\nPlugin settings :"
	print "-----------------\n"
	available_plugins = ["blog","pyscss","sitemap","static","theme"]
	selected_plugins = []
	for plugin in available_plugins:
		choice = None
		while choice is not "y" and choice is not "n" and choice is not "":
			choice = wait_for_input("Enable plugin : {0} ? (Y/n)".format(plugin),"y")

		if choice == "y":
			selected_plugins.append(plugin)


	# static settings
	if "static" in selected_plugins:
		static_settings = wait_for_input("Emplacement of static file (./static/): ","./static/")


	# TODO suite parametrage plugin

	# TODO Creation du fichier params.py sur disque.

	# Creation des dossiers input_folder / output_folder / plugins (si non existant)
	if not os.path.exists(input_folder):
		os.makedirs(input_folder)

	if not os.path.exists(output_folder):
		os.makedirs(output_folder)

	if not os.path.exists(theme_folder):
		os.makedirs(theme_folder)
		os.makedirs(theme_folder+"/static/")
		os.makedirs(theme_folder+"/templates/")
		# TODO Creation/deplacement de l'arborescence pour le THEME

	if not os.path.exists("./plugins/"):
		os.makedirs("./plugins/")
	try:
		f = open("./plugins/__init__.py","w")
		f.close()
	except:
		pass

if __name__ == "__main__":
	try:
		main()
	except:
		pass