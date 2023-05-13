# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='asynczipstream',
    version='1.0.1',
    description='Asynchronous Zipfile generator that takes input files as well as streams',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='lososkin',
    author_email='yalososka@gmail.com',
    url='https://github.com/lososkin/python-zipstream-aio',
    packages=find_packages(exclude=['tests']),
    keywords='async zip streaming',
    install_requires="aiofiles>22.1.0",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: System :: Archiving :: Compression",
    ],
)
