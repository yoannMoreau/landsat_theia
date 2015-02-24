#!/usr/bin/env python

# USGS Landsat Imagery Util
#
#
# Author: developmentseed
# Contributer: scisco
#
# License: CC0 1.0 Universal

import sys
import subprocess

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Check if gdal-config is installed
if subprocess.call(['which', 'gdal-config']):
    error = """Error: gdal-config is not installed on this machine.
This installation requires gdal-config to proceed.
If you are on Mac OSX, you can installed gdal-config by running:
    brew install gdal
On Ubuntu you should run:
    sudo apt-get install libgdal1-dev
Exiting the setup now!"""
    print error

    sys.exit(1)


def readme():
    with open("README.md") as f:
        return f.read()

setup(name="landsat_theia",
      version='0.0.1',
      description="A utility to search, download THEIA Landsat " +
      " satellite imagery",
      long_description=readme(),
      author="Yoann M",
      author_email="yoann.moreau@gmail.com",
      scripts=["bin/landsat"],
      url="https://github.com/yoannMoreau/landsat_theia",
      packages=["landsat_theia"],
      include_package_data=True,
      license="CCO",
      platforms="Posix; ",
      install_requires=[
          "GDAL==1.11.0",
          "gsutil==4.4",
          "python-dateutil==2.2",
          "numpy"
      ],
      )