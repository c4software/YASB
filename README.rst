YASB
====

YASB (Yet Another Static Builder) is a Website generator written in Python_. With it you can :

* Build a static website.
* Generate a personal blog.
* Host the result of the build anywhere you want.
* Write simple plugin to extend YASB according to your need.

Features
--------
* Write your article using reStructuredText_.
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

Demo project
------------
`YASB-SAMPLE`_

Usage
-----
SOON

Core Documentation
------------------
SOON

Plugins Documentation
---------------------
SOON

.. _YASB-SAMPLE: https://github.com/c4software/YASB-SAMPLE
.. _Python: http://www.python.org/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Jinja2: http://jinja.pocoo.org/
.. _pyScss: https://github.com/Kronuz/pyScss