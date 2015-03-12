
=======
# landsat_theia
Tools for download and search satellite images from theia based on the tools from developpement seed (landsat-utils)
. This toolbox is developped in python

<h2>Installation<b></h2>

mkdir PATH/TO/INSTALL <br>
git clone git+git://github.com/yoannMoreau/landsat_theia.git <br>
cd  PATH/TO/INSTALL/landsat_theia <br>
python python/landsat_theia.py -h <br>

( or you cas Use pip to install landsat-theia )

<h2>Overview: What can landsat-theia do?</h2>

landsat-theia has two main functions, it's based on lansat-theia developp for searching, downloading and processing Landsat8 imagery. Process possibility has not been maintained in that version due to high possibility of gdal toolbox. theia is a CNES plaform which distribute freely landsat imagery with atmospheric correction (based on SMAC and temporal algorithm), snow/cloud/shadow mask on a sentinel-2 tiles format. All scene on France are treated within a timelaps on 1.5 month.
Web interface could be used for manually download at http://spirit.cnes.fr/resto/Landsat/
More detail on the blog : http://www.cesbio.ups-tlse.fr/multitemp/

Search for landsat tiles based on several search parameters.
Download landsat images.

Help: Type landsat_theia -h for detailed usage parameters.

the command Line of landsat_theia is create as :<br>
<b>landsat_theia [ACTION {download/search}] [parameters of ACTION] [location{query/shapefile or sceneID for download}]</b>

<h2>Step 1: Search</h2>

Search returns information about all landsat tiles that match your criteria. The most important result is the tile's sceneID, which you will need to download the tile (see step 2 below).

Search for landsat tiles in a given geographical region, using any of the following:

query based on sémantic description of your needs such as 
for Date and location. Unfortunately it should be in french until soon next update on theia site
"LANDSAT7 images entre janvier et juin 2009"
"LANDSAT8 images sur  Toulouse acquises en mai 2013 "
Custom shapefile: Use a tool such as http://geojson.io/ to generate custom shapefiles bounding your geographical region of interest. Landsat-theia will download tiles within this shapefile.
Additionally filter your search using the following parameters:

Start and end dates for when imagery was taken
Examples of search:

<h5>Search a town:</h5>

$: landsat_theia search --start "january 1 2014" --end "August 25 2014" query 'Toulouse'

<h3>Search by custom shapefile:</h3>

$: landsat_theia search  --start "july 01 2014" --end "august 1 2014" shapefile path/to/shapefile.shp

<h5>Limit Search :</h5>

$: landsat_theia search  --limit 1 --start "july 01 2014" --end "august 1 2014" query "toulouse"

<h5>export Search result </h5>
Search result could be export directily in geojson format for been open in a SIG format. Result will be export name as  
results.geojson in the outfile Repository if declared in parameters

landsat_theia search  -o /PATH/TO/RESULT --limit 1 --start "july 01 2014" --end "august 1 2014" query "toulouse" 

<h2>Step 2: Download</h2>

You can download tiles using their unique sceneID, which you get from landsat search.

Examples of download:

RMQ : It's important to create a login/password before downloading images. Please do it at this adress http://spirit.cnes.fr/resto/Landsat/, it's free and really simple to create 

<h5>Download images by their custom sceneID, which you get from landsat search: </h5>
$: landsat_theia download  -u  USER -p MYPASSWORD LANDSAT8_OLITIRS_XS_20150105_N2A_France-MetropoleD0002H0002

<h5>Search and download tiles all at once with the --download flag: </h5>
$: landsat_theia search --download -u  USER -p MYPASSWORD --start "january 01 2014" --end "january 10 2014"  query 'Toulouse'
or
$: landsat_theia search -d -s "january 01 2014" -e "january 10 2014"  -u  MYLOG -p MYPASSWORD query 'Toulouse'

<h5>Search and download tiles all at once with the --download flag in a specific directory:</h5>
$: landsat_theia search --download  -o /PATH/TO/MY/RESULT -u USER -p MYPASSWORD --start "january 01 2014" --end "january 10 2014"  query 'Toulouse'

RMQ : a result.geofile will be writen in such directory. Be sure to have write in such repository.


<h2>Important Notes </h2>

All downloaded and processed images are stored by default in your home directory in landsat forlder: ~/landsat
If you are not sure what images you are looking for, make sure to use --onlysearch flag to view the results first. Run the search again if you need to narrow down your result and then start downloading images. Each image is usually more than 400mb Semantic search might takes a very long time if there are too many images to download, It's possible to use a limit parameter to limit downloading but neverthless be sure of wich images you needs and favorise downloading by SceneID of area of interest thanks to shapefile.

To Do List

Improve console output
Maintain with bug error 

