joins module
===============

Joins two spatially enabled feature collections based on their relative spatial locations.

A spatial relationship match joins the properties of the input with the properties of the target features. 
Therefore, the result features of every match get the geometry from the input features and the properties of both. 
So that a spatial join represents an inner join between two feature collections.

.. figure:: https://geospatial-ai.de/wp-content/uploads/2022/09/image-1.png

    Geospatial Feature Collections located in Dessau

Contains
--------
Joins the input features from 'left' with the matching target features from 'right' for all input features containing the target features. 
Therefore, the target geometry must be completely inside the input geometry. 
So that no points of the target geometry lie in the input's exterior geometry, and at least one point of the interior of the target geometry lies in the input's interior geometry.

.. figure:: https://geospatial-ai.de/wp-content/uploads/2022/09/image.png

    Building containing one location

Crosses
-------
Joins the input features from 'left' with the matching target features from 'right' for all input features covering the target features. 
Therefore, no point of the target geometry must be outside of the input geometry.

.. figure:: https://geospatial-ai.de/wp-content/uploads/2022/09/image-4.png

    Roads crossing at the intersection of Friedhofstraße and Gliwicer Straße

Intersects
----------
Joins the input features from 'left' with the matching target features from 'right' for all input features intersecting the target features. 
Therefore, the input and target geometry must have any point in common.

.. figure:: https://geospatial-ai.de/wp-content/uploads/2022/09/image-3.png

    Locations intersecting roads

Overlaps
--------
Joins the input features from 'left' with the matching target features from 'right' for all input features overlapping the target features. 
Therefore, the input and target geometry must have the same dimension and at least one point not shared by the other. 
So that the intersection of their interiors results in a geometry, having the same dimension.

.. figure:: https://geospatial-ai.de/wp-content/uploads/2022/09/image-5.png

    Buildings overlapping a specified area of interest

Touches
-------
Joins the input features from 'left' with the matching target features from 'right' for all input features touching the target features. 
Therefore, the input and target geometry must have at least one point in common and all common points lie on at least one boundary. 
So that the input and target interior do not share any point in common.

.. figure:: https://geospatial-ai.de/wp-content/uploads/2022/09/image-6.png

    One location touching four road segments

Within
------
Joins the input features from 'left' with the matching target features from 'right' for all target features containing the input features. 
Therefore, the input geometry must be completely inside the target geometry. 
So that no points of the input geometry lie in the target's exterior geometry, and at least one point of the interior of the input geometry lies in the target's interior geometry.

.. figure:: https://geospatial-ai.de/wp-content/uploads/2022/09/image-7.png

    Buildings being within a specified area of interest

For example:

>>> from georapid.client import GeoRapidClient
>>> from georapid.factory import EnvironmentClientFactory
>>> from georapid.joins import within
>>> host = "geojoins.p.rapidapi.com"
>>> client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
>>> lat = 51.83864
>>> lon = 12.24555
>>> delta = 0.1
>>> xmin, xmax, ymin, ymax = lon-delta, lon+delta, lat-delta, lat+delta
>>> left = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": {
                "id": "left_point"
            }
        }]
    }
    right = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[xmin, ymax], [xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]]]
            },
            "properties": {
                "id": "right_polygon"
            }
        }]
    }
>>> geojson = within(client, left, right)

Functions
---------
.. automodule:: georapid.joins
    :members: