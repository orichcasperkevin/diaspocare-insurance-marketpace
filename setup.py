# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in insur_marketplace/__init__.py
from insur_marketplace import __version__ as version

setup(
	name='insur_marketplace',
	version=version,
	description='diaspocare insurance marketplace',
	author='casper k orich',
	author_email='orichcasper59@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
