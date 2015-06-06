#!/usr/bin/env python
# encoding: utf-8

"""
OpenWeatherMapRequests to fetch data using requests and requests-cache

"""

import requests
import requests_cache
import datetime
import os
import logging
import logging.config
import traceback
import six
from six.moves.urllib.parse import urlencode
import json
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import collections
#from bunch import bunchify

from .version import __author__, __copyright__, __credits__, \
    __license__, __version__, __maintainer__, __email__, __status__, __url__

# resolution
#   tick, hour, day

ENV_VAR_API_KEY = 'OPEN_WEATHER_MAP_API_KEY'

def get_api_key(api_key=''):
    if api_key=='' or api_key is None:
        try:
            return(os.environ[ENV_VAR_API_KEY])
        except:
            logging.warning("You should get an API key from OpenWeatherMap.org and pass it us using either --api_key or using environment variable %r" % ENV_VAR_API_KEY)
            return('')
    else:
        return(api_key)

class RequestsCachedSessionWithLog(requests_cache.CachedSession):
    """
    Requests Session with log and cache mechanism
    """
    def get(self, url, **kwargs):
        try:
            params = kwargs['params']
        except:
            params = {}
        if params=={}:
            logging.debug("Request to '%s'" % url)
        else:
            logging.debug("Request to '%s' with '%s' using '%s'" % (url, params, url+'?'+urlencode(params)))
        response = super(RequestsCachedSessionWithLog, self).get(url, **kwargs)
        return(response)

def pd_timestamp_to_timestamp(dt, unit='s'):
    """
    Returns unix timestamp (int) from Pandas Timestamp
    """
    d_unit = {
        's': 1E9,
        'ms': 1E6,
        'us': 1E3,
        'ns': 1,
    }
    return(int(dt.value/d_unit[unit]))


def datetime_to_timestamp(dt):
    """
    Returns unix timestamp (int) from datetime
    """
    return(int((dt - datetime.datetime(1970, 1, 1)).total_seconds()))

def gen_chunks_start_end_date(start=None, end=None, chunksize=None):
    """
    Generator which returns start, end date for each chunk
    """

    freq = datetime.timedelta(days=1)
    offset = 0
    dt = start

    try:
        if chunksize>0:
            while True:
                dt1 = start + offset * freq
                dt2 = dt1 + (chunksize-1) * freq
                if dt2>=end:
                    dt2 = end
                    yield(dt1, dt2)
                    break
                yield(dt1, dt2)
                offset += chunksize
        else:
            yield(start, end)
    except:
        yield(start, end)

def temp_K_to_C(temp):
    """
    Returns celcius from kelvin
    """
    return(temp-273.15)

def stations_to_df(data):
    df_stations = json_normalize(data)
    return(df_stations)

def historic_weather_to_df(data):
    data = data['list']
    if len(data)==0:
        raise(Exception("Empty list"))
    df = json_normalize(data)
    df['dt'] = pd.to_datetime(df['dt'], unit='s')
    for col in df.columns:
        if 'temp.' in col and 'temp.c' not in col\
                or 'temp_max' in col\
                or 'calc.dewpoint' in col and 'calc.dewpoint.c' not in col\
                or 'calc.heatindex' in col and 'calc.heatindex.c' not in col\
                or 'calc.humidex' in col and 'calc.humidex.c' not in col:
            df[col] = df[col].map(temp_K_to_C)
    df = df.set_index('dt')
    return(df)

def json_loads(data):
    try:
        data = json.loads(data)
        return(data)
    except:
        logging.debug(data)
        logging.error(traceback.format_exc())
        raise

class OpenWeatherMapRequests(object):
    def __init__(self, *args, **kwargs):
        self.BASE_URL = 'http://api.openweathermap.org/data/2.5'

        self.MAX_RETRIES_DEFAULT = 3
        self.CHUNKSIZE_DEFAULT = 30

        try:
            self.api_key = kwargs['api_key']
        except:
            self.api_key = None

        try:
            cache_name = kwargs['cache_name']
        except:
            cache_name = 'cache'

        try:
            backend = kwargs['backend']
        except:
            backend = None

        try:
            expire_after = kwargs['expire_after']
        except:
            expire_after = 0 # 0: no cache - None: no cache expiration

        if expire_after==0:
            logging.debug("Requests without cache")
        else:
            logging.info("Installing cache '%s' with expire_after=%s (seconds)" % (cache_name, expire_after))
            if expire_after is None:
                logging.warning("expire_after is None - no cache expiration!")
        self.session = RequestsCachedSessionWithLog(cache_name, backend, expire_after)

        try:
            self.max_retries = kwargs['max_retries']
        except:
            self.max_retries = self.MAX_RETRIES_DEFAULT

        try:
            self.chunksize = kwargs['chunksize']
        except:
            self.chunksize = self.CHUNKSIZE_DEFAULT

        a = requests.adapters.HTTPAdapter(max_retries=self.max_retries)
        b = requests.adapters.HTTPAdapter(max_retries=self.max_retries)
        self.session.mount('http://', a)
        self.session.mount('https://', b)

    def _url(self, endpoint):
        return(self.BASE_URL + endpoint)

    def get_historic_weather(self, station_id, start_date=None, end_date=None, resolution=None):
        if isinstance(start_date, six.string_types):
            start_date = pd.to_datetime(start_date)
        if isinstance(end_date, six.string_types):
            end_date = pd.to_datetime(end_date)
        lst = []
        for i, (start_date, end_date) in enumerate(gen_chunks_start_end_date(start_date, end_date, self.chunksize)):
            try:
                logging.info("%d: from %s to %s" % (i+1, start_date, end_date))
                data = self._get_historic_weather(station_id, start_date, end_date, resolution)
                #logging.info(data)
                lst.append(data)
                #time.sleep(2)
            except:
                logging.error(traceback.format_exc())
        logging.info("Build concatenated DataFrame")
        df_all = pd.concat(lst)
        return(df_all)

    def _get_historic_weather(self, station_id, start_date=None, end_date=None, resolution=None):
        if resolution is None:
            resolution = 'hour'
        endpoint = '/history/station'
        params = {
            'appid': self.api_key,
            'id': station_id,
            'type': resolution,
            'start': datetime_to_timestamp(start_date),
            'end': datetime_to_timestamp(end_date) - 1
        }
        url = self._url(endpoint)
        response = self.session.get(url, params=params)
        #if response.status_code!=200:
        #    raise(NotImplementedError("Request error"))
        #data = response.text
        #data = json_loads(data)
        #data = historic_weather_to_df(data)
        data = historic_weather_to_df(response.json())
        return(data)

    def find_stations_near(self, lon, lat, cnt):
        """
        Searches for weather station near a given coordinate and
        returns them, ordered by distance
        """
        endpoint = "/station/find"
        params = {
            'appid': self.api_key,
            'lat': lat,
            'lon': lon,
            'cnt': cnt,
        }
        url = self._url(endpoint)
        response = self.session.get(url, params=params)
        #if response.status_code!=200:
        #    raise(NotImplementedError("Request error"))
        #data = response.text
        #data = json_loads(data)
        #data = stations_to_df(data)
        data = stations_to_df(response.json())
        return(data)

    def get_weather(self, lon, lat):
        """
        Returns recent weather data for given station
        """
        endpoint = "/weather"
        params = {
            'appid': self.api_key,
            'lat': lat,
            'lon': lon,
        }
        url = self._url(endpoint)
        response = self.session.get(url, params=params)
        if response.status_code!=200:
            raise(NotImplementedError("Request error"))
        #data = response.text
        #data = json_loads(data)
        data = response.json()
        #data = bunchify(data)
        for key in ['temp', 'temp_max', 'temp_min']:
            data['main'][key] = temp_K_to_C(data['main'][key])
        data['dt'] = pd.to_datetime(data['dt'], unit='s')
        data['sys']['sunrise'] = pd.to_datetime(data['sys']['sunrise'], unit='s')
        data['sys']['sunset'] = pd.to_datetime(data['sys']['sunset'], unit='s')
        return(data)
