YASB
====

YASB (Yet Another Static Builder) is a Website generator written in Python_. With it you can :

* Build a static website.
* Generate a personal blog.
* Host the result of the build anywhere you want.
* Write simple plugin to extend YASB according to your need.

Features
--------
* Write your article using reStructuredText_. (You can also add Jinja2 synthax if you want -Example_-)
* Make theme for your project using Jinja2_ (with Code Syntax Highlighting).
* A plugin mechanism to extend YASB.
* CLI tool to invoke the build of your project.
* A set of builtin plugin :
	* Blog (Pagination, Archive, RSS)
	* Pyscss (SASS Integration to build your CSS when you make html) (Using pyScss_)
	* sitemap (Generate a sitemap.xml at the end of the build process)


Instalation
-----------
	pip install -U  https://github.com/c4software/YASB/archive/master.zip


Fast usage
----------

.. code:: bash

	# mkdir myproject && cd myproject
	# yasb-init
	# # Create your first article in the source/ folder
	# yasb

Project Structure
-----------------
The only **NEEDED** file in your project is the **params.py**. This file contain at least :

.. code:: python

	settings = {"site_title":"Demo blog", # Title of the website
			"author":"Valentin Brosseau", # Author of the website
			"url":"http://demo.url", # Url of the website
			"input":"./source/", # RST source file, Location of RST file
			"output":"./output/", # Output folder for the build
			"plugins":[], # Enable plugin for this demo project
			"title_as_name": False, # Use the title in the RST as the filename for the output
			"theme":"./theme/demo/", # Folder of the theme
			"build_diff":False, # Enable the differencial build, if True the Yasb script will build only New or Modified file since the last build. 
			# ... 
		}

For a full/working example you can take a look at the Sample Project (`YASB-SAMPLE`_).

**Note:** *All Flags/Settings you put in this stucture will be available in your templates.*

Demo project
------------
`YASB-SAMPLE`_

Usage Documentation
------------------
To build your project you need to run the "yasb" command directly from the project folder.

	# yasb --help
	usage: yasb [-h] [-v] [--ignore PLUGIN] [--debug] [--silent]

	Yasb builder tool

	optional arguments:
	  -h, --help       show this help message and exit
	  -v, --version    show program's version number and exit
	  --ignore PLUGIN  Ignore the execution of the specified plugin (Overide your params.py)
	  --debug          Change the log level to debug
	  --silent         Disable output (except error)

* Classic usage :
	# yasb
* Advanced usage (Run the build, without the plugin static and theme) :
	# yasb --ignore theme --ignore static
	

More documentation : Soon


Plugins usage Documentation
---------------------------
SOON

.. _YASB-SAMPLE: https://github.com/c4software/YASB-SAMPLE
.. _Python: http://www.python.org/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Jinja2: http://jinja.pocoo.org/
.. _pyScss: https://github.com/Kronuz/pyScss
.. _Example: https://raw.github.com/c4software/YASB-SAMPLE/master/source/site_settings_demo.rst