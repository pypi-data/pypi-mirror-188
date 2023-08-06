#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pollai',
    version='0.1.0',
    author='ByteVolx',
    author_email='onions193@gmail.com',
    description='AI models simplified and implemented',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/PollAI/pollai',
    packages=find_packages(),
    install_requires=[
        "scikit-learn",
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)