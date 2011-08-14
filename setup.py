#!/usr/bin/env python

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "nymp",
    version = "0.0.1",
    author = "Thammi",
    author_email = "thammi@chaossource.net",
    description = ("A graphical xmms2 cli frontend. It is library focused and provides a tree view on your collection"),
    license = "GPLv3",
    keywords = "xmms2 audio cli",
    url = "http://www.chaossource.net/nymp/",
    packages=['nymp', 'nymp.xmms', 'nymp.gui'],
    package_dir={'': 'src'},
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Multimedia :: Sound/Audio",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Environment :: Console",
    ],
    entry_points={
        'console_scripts': [
            'nymp = nymp.start:main',
            ],
        },
)

