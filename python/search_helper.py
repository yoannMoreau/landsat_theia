# USGS Landsat Imagery Util
#
#
# Author: developmentseed
# Contributer: scisco, KAPPS-
#
# License: CC0 1.0 Universal

import json
import requests
import requests.exceptions

class Search(object):

    def __init__(self):
        self.api_url = 'http://spirit.cnes.fr/resto/Landsat/'

    def search(self,limit,start_date=None,end_date=None,clipper=None):
        """
        The main method of Search class. It searches tTheia Landsat API
        Returns python dictionary
        
        Arguments:
            start_date -- date string. format: YYYY-MM-DD
            end_date -- date string. format: YYYY-MM-DD
            limit -- integer specigying the maximum results return.
            clipper -- clipper object : clipper.bbox / clipper.town
        
        """

        search_string = self._query_builder(start_date,
                                            end_date,
                                            clipper
                                            )

        # Have to manually build the URI to bypass requests URI encoding
        # The api server doesn't accept encoded URIs
        #r = requests.get('%s?%s&&maxRecords=%s' % (self.api_url,
        #                                            search_string,
        #                                            limit))
        
        try:
            r = requests.get('%s?%s&&maxRecords=%s' % (self.api_url,
                                                    search_string,
                                                    limit)) 
            r.raise_for_status()
        except requests.HTTPError, e:
            exit ("site is not available")
            
        r_dict = json.loads(r.text)
        
        result={}
        
        if  (r_dict['features'] == 0):
            result['status'] = u'error'
            result['message'] = "error while loading datas"

        else:
            result['status'] = u'SUCCESS'
            result['total'] = len(r_dict['features'])
            result['limit'] = limit
            result['ID']=[i['id'] for i in r_dict['features']]
            result['downloads']=[{"download" : i['properties']['services']['download']['url'],
                                 "id" : i['id']}
                                  for i in r_dict['features']]
            result['results'] = {
                                "features": [{
                                  'properties':{'sceneID': i['id'],
                                  'sat_type': i['properties']['platform'],
                                  'thumbnail': i['properties']['thumbnail'],
                                  'date': i['properties']['completionDate'],
                                  'download': i['properties']['services']['download']['url']}
                                  ,
                                  'geometry': i['geometry'],
                                  "type": "Feature"}
                                 for i in r_dict['features']],
                                 "type": "FeatureCollection"
                                 }


        
        return result

    def _query_builder(self,
                       start_date=None,
                       end_date=None,
                       clipper=None
                        ):
        """ Builds the proper search syntax (query) for Landsat theia API """
        search_string='format=json&lang=fr&q='
        if (start_date is not None):
            if(end_date is not None):
                search_string+='entre+'+start_date+'+et+'+end_date
            else:
                search_string+=start_date
        elif(end_date is not None): 
            search_string+=end_date
        
        if(clipper.query is not None):
            query=clipper.query.replace(' ','+')
            search_string+='+'+query
        if(clipper.bbox is not None):
            search_string+='&box='+clipper.bbox

        return search_string