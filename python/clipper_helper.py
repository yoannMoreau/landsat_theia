# USGS Landsat Imagery Util
#
#
# Author: developmentseed
# Contributer: scisco, KAPPS-
#
# License: CC0 1.0 Universal

import os
import re
import errno
import shutil
from tempfile import mkdtemp

try:
    from osgeo import ogr
    from osgeo import osr
except:
    import ogr
    import osr


class Clipper(object):

    def __init__(self):
        """ """

    def shapefile(self, file):
        """
        reprojette en WGS84 et recupere l'extend
        """ 
        
        driver = ogr.GetDriverByName('ESRI Shapefile')
        dataset = driver.Open(file)
        if dataset is not None:
            # from Layer
            layer = dataset.GetLayer()
            spatialRef = layer.GetSpatialRef()
            # from Geometry
            feature = layer.GetNextFeature()
            geom = feature.GetGeometryRef()
            spatialRef = geom.GetSpatialReference()
            
            #WGS84
            outSpatialRef = osr.SpatialReference()
            outSpatialRef.ImportFromEPSG(4326)
    
            coordTrans = osr.CoordinateTransformation(spatialRef, outSpatialRef)
    
            env = geom.GetEnvelope()
            xmin = env[0]
            ymin = env[2]
            xmax = env[1]
            ymax = env[3]
    
            pointMAX = ogr.Geometry(ogr.wkbPoint)
            pointMAX.AddPoint(env[1], env[3])
            pointMAX.Transform(coordTrans)
            
            pointMIN = ogr.Geometry(ogr.wkbPoint)
            pointMIN.AddPoint(env[0], env[2])
            pointMIN.Transform(coordTrans)
    
    
            self.bbox = str(pointMIN.GetPoint()[0])+','+str(pointMIN.GetPoint()[1])+','+str(pointMAX.GetPoint()[0])+','+str(pointMAX.GetPoint()[1])
            self.query = None
        else:
            exit(" shapefile not found. Please verify your path to the shapefile")

    
    def query(self,query):
        "return la requete en format text"
        self.query = query
        self.bbox = None
        