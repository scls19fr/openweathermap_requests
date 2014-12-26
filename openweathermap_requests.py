#!/usr/bin/env python
# encoding: utf-8

import click
import os
import logging
import logging.config
import traceback
from openweathermap_requests import OpenWeatherMapRequests, ENV_VAR_API_KEY
import pprint

@click.command()
#@click.option('--expire_after', default=-1, help=u"Cache expiration (-1: no cache expiration, 0: no cache, d: d seconds expiration cache)")
@click.option('--api_key', default='', help=u"API Key for Wunderground")
@click.option('--lon', default=0.34189, help=u"Longitude")
@click.option('--lat', default=46.5798114, help=u"Latitude")
@click.option('--count', default=1, help=u"Weather station count")
#@click.option('--place', default='Poitiers', help=u"Place")
@click.option('--range', default='', help=u"Date range (YYYYMMDD:YYYYMMDD) or date (YYYYMMDD) or '' (current weather)")
def main(api_key, lon, lat, count, range):
    logging.info("OpenWeatherMaps.org - API fetch with Requests and Requests-cache")

    if api_key=='':
        try:
            api_key = os.environ[ENV_VAR_API_KEY]
        except:
            logging.warning("You should get an API key from OpenWeatherMap.org and pass it us using either --api_key or using environment variable %r" % ENV_VAR_API_KEY)
            api_key = None
    
    pp = pprint.PrettyPrinter(indent=4)
    
    cache_name = 'cache-openweathermap'
    if range=='':
        if count==1:
            #ow = OpenWeatherMapRequests(api_key=api_key, cache_name='openweathermaps-cache', expire_after=datetime.timedelta(minutes=5))
            ow = OpenWeatherMapRequests(api_key=api_key, cache_name=cache_name, expire_after=5*60)
            logging.info("get_weather")
            data = ow.get_weather(lon=lon, lat=lat)
            pp.pprint(data)
        else:
            ow = OpenWeatherMapRequests(api_key=api_key, cache_name=cache_name, expire_after=24*60*60)
            logging.info("find_stations_near")
            data = ow.find_stations_near(lon=lon, lat=lat, cnt=count)
            print(data)

    else:
        ow = OpenWeatherMapRequests(api_key=api_key, cache_name=cache_name, expire_after=None) # no expiration for history
        range = range.split(':')
        range = map(pd.to_datetime, range)
        if len(range)==1:
            range.append(range[0]+datetime.timedelta(days=1))
        logging.info("get_historic_weather")
        start_date = range[0]
        end_date = range[1]

        stations = ow.find_stations_near(lon=lon, lat=lat, cnt=1)
        logging.info("\n%s" % stations)
        station_id = stations.iloc[0]['station.id']

        data = ow.get_historic_weather(station_id, start_date, end_date)
        logging.info("\n%s" % data)

        format = "%Y%m%d"
        range_str = "%s_%s" % (start_date.strftime(format), end_date.strftime(format))

        filename = "openweathermap_%s_%s_%s.csv" % (lon, lat, range_str)
        logging.info("Creating file %s" % filename)
        data.to_csv(filename)

        filename = "openweathermap_%s_%s_%s.xls" % (lon, lat, range_str)
        logging.info("Creating file %s" % filename)
        data.to_excel(filename, engine='openpyxl') # see https://github.com/pydata/pandas/issues/9139

if __name__ == '__main__':
    basepath = os.path.dirname(__file__)
    logging.config.fileConfig(os.path.join(basepath, "logging.conf"))
    logger = logging.getLogger("simpleExample")
    main()
