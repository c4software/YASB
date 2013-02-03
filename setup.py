#!/usr/bin/env python
from setuptools import setup

requires = [] #['jinja2','docutils','pygments']

try:
    import argparse  # NOQA
except ImportError:
    requires.append('argparse')

entry_points = {'console_scripts': [
                                    'yasb = Yasb.build:main'
                                   ]
                }


README = ""
CHANGELOG = ""


setup(
    name="Yasb",
    version="0.1",
    url='http://blog.lesite.us',
    author='Valentin Brosseau',
    author_email='c4software@gmail.com',
    description="Yasb - Yet Another Static Builder",
    long_description="",
    packages=['Yasb', 'Yasb.plugins', 'Yasb.parsers'],
    include_package_data=True,
    install_requires=requires,
    entry_points=entry_points,
    classifiers=[],
    test_suite='',
)