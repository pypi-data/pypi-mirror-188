fires module
============

Query broadcasted news related to wildfires and visualize them using spatial aggregations.

The service filters thousands of online news sources mentioning occurred wildfires. 
We constructed a web mercator spatial grid having a grid size being optimized for geographic visualization. 
Each grid cell is enriched with a count attribute representing the number of news article related to locations of the corresponding grid cell.

The service uses the impressive data source provided by the `Global Database of Events, Language and Tone (GDELT) Project <https://www.gdeltproject.org>`__.
The service aggregates locations where some kind of wildfire took place using geospatial intelligence operations. 
The geospatial results support the GeoJSON and Esri Features format out of the box.

All endpoints support a date parameter for filtering the results. 
For best sustainability, the serverless cloud-backend queries the articles from the knowledge graph and calculates the geospatial features on-the-fly.

.. image:: https://geospatial-ai.de/wp-content/uploads/2022/03/148703806-071bbb42-59c7-4cb8-aa42-cb08814db5df.png

For example:

>>> from georapid.client import GeoRapidClient
>>> from georapid.factory import EnvironmentClientFactory
>>> from georapid.fires import articles
>>> host = "geofires.p.rapidapi.com"
>>> client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
>>> articles(client)

.. automodule:: georapid.fires
    :members:
