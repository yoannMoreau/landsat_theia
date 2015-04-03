#!/usr/bin/env python

# USGS Landsat Imagery Util
#
# Based on :
# Author: developmentseed
# Contributer: scisco, KAPPS-
#
# License: CC0 1.0 Universal
# Modification for theia by Yoann Moreau

from __future__ import print_function
import sys
import subprocess
import argparse
import textwrap
import json
import os

from dateutil.parser import parse

from gs_helper import GsHelper
from clipper_helper import Clipper
from search_helper import Search
from general_helper import reformat_date


DESCRIPTION = """Landsat-util is a command line utility that makes it easy to
search, download, and process Landsat imagery.
    Commands:
        Search:
        landsat.py search [-h] [-l LIMIT] [-s START] [-e END]
                     [--onlysearch]
                     {shapefile,query}
        SEARCH:
            {shapefile,query}
                                Search commands
            shapefile           Activate Shapefile
            town             Activate country
            
            optional arguments:
            -h, --help            show this help message and exit
            -l LIMIT, --limit LIMIT
                                Search return results limit default is 100
            -s START, --start START
                                Start Date - Most formats are accepted e.g.
                                Jun 12 2014 OR 06/12/2014
            -e END, --end END   End Date - Most formats are accepted e.g.
                                Jun 12 2014 OR 06/12/2014
            -d, --download      Use this flag to download found images
            -u, --user          Use this flag to give your login name
            -p, --password      Use this flag to give your password name
            -o --outputPath     Output path to write downloaded file 
                                DEFAULT HOME_directory/landsat
        Download:
        landsat_theia download [-h] sceneName 
        positional arguments:
            sceneID     Provide Full sceneName, e.g. LANDSAT8_OLITIRS_XS_20150130_N2A_France-MetropoleD0004H0003
"""


def args_options():
    parser = argparse.ArgumentParser(prog='landsat_theia.py',
                        formatter_class=argparse.RawDescriptionHelpFormatter,
                        description=textwrap.dedent(DESCRIPTION))

    subparsers = parser.add_subparsers(help='Landsat Utility',
                                       dest='subs')

    #---------------- Search
    parser_search = subparsers.add_parser('search',
                                          help='Search Landsat metdata')

    # Global search options
    parser_search.add_argument('-l', '--limit', default=100, type=int,
                               help='Search return results limit\n'
                               'default is 100')
    parser_search.add_argument('-s', '--start',
                               help='Start Date - Most formats are accepted '
                               'e.g. Jun 12 2014 OR 06/12/2014')
    parser_search.add_argument('-e', '--end',
                               help='End Date - Most formats are accepted '
                               'e.g. Jun 12 2014 OR 06/12/2014')
    
    parser_search.add_argument('-d', '--download', action='store_true',
                               help='Use this flag to download found images')
    parser_search.add_argument('-u', '--user',
                               help='loggin for downloading (on theia site)')
    parser_search.add_argument('-p', '--password',
                               help='password for downloading (on theia site)')
    parser_search.add_argument('-o', '--outputRepository', 
                               help='password for downloading (on theia site) DEFAULT HOME_directory/landsat')
    

    search_subparsers = parser_search.add_subparsers(help='Search commands',
                                                     dest='search_subs')


    search_shapefile = search_subparsers.add_parser('shapefile',
                                                    help="Activate Shapefile")
    search_shapefile.add_argument('path',
                                  help="Path to shapefile")
    
    search_query = search_subparsers.add_parser('query',
                                                  help="Activate query")
    
    search_query.add_argument('name', help="Town name e.g. Toulouse")


    #---------------- Download


    parser_download = subparsers.add_parser('download',
                                            help='Download images from Google Storage')
    parser_download.add_argument('scenes',
                                 metavar='scenes',
                                 nargs="+",
                                 help="Provide Full sceneID, e.g. "
                                 "LANDSAT8_OLITIRS_XS_20150114_N2A_France-MetropoleD0005H0002")
    parser_download.add_argument('-u', '--user',
                               help='loggin for downloading (on theia site)')
    parser_download.add_argument('-p', '--password',
                               help='password for downloading (on theia site)')
    parser_download.add_argument('-o', '--outputRepository',
                               help='password for downloading (on theia site)')
    
    return parser


def main(args):
    """
    Main function - launches the program
    """

    if args:
        
        if not args.outputRepository:
            HOME_DIR = os.path.expanduser('~')
            # Utility's base directory
            BASE_DIR = os.path.abspath(os.path.dirname(__file__))
            DOWNLOAD_DIR = HOME_DIR + '/landsat'
            ZIP_DIR = DOWNLOAD_DIR + '/zip'
        else:
            ZIP_DIR = args.outputRepository
        
        if args.subs == 'search':

            try:
                if args.start:
                    args.start = reformat_date(parse(args.start))

                if args.end:
                    args.end = reformat_date(parse(args.end))
            except TypeError:
                exit("You date format is incorrect. Please try again!", 1)

            s = Search()
            
            clipper = Clipper()
            if args.search_subs == 'shapefile':
                clipper.shapefile(args.path)
            elif args.search_subs == 'query':
                clipper.query(args.name)
            
            result = s.search(args.limit,args.start,args.end,clipper)
            try:
                if result['status'] == 'SUCCESS':
                    if result['total'] > 200:
                        exit('Too many results. Please narrow your search or limit your query with -l options')
                    else:
                        if args.outputRepository:
                            with open(ZIP_DIR+'/result.geojson', 'w') as outfile:
                                json.dump(result['results'], outfile)
                            print ("The geojsonFIle have been created  here: %s" %
                                 ZIP_DIR)
                        else:
                            print ("the IDs which matched with request are : ")
                            for i in result['ID']:
                                print (i)
                    
                    if args.download:
                        gs = GsHelper(ZIP_DIR)
                        if (args.password) and (args.user):
                            print('Starting the download:')
                            for item in result['downloads']:
                                login=args.user
                                mdp=args.password
                                gs.single_download(login,mdp,item['download'],item['id'],ZIP_DIR)
                                print ("%s have been downloaded ... continuing downloading" % item['id'])
                            print("%s images were downloaded"
                                  % result['total'])
                            exit("The downloaded images are located here: %s" %
                                 ZIP_DIR)
                        else:
                             exit("Please give a loggin and a password for theia downloading")
                    else:
                        exit("")
                elif result['status'] == 'error':
                    exit(result['message'])
            except KeyError:
                exit('Too Many API queries. You can only query DevSeed\'s '
                     'API 5 times per minute', 1)

        elif args.subs == 'download':
            gs = GsHelper(ZIP_DIR)
            print('Starting the download:')
            if (args.password) and (args.user):
                for scene in args.scenes:
                    login=args.user
                    mdp=args.password
                    download='http://spirit.cnes.fr/resto/Landsat/'+scene+'/$download'
                    testD=gs.checkifDownloadExist(login,mdp,download,scene)
                    if testD:
                        gs.single_download(login,mdp,download,scene,ZIP_DIR)
                    else:
                        exit("SceneID has not been founded or wrong User/Password given!")
                exit("The downloaded images are located here: %s" % gs.zip_dir)
            else:
                exit("Please give a loggin and a password for theia downloading")


def exit(message, code=0):
    print(message)
    sys.exit(code)

def __main__():

    global parser
    parser = args_options()
    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    __main__()