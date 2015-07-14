[![Latest Version](https://img.shields.io/pypi/v/openweathermap_requests.svg)](https://pypi.python.org/pypi/openweathermap_requests/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/openweathermap_requests.svg)](https://pypi.python.org/pypi/openweathermap_requests/)
[![Wheel format](https://img.shields.io/pypi/wheel/openweathermap_requests.svg)](https://pypi.python.org/pypi/openweathermap_requests/)
[![License](https://img.shields.io/pypi/l/openweathermap_requests.svg)](https://pypi.python.org/pypi/openweathermap_requests/)
[![Development Status](https://img.shields.io/pypi/status/openweathermap_requests.svg)](https://pypi.python.org/pypi/openweathermap_requests/)
[![Downloads monthly](https://img.shields.io/pypi/dm/openweathermap_requests.svg)](https://pypi.python.org/pypi/openweathermap_requests/)
[![Requirements Status](https://requires.io/github/scls19fr/openweathermap_requests/requirements.svg?branch=master)](https://requires.io/github/scls19fr/openweathermap_requests/requirements/?branch=master)
[![Documentation Status](https://readthedocs.org/projects/openweathermap-requests/badge/?version=latest)](http://openweathermap-requests.readthedocs.org/en/latest/)
[![Sourcegraph](https://sourcegraph.com/api/repos/github.com/scls19fr/openweathermap_requests/.badges/status.png)](https://sourcegraph.com/github.com/scls19fr/openweathermap_requests)
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/scls19fr/openweathermap_requests?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Code Health](https://landscape.io/github/scls19fr/openweathermap_requests/master/landscape.svg?style=flat)](https://landscape.io/github/scls19fr/openweathermap_requests/master)
[![Build Status](https://travis-ci.org/scls19fr/openweathermap_requests.svg)](https://travis-ci.org/scls19fr/openweathermap_requests)

OpenWeatherMap Requests
=======================

[Python](https://www.python.org/) package to fetch data from [OpenWeatherMap.org](http://openweathermap.org/) using [Requests](http://docs.python-requests.org/) and [Requests-cache](https://requests-cache.readthedocs.org) and get [Pandas DataFrame](http://pandas.pydata.org/) with weather history.

Command Line Interface Usage
----------------------------

### Current weather

Get current weather data

    $ python openweathermap_requests.py --lon 0.34189 --lat 46.5798114

### Historical weather data

Fetch historical weather data from nearest weather station of coordinates (lon=0.34189, lat=46.5798114) from 2014/01/01 to 2014/12/01 using:

    $ python openweathermap_requests.py --lon 0.34189 --lat 46.5798114 --range 20140101:20141201

Library Usage
-------------

    import datetime
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    from openweathermap_requests import OpenWeatherMapRequests

    ow = OpenWeatherMapRequests(api_key='', cache_name='cache-openweathermap', expire_after=5*60)

    (lon, lat) = (0.34189, 46.5798114) # Poitiers

    data = ow.get_weather(lon=lon, lat=lat)  # display current weather data
    print(data)

    stations = ow.find_stations_near(lon=lon, lat=lat, cnt=10) # get 10 nearest stations from coordinates (lon, lat)

    station_id = stations.iloc[0]['station.id'] # get station_id of nearest station

    start_date = datetime.datetime(2014, 1, 1)
    end_date = datetime.datetime(2014, 6, 1)

    data = ow.get_historic_weather(station_id, start_date, end_date) # get historic weather from start date to end date
    print(data)

Install
-------

### From Python package index

    $ pip install openweathermap_requests

### From source

Get latest version using Git

    $ git clone https://github.com/scls19fr/openweathermap_requests.git
    $ cd openweathermap_requests
    $ python setup.py install

Links
-----

-   Documentation can be found at [Read The Docs](http://openweathermap-requests.readthedocs.org/) ;
-   Source code and issue tracking can be found at [GitHub](https://github.com/scls19fr/openweathermap_requests).
-   Feel free to [tip me](https://gratipay.com/scls19fr/)!
