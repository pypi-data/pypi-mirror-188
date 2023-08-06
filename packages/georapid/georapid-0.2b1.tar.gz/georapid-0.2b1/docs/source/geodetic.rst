geodetic module
===============

Enables various geodetic functions like buffers, points from distance and direction, points along path and wedge construction.

The construction of geodetic buffers representing an approximated region or protected area around points of interest is a typical geospatial intelligence task. 
The combination of coordinates or named locations and distance measurements often describes various geospatial activities as events, e.g. wildfires in Grunewald forest around 85 km SSW of Berlin. 
Therefore, you must be able to create points by using distances and directions. 
Locating points using a bunch of distances and offsets along a straight line, which is defined by two locations, is a very common surveying task.

Every parameter representing a linear measurement like a distance, a radius or an offset has a linear unit parameter, e.g. 'km'. 
Direction parameters represent an angular measurement defining the azimuth in degree.

The endpoints support a format parameter which defines if the response contains the result features as a GeoJSON feature collection or an Esri feature set.

Create Buffers
--------------
Creates geodetic buffers representing a region or protected area around the specified locations. 
The distance defines the location of the buffer's boundary as an approximated representation.

.. figure:: https://geospatial-ai.de/wp-content/uploads/2022/09/image-8.png

    Two 150 kilometer buffers around Bonn and Dessau

Create Points along
-------------------
Creates points along the line defined by lat1, lon1 and lat2, lon2. The distances define the location along the line, and the offsets define the lateral offset. 
The number of distances must equal the number of offsets. 
A combination of distances=[0, <line length>] and offsets=[0, 0] creates a point at the start and another at the end location.

.. figure:: https://geospatial-ai.de/wp-content/uploads/2022/09/image-9.png

    Three points along the line having different offsets between Dessau and Bonn

Create Points from Direction
----------------------------
Creates points using locations of observers, a distance and a direction representing the azimuth using degree targeting onto the observed location.

.. figure:: https://geospatial-ai.de/wp-content/uploads/2022/09/image-10.png

    Two locations being 150 kilometers in NE direction away from Bonn and Dessau

Create Path from Directions
---------------------------
Creates a path using a start location, a combination of distances defining the location along the path and directions representing the azimuths at every vertex of the path.

.. figure:: https://geospatial-ai.de/wp-content/uploads/2022/09/image-11.png
    
    Create a path starting at the center of Dessau towards Mosigkau using five pairs of azimuth and direction

Create parametric Wedges
------------------------
Creates parametric wedges using locations of observers, a distance, a direction representing the azimuth using degree, and an azimuth span targeting onto the observed location.

.. figure:: https://geospatial-ai.de/wp-content/uploads/2022/09/image-12.png

    Two parametric wedges located at Bonn and Dessau heading 150 km with an azimuth of 45 degree and a span of 25 degree

For example:

>>> from georapid.client import GeoRapidClient
>>> from georapid.factory import EnvironmentClientFactory
>>> from georapid.geodetic import create_wedges
>>> from georapid.units import LinearUnit
>>> host = "geodetic.p.rapidapi.com"
>>> latitudes = [51.83864, 50.73438]
>>> longitudes = [12.24555, 7.09549]
>>> azimuth = 45
>>> azimuth_span = 20
>>> distance = 23.5
>>> geojson = create_wedges(client, latitudes, longitudes, azimuth, azimuth_span, distance, LinearUnit.km)

Functions
---------

.. automodule:: georapid.geodetic
    :members:
