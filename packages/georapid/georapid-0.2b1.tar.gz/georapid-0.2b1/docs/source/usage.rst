Usage
=====

.. _installation:

Installation
------------

To use georapid, first install it using pip:

.. code-block:: console

   (.venv) $ pip install georapid

Creating clients
----------------

To authorize against the endpoints being hosted on Rapid API you need to use your own Rapid API key.
The default client factory reads the API key from an environment variable named 'x_rapidapi_key'.

Creating a client for a specific host,
you can use the following function:

.. autofunction:: georapid.factory.EnvironmentClientFactory.create_client_with_host
    :noindex:

The ``host`` parameter must target the specific host like ``"geoprotests.p.rapidapi.com"``.
Furthermore, the factory directly access ``os.environ['x_rapidapi_key']`` and uses the specified API key as a header parameter.
Otherwise, :py:func:`georapid.factory.EnvironmentClientFactory.create_client_with_host` will raise a :exc:`ValueError`.

Every service endpoint has its own module. 
The protests module offers access to the news articles mentioning occurred protests or demonstrations.
You need to import the ``articles`` function from the module and call it using a valid client instance.
If you do not specifiy a date, the function returns the corresponding articles from yesterday as a JSON object.

For example:

>>> from georapid.client import GeoRapidClient
>>> from georapid.factory import EnvironmentClientFactory
>>> from georapid.protests import articles
>>> host = "geoprotests.p.rapidapi.com"
>>> client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
>>> articles(client)
"articles": [{ 
   "url": "https://www.tt.com/artikel/18526556/traenengaseinsatz-gegen-demonstranten-im-sudan", 
   "urlmobile": "", 
   "title": "Tränengaseinsatz gegen Demonstranten im Sudan | Tiroler Tageszeitung Online", 
   "seendate": "20211231T003000Z", 
   "socialimage": "", 
   "domain": "tt.com", 
   "language": "German", 
   "sourcecountry": "Austria"},
   ...
]

Mapping
-------

There are specific service endpoints offering location-enabled entities also known as geospatial features. 
As an analyst you need to get some insights into the spatial patterns of the domain-specific problems you want to solve.
For instance, mapping all news related to protests by using the mentioned locations e.g. cities, administrative regions and so on usually leads to an overload of information.
Therefore, the location-enabled service endpoints offer spatial aggregations. 

Spatial binning aggregates locations into a pre-defined spatial grid structure. 
The spatial grid comprises distinct cells having a two-dimensional geometry (e.g. rectangle or polygon). 
We created a simple hexagonal grid supporting the WGS84 and Web Mercator spatial reference. 
The spatial grid offers a point in grid aggregation. 
As a result, the aggregation contains the number of locations intersecting each grid cell in an attribute called hit count.

There are two well-known output formats supporting feature representations. 
GeoJSON is a format for encoding a variety of geographic data structures. 
A GeoJSON object may represent a geometry, a feature, or a collection of features. 
GeoJSON supports the following geometry types: Point, LineString, Polygon, MultiPoint, MultiLineString, and MultiPolygon. 

Esri JSON is a variant of JSON that has been specialized for use with ArcGIS. 
One notable difference between Esri JSON and GeoJSON is that Esri JSON uses a slightly different data model for representing geographic features. 
While GeoJSON uses a simple "feature" object with a "geometry" and an optional "properties" member, Esri JSON uses a more complex "feature set" object that includes a "displayFieldName", "fieldAliases", "geometryType", and "spatialReference" in addition to an array of "features" with "attributes" and "geometry" members.

You need to import the ``aggregate`` function from the module and call it using a valid client instance.
If you do not specifiy a date, the function returns the aggregated articles from yesterday as geospatial features.

For example:

>>> from georapid.protests import aggregate
>>> from georapid.formats import OutFormat
>>> aggregate(client, format=OutFormat.ESRI)
{'geometryType': 'esriGeometryPolygon', 'spatialReference': {'wkid': 102100}, 'fields': [{'name': 'count', 'type': 'esriFieldTypeInteger'}, {'name': 'timestamp', 'type': 'esriFieldTypeDate'}], 'features': ...


We are ging to use the `ArcGIS API for Python <https://developers.arcgis.com/python>`__ which enables access to ready-to-use maps and curated geographic data from Esri and other authoritative sources, and works with your own data as well. 
It integrates well with the scientific Python ecosystem and includes rich support for Pandas and Jupyter notebook.
For more details take a closer look at `Install and Setup <https://developers.arcgis.com/python/guide/install-and-set-up>`__. 

Choose your favourite enironment e.g. conda or pip, create a dedicated environment, and enter the following at the prompt:

.. code-block:: console

   conda install -c esri arcgis
   pip install arcgis

Start a new Juypter notebook instance:

.. code-block:: console

   jupyter notebook

Render the aggregated news related to protests from yesterday:

>>> from georapid.client import GeoRapidClient
>>> from georapid.factory import EnvironmentClientFactory
>>> from georapid.protests import aggregate
>>> from georapid.formats import OutFormat

>>> from arcgis import GIS
>>> from arcgis.features import FeatureSet

>>> host = "geoprotests.p.rapidapi.com"
>>> client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
>>> features_dict = aggregate(client, format=OutFormat.ESRI)
>>> feature_set = FeatureSet.from_dict(features_dict)
>>> feature_set

>>> gis = GIS()
>>> map_view = gis.map()
>>> map_view

.. image:: https://user-images.githubusercontent.com/921231/211210746-165bda47-0420-4b53-833c-ea295fdf6203.png

>>> feature_set.sdf.spatial.plot(map_view)

Terms of use
------------
We designed the geospatial intelligence API services for research and analysis of geospatial knowledge worldwide. 
The geospatial datasets and any result being generated by these API services are available for unrestricted use for academic, commercial, or governmental use of any kind.

Redistribution
--------------
You may redistribute, republish, and mirror the geospatial datasets in any form. 
However, any use or redistribution of the geospatial datasets and results must include a citation to GEOINT API services and a link to our website `Geospatial AI <https://geospatial-ai.de>`__.
The underlying serverless cloud-backend analyses raw geospatial locations of news articles provided by the `Global Database of Events, Language and Tone (GDELT) Project <https://www.gdeltproject.org>`__.