from Yasb.parsers import rst
from Yasb import htmlbuilder
from Yasb.settings import Settings
from Yasb.utils import format_title_to_filename

import os, sys
import logging
from Yasb import colorer
import datetime

import argparse
import time

try:
	import cpickle as pickle
except:
	import pickle

def main():
	sys.path.append(os.getcwd())

	# Parse command line arguments
	parser = argparse.ArgumentParser(version="0.1",description='Yasb builder tool')
	parser.add_argument('--ignore', action="append", default=[], help="Ignore the execution of the specified plugin. Overide your params.py")
	parser.add_argument('--debug', action="store_true", default=False, help="Change the log level to debug")
	parser.add_argument('--silent', action="store_true", default=False, help="Disable output (except error)")
	arg = parser.parse_args()

	# Previous parsing data
	previoud_parsing = {}

	# Set the log level according to the user specification
	if arg.debug:
		logging.basicConfig(format="%(message)s", level=logging.DEBUG)
	else:
		logging.basicConfig(format="%(message)s", level=logging.INFO)

	if arg.silent:
		logging.getLogger().setLevel(logging.ERROR)

	try:
		import params
		params.settings["lastbuild"] = datetime.datetime.now() # Append lastbuild date to settings. So we can use it in template
		settings = Settings(params.settings)
	except:
		logging.error("Can't import settings in your params.py")
		exit()

	# Get the last build date
	previous_build_date = 0
	if settings.get("diff_build",False):
		try:
			previous_build_date = open(settings.get("lastbuild_file"), 'r').read()
			previoud_parsing = pickle.load(open(settings.get("diff_build_db"),"rb"))
		except:
			previous_build_date = 0

	# Init plugins defined in the user configuration
	# Try to import :
	# - In the plugin folder of the project (allow user to overide system plugin)
	# - If failed import in the system plugin folder
	plugins = []
	for plugin in settings.get("plugins",[]):
		if plugin not in arg.ignore:
			try:
				# Import and init user plugin
				plugins.append(getattr(__import__('{0}.{1}'.format(settings.get("plugin_folder"), plugin), fromlist=['Plugin']), 'Plugin')(settings))
			except:
				try:
					# If plugin is not an user plugin falback to system plugin
					plugins.append(getattr(__import__('Yasb.plugins.'+plugin, fromlist=['Plugin']), 'Plugin')(settings))
				except:
					logging.error("[Core] Disable : {0} plugin.".format(plugin))
		else:
			logging.warn("[Core] Ignoring plugin \"{0}\". (/!\ Disabled by command line)".format(plugin))

	# Iterate over page	
	processing_pages(settings.get("input"), "", settings, plugins, previous_build_date, previoud_parsing)

	# Execute the teardown method of each plugin
	for plugin in plugins:
		plugin.teardown(settings)

	# Diff mode enabled ?
	if settings.get("diff_build",False):
		# If enabled write the build date into the disk.
		f = open(settings.get("lastbuild_file"), 'w')
		f.write(str(time.time()))
		f.close()
		# Same for the process data
		pickle.dump(previoud_parsing, open(settings.get("diff_build_db"),"wb"), protocol=pickle.HIGHEST_PROTOCOL)

def processing_pages(path, folder, settings, plugins, previous_build_date, previoud_parsing):
	listing = [("{}{}".format(path, f),f) for f in os.listdir(path)]
	for path_in_file, infile in listing:
		if infile.startswith("."):
			continue

		if os.path.isdir(path_in_file):
			logging.warn("[Core] {} it's a directoy processing it.".format(infile))
			processing_pages(path_in_file+"/", infile, settings, plugins, previous_build_date, previoud_parsing)
			continue

		if settings.get("diff_build",False) and float(previous_build_date) > float(os.path.getmtime(path_in_file)):
			logging.warn("[Core] file ({0}) not modified since the lastbuild.".format(infile))
			try:
				content,fields = previoud_parsing[path_in_file]
				fields["loaded_from_db"]=True # Content and fields loaded from DB. We add a special field to indicate the source of file 
			except:
				logging.error("[Core] Ignoring {0} file not found in db.".format(infile))
				continue
		else:
			# New file OR update file
			# Load it from the disk
			# Parsing / rendering
			logging.info("[Core] Processing : "+path_in_file)
			content,fields = rst.run(open(path_in_file, 'r').read(), settings)
			
			# Append to the field the input_filename
			fields["input_filename"] = path_in_file

			# If we are in a subfolder append
			if "path" in fields:
				fields['path'] = "{}/{}".format(fields['path'], folder)
			else:
				fields['path']  = "{}/".format(folder)

			output_dir = settings.get("output")

			# If the article has the nosave field we skip the writing to disk action
			if "nosave" not in fields:
				# Execute the "run" action of each enable plugin
				for plugin in plugins:
					content = plugin.run(settings=settings, content=content, fields=fields) or content

				result_page = htmlbuilder.build_html(content,fields, settings)
				# Create output dir if needed
				if not os.path.exists(output_dir):
					os.makedirs(output_dir)

				# Create output path if needed
				if "path" in fields:
					output_dir = output_dir+fields['path']
					if not os.path.exists(output_dir):
						os.makedirs(output_dir)
				
				# Naming the output file
				if "page" not in fields:
					# If not any name is defined in the rst we generate a name
					if settings.get('title_as_name') and fields["title"] != "":
						# Use the title inside fields to name the output file.
						fields['page'] = format_title_to_filename(fields['title'])+".html"
					else:
						fileName, fileExtension = os.path.splitext(infile)
						fields['page'] = fileName+".html"

				logging.debug("[Core] Open for writing : "+output_dir+fields['page'])
				f = open(output_dir+fields['page'], 'w')
				f.write(result_page.encode('utf8'))
				f.close()

				if settings.get("diff_build",False):
					# If we are in diff build mode, we save the result of parsing (to speed up next build)
					previoud_parsing[path_in_file] = (content, fields)
