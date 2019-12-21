# Copyright (c) 2019 R. Tohid
#
# Distributed under the Boost Software License, Version 1.0. (See a copy at
# http://www.boost.org/LICENSE_1_0.txt)import setuptools
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="phycfg-rtohid",  # Replace with your own username
    version="0.0.1",
    author="R. Tohid",
    author_email="stellar dot python at gmail dot com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rtohid/phycfg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: BOOST SOFTWARE LICENSE",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
