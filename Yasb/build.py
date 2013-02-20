from Yasb.parsers import rst
from Yasb import htmlbuilder
from Yasb.settings import Settings
from Yasb.utils import format_title_to_filename

import os, sys
import logging
from Yasb import colorer
import datetime

import argparse

def main():
	sys.path.append(os.getcwd())

	# Parse command line arguments
	parser = argparse.ArgumentParser(version="0.1",description='Yasb builder tool')
	parser.add_argument('--ignore', action="append", default=[], help="Ignore the execution of the specified plugin. Overide your params.py")
	parser.add_argument('--debug', action="store_true", default=False, help="Change the log level to debug")
	arg = parser.parse_args()

	# Set the log level according to the user specification
	if arg.debug:
		logging.basicConfig(format="%(message)s", level=logging.DEBUG)
	else:
		logging.basicConfig(format="%(message)s", level=logging.INFO)

	try:
		import params
		params.settings["lastbuild"] = datetime.datetime.now() # Append lastbuild date to settings. So we can use it in template
		settings = Settings(params.settings)
	except:
		logging.error("Can't import settings in your params.py")
		exit()

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
					logging.error("[Core] Plugin : {0} is unknown.".format(plugin))
		else:
			logging.warn("[Core] Ignoring plugin \"{0}\". (/!\ Disabled by command line)".format(plugin))

	# Iterate over page
	listing = os.listdir(settings.get("input"))
	for infile in listing:

		if infile.startswith("."):
			continue

		logging.info("[Core] Processing : "+infile)
		content,fields = rst.run(open(settings.get("input")+infile, 'r').read())
		
		output_dir = settings.get("output")

		# If the article has the nosave field we skip the writing to disk action
		if "nosave" not in fields:
			
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

		# Execute the "run" action of each enable plugin
		for plugin in plugins:
			plugin.run(settings=settings, content=content, fields=fields)


	# Execute the teardown method of each plugin
	for plugin in plugins:
		plugin.teardown(settings)


