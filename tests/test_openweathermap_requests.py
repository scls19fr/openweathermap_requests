#!/usr/bin/env python
# encoding: utf-8

from nose.tools import raises, with_setup, eq_, ok_

import openweathermap_requests
from openweathermap_requests import *
import datetime
#import logging
import six

def test_version():
    """Test version"""
    version = openweathermap_requests.__version__
    print(version)
    assert(isinstance(version, six.string_types))

(lon, lat) = (0.34189, 46.5798114) # Poitiers (LFBI / 5530)
#(lon, lat) = (2.3488000, 48.8534100) # Paris,FR

def create_open_weather_map():
    "set up test fixtures"
    #logger = logging.getLogger()
    #logger.setLevel(logging.DEBUG)
    api_key = get_api_key()
    ow = OpenWeatherMapRequests(api_key=api_key)
    return ow
 
def test_get_weather():
    ow = create_open_weather_map()
    data = ow.get_weather(lon=lon, lat=lat)
    print(data)
    assert(data['sys']['country']=='FR')

def test_find_stations_near():
    ow = create_open_weather_map()
    stations = ow.find_stations_near(lon=lon, lat=lat, cnt=1)
    print(stations)
    #station_name = stations.iloc[0]['station.name']
    #assert(station_name=='LFBI')
    distance = stations.iloc[0]['distance']
    assert(distance<200)

#def test_get_historic_weather_by_station_id():
#    ow = create_open_weather_map()
#    stations = ow.find_stations_near(lon=lon, lat=lat, cnt=1)
#    station_id = stations.iloc[0]['station.id']
#    end_date = datetime.datetime.now() - datetime.timedelta(days=30)
#    start_date = end_date - datetime.timedelta(days=10)
#    data = ow.get_historic_weather(station_id, start_date, end_date)
#    print(data)
#    assert(len(data)>0)

def test_get_historic_weather_by_place():
    ow = create_open_weather_map()
    place = 'Paris,FR'
    end_date = datetime.datetime.now() - datetime.timedelta(days=30)
    start_date = end_date - datetime.timedelta(days=10)
    data = ow.get_historic_weather(place, start_date, end_date)
    print(data)
    assert(len(data)>0)
