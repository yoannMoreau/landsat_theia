# USGS Landsat Imagery Util
#
# BAsed on 
# Author: developmentseed
# Contributer: scisco, KAPPS-
#
# License: CC0 1.0 Universal
# Modification for theia by Yoann Moreau
import subprocess
from zipfile import ZipFile
import tarfile
import urllib2,base64

from dateutil.parser import parse

from general_helper import check_create_folder, exit


class GsHelper(object):

    def __init__(self,download_dir):
        # Make sure download directory exist
        self.zip_dir=download_dir
        check_create_folder(download_dir)

    def single_download(self,username,password,download ,name,ZIP_DIR):

        """ Download single image from Landsat on Google Storage
        Arguments:
            row - string in this format xxx, e.g. 003
            path - string in this format xxx, e.g. 003
            name - zip file name without .tar.bz e.g. LT81360082013127LGN01
            sat_type - e.g. L7, L8, ...
        """
        try:
            request = urllib2.Request(download)
            base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
            request.add_header("Authorization", "Basic %s" % base64string)   
            result = urllib2.urlopen(request)
            data = result.read()        
            result.close()
            try:
                f=open(ZIP_DIR+'/'+name+'.tgz', 'wb')
                f.write(data)
                f.close()
                return True
            except urllib2.HTTPError:  
                return False
        except urllib2.HTTPError:  
            return False

    def checkifDownloadExist(self,username,password,download , name):
        """ Download single image from Landsat on Google Storage
        Arguments:
            row - string in this format xxx, e.g. 003
            path - string in this format xxx, e.g. 003
            name - zip file name without .tar.bz e.g. LT81360082013127LGN01
            sat_type - e.g. L7, L8, ...
        """
        try:
            request = urllib2.Request(download)
            base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
            request.add_header("Authorization", "Basic %s" % base64string)   
            result = urllib2.urlopen(request)
            try:
                f=open(self.zip_dir+'/'+name+'.tgz', 'wb')
                f.close()
                return True
            except urllib2.HTTPError:  
                return False
        except urllib2.HTTPError:  
            return False
