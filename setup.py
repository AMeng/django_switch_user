from setuptools import setup, find_packages
import os

version = '0.1'

LONG_DESCRIPTION = """
==================
django_switch_user
==================

Simple app that places a small form for super users to select
a different user, and automatically log in as that user, for
testing purposes.

"""

setup(
name='django_switch_user',
version=version,
description="Allows admins to login as different users for testing purposes",
long_description=LONG_DESCRIPTION,
classifiers=[
"Programming Language :: Python",
"Topic :: Software Development :: Libraries :: Python Modules",
"Framework :: Django",
"Environment :: Web Environment",
"Operating System :: OS Independent",
"Intended Audience :: Customer Service",
"Natural Language :: English",
],
keywords=['django', 'users', 'alias', 'spoof', 'login', 'switch', 'logout', 'session',],
author='Alexander Meng',
author_email='alexbmeng@gmail.com',
url='http://github.com/AMeng/django_switch_user',
packages=find_packages(),
include_package_data=True,
zip_safe=False,
install_requires=['setuptools'],
)
