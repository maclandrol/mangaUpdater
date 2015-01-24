#!/usr/bin/python

import setuptools
import os, sys

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "python")))


setuptools.setup(
	name="mangaU",
	version='1.0',
	description="Manga manager and downloader using MangaEden api (https://www.mangaeden.com)",
	keywords=["manga", "download", "scan", "mangaeden", "manager"],
	author="Emmanuel Noutahi",
	author_email="emmanuel.noutahi@gmail.com",
	url="https://github.com/maclandrol/mangaUpdater",
	download_url="https://github.com/maclandrol/mangaUpdater/tarball/master",
	scripts=['mangaU'],
	packages=setuptools.find_packages(),

	classifiers=[
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Operating System :: POSIX :: Linux",
		"Environment :: Console",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2.7",
		"Development Status :: 5 - Production/Stable",
		"Topic :: Utilities",
		'Natural Language :: English',
		'Intended Audience :: General',
		'License :: GNU General Public License (GPL)',
		'Operating System :: POSIX',
		],
	install_requires=[
		'requests',
		'colorama',
		'pysqlite'
	],
	long_description="""\

Description
-----------

This is a console based application to download and manage mangas inside a local database.
The main features offered are search and download, and keeping a database to manage what you're are reading

To install:

::

	sudo python setup.py install

To run:

::

	mangaU


"""
)
