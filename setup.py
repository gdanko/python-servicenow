import os
from setuptools import setup, find_packages

def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	name = "servicenow",
	version = "0.1.4",
	author = "Gary Danko",
	author_email = "gdanko@protonmail.com",
	url = "https://github.com/gdanko/python-servicenow",
	license = "GPLv3",
	description = "A simple interface for ServiceNow",
	packages = ["servicenow"],
	package_dir = {"servicenow": "servicenow"},
	package_data = {
		"servicenow": ["data/servicenow.db"],
	},
	install_requires = ["idps", "requests"],

	# See https://pypi.python.org/pypi?%3Aaction=list_classifiers
	classifiers = [
		"Development Status :: 4 - Beta",
		"Environment :: Console",
		"Intended Audience :: System Administrators",
		"License :: Other/Proprietary License",
		"Operating System :: POSIX :: Other",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.3",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5"
	]
)
