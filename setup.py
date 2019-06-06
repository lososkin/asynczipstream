# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='zipstream-new',
    version='1.1.6',
    description='Zipfile generator that takes input files as well as streams',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='arjan5',
    author_email='arjan@anymore.nl',
    url='https://github.com/arjan-s/python-zipstream',
    packages=find_packages(exclude=['tests']),
    keywords='zip streaming',
    test_suite='nose.collector',
    tests_require=['nose'],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: System :: Archiving :: Compression",
    ],
)
