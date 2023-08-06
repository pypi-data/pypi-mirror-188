from setuptools import setup, find_packages
from io import open
from os import path

import pathlib
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup (
 name = 'tf2md',
 description = 'A simple commandline app for generating terraform docs',
 version = '1.0.2',
 packages = find_packages(), # list of all packages
 install_requires = ['mdutils', 'python-hcl2', 'click'],
 python_requires='>=3.5', # any python greater than 2.7
 entry_points='''
        [console_scripts]
        tf2md=tf2md.__main__:main
    ''',
 author="Karl Webster",
 keyword="markdown, terraform",
 long_description=README,
 long_description_content_type="text/markdown",
 license='GPL3',
 url='https://github.com/ktasper/tf2md',
)
