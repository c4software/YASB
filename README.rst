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


Docker Image
------------

You can also use the prebuilt Yasb image :

.. code:: bash
  # docker run -it -v $(pwd):/sources/ c4software/yasb:latest yasb  


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

For a complete... complete example see the settings of my current blog :

.. code:: python

	settings = {"site_title":"Un peu de tout, un peu de rien...", 
			"author":"Valentin Brosseau",
			"url":"http://blog.lesite.us",
			"input":"./source/",
			"output":"./output/",

			"title_as_name":True,

			"plugins":['sitemap','blog','pyscss',"theme","static"],
			
			"static_settings":"",
			"theme":"./theme/valentin/",
			"blog_settings":{"index_page":"index","nbchar_resume":100,"nb_per_page":7},
			"scss_settings":{"files":[('main.scss','main.css'),('pygments.scss','pygments.css')],"path":"./theme/valentin/static/styles/"},

			"diff_build":True,
			"lastbuild_file":"./output/.lastbuild",
			"diff_build_db":"./output/.diff_build_db",

			"links":(
					    ('Accueil', '/'),
					    ('Archives', '/archives.html'),
					    ('Moi', 'http://valentinbrosseau.lesite.us/'),
					    ('Twitter', 'http://twitter.com/c4software'),
					    ('Google+', 'https://plus.google.com/104883394321573041618/about'),
					    ('Flux RSS', 'feeds/all.atom.xml')
			        )
			}

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

Simplify the process
--------------------
To simplify the build/update/etc.. process you can write a simple makefile like this one : 

.. code:: makefile

	BASEDIR=$(PWD)
	OUTPUTDIR=$(BASEDIR)/output

	SSH_HOST=YOUR HOST
	SSH_PORT=22
	SSH_USER=YOURUSER
	SSH_TARGET_DIR=YOURSERVERPATH

	minimal: 
		yasb --ignore static --ignore theme --ignore pyscss --silent

	minimal-verbose: 
		yasb --ignore static --ignore theme --ignore pyscss

	autobuild:
		yasb-monitor --ignore static --ignore theme --ignore pyscss --silent

	help:
		@echo '                                '
		@echo 'Usage:                          '
		@echo '   make minimal                 '
		@echo '   make minimal-verbose         '
		@echo '   make autobuild               '
		@echo '   make full	                   '
		@echo '   make clean                   '
		@echo '   make rsync	               '
		@echo '                                '

	full:
		yasb

	clean:
		rm -rf $(OUTPUTDIR)
		mkdir $(OUTPUTDIR)

	rsync:
		rsync -avzh --exclude '.diff_build_db' --exclude '.lastbuild' --delete -e "ssh -p $(SSH_PORT)" $(OUTPUTDIR)/ $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR)

	.PHONY: help clean minimal minimal-verbose autobuild full rsync


With this makefile you can run command like :

* make **clean** : Empty your output path.
* make **minimal** : Build your project without copying theme, building pyscss and copying static.
* make **minimal-verbose** : Same as minimal but with some output.
* make **full** : Build your project with default settings (Usefull for the first init).
* make **rsync** : Sync the output result with your personnal webserver.
* make **autobuild** : Autobuild the website when a change is detected in the source folder

For example to init your project you can do :

	make clean full

**Note**: By default running make without any other argument will do the **minimal** rule

Plugins usage Documentation
---------------------------
SOON

.. _YASB-SAMPLE: https://github.com/c4software/YASB-SAMPLE
.. _Python: http://www.python.org/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Jinja2: http://jinja.pocoo.org/
.. _pyScss: https://github.com/Kronuz/pyScss
.. _Example: https://raw.github.com/c4software/YASB-SAMPLE/master/source/site_settings_demo.rst
