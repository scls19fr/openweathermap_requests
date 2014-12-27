#!/usr/bin/env python
# encoding: utf-8

from nose.tools import raises, with_setup, eq_, ok_

import openweathermap_requests
from openweathermap_requests import *
import datetime
#import logging

def test_version():
    """Test version"""
    isinstance(openweathermap_requests.__version__, basestring)

def create_open_weather_map():
    "set up test fixtures"
    #logger = logging.getLogger()
    #logger.setLevel(logging.DEBUG)
    api_key = get_api_key()
    (lon, lat) = (0.34189, 46.5798114) # Poitiers (LFBI / 5530)
    ow = OpenWeatherMapRequests(api_key=api_key)
    return(ow, lon, lat)
 
def test_get_weather():
    (ow, lon, lat) = create_open_weather_map()
    data = ow.get_weather(lon=lon, lat=lat)
    assert(data['sys']['country']=='FR')

def test_find_stations_near():
    (ow, lon, lat) = create_open_weather_map()
    stations = ow.find_stations_near(lon=lon, lat=lat, cnt=1)
    station_name = stations.iloc[0]['station.name']
    assert(station_name=='LFBI')

def test_get_historic_weather():
    (ow, lon, lat) = create_open_weather_map()
    stations = ow.find_stations_near(lon=lon, lat=lat, cnt=1)
    station_id = stations.iloc[0]['station.id']
    end_date = datetime.datetime.now() - datetime.timedelta(days=30)
    start_date = end_date - datetime.timedelta(days=10)
    data = ow.get_historic_weather(station_id, start_date, end_date)
    assert(len(data)>0)
