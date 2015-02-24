# USGS Landsat Imagery Util
#
#
# Author: developmentseed
# Contributer: scisco, KAPPS-
#
# License: CC0 1.0 Universal

##
## Main Setting File
##
# License: CC0 1.0 Universal
# Modification for theia by Yoann Moreau


import os

# Google Storage Landsat Config

DEBUG = os.getenv('DEBUG', False)
API_URL = 'http://spirit.cnes.fr/resto/Landsat/'

# Local Forlders Config

# User's Home Directory
HOME_DIR = os.path.expanduser('~')
# Utility's base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_DIR = HOME_DIR + '/landsat'
ZIP_DIR = DOWNLOAD_DIR + '/zip'

