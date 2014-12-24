.. image:: https://pypip.in/version/openweathermap_requests/badge.svg
    :target: https://pypi.python.org/pypi/openweathermap_requests/
    :alt: Latest Version

.. image:: https://pypip.in/py_versions/openweathermap_requests/badge.svg
    :target: https://pypi.python.org/pypi/openweathermap_requests/
    :alt: Supported Python versions

.. image:: https://pypip.in/format/openweathermap_requests/badge.svg
    :target: https://pypi.python.org/pypi/openweathermap_requests/
    :alt: Download format

.. image:: https://pypip.in/license/openweathermap_requests/badge.svg
    :target: https://pypi.python.org/pypi/openweathermap_requests/
    :alt: License

.. image:: https://pypip.in/status/openweathermap_requests/badge.svg
    :target: https://pypi.python.org/pypi/openweathermap_requests/
    :alt: Development Status

.. image:: https://readthedocs.org/projects/openweathermap-requests/badge/?version=latest
   :target: http://openweathermap-requests.readthedocs.org/en/latest/
   :alt: Documentation Status

.. image:: https://sourcegraph.com/api/repos/github.com/scls19fr/openweathermap_requests/.badges/status.png
   :target: https://sourcegraph.com/github.com/scls19fr/openweathermap_requests

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/scls19fr/openweathermap_requests?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. image:: https://travis-ci.org/scls19fr/openweathermap_requests.svg?branch=master
    :target: https://travis-ci.org/scls19fr/openweathermap_requests

OpenWeatherMap Requests
=======================

`Python <https://www.python.org/>`__ package to fetch data from `OpenWeatherMap.org <http://openweathermap.org/>`__
and get `Pandas DataFrame <http://pandas.pydata.org/>`__ with weather history.

Command Line Interface Usage
----------------------------

Current weather
~~~~~~~~~~~~~~~

Get current weather data

::

$ python openweathermap_requests.py --lon 0.34189 --lat 46.5798114


Historical weather data
~~~~~~~~~~~~~~~~~~~~~~~

Fetch historical weather data from nearest weather station of coordinates (lon=0.34189, lat=46.5798114) 
from 2014/01/01 to 2014/12/01 using

::

$ python openweathermap_requests.py --lon 0.34189 --lat 46.5798114 --range 20140101:20141201


Library Usage
-------------



Links
-----

- Documentation can be found at `Read The Docs <http://openweathermap-requests.readthedocs.org/>`__ ;
- Source code and issue tracking can be found at `GitHub <https://github.com/scls19fr/openweathermap_requests>`__.
