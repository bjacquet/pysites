#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 by Bruno Jacquet (bruno.jacquet@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import logging
import string
from urlparse import urlsplit
from bbcweatherforecast import BBCWeatherForecast
from rhbase import ReqHBase


html = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <title>London 3 days forecast</title>
  </head>
  <body>
    <h1>{title}</h1>
    <h2>{day1}</h2>
    <p>{day1forecast}</p>
    <h2>{day2}</h2>
    <p>{day2forecast}</p>
    <h2>{day3}</h2>
    <p>{day3forecast}</p>
    <p>Last updated: {lastBuildDate}</p>
  </body>
</html>
"""


class ReqH(ReqHBase):
    do_nothing = 0

    @staticmethod
    def do_purge(req=None):
        logging.info("do_purge() called for params: '%s'" % req)

        londonweather = BBCWeatherForecast("http://feeds.bbc.co.uk/weather/feeds/rss/5day/world/8.xml")
        londonweather.parseFeed(True)

        retpage = html.replace('{title}', londonweather.title)
        retpage = retpage.replace('{day1}', londonweather.day1)
        retpage = retpage.replace('{day1forecast}', londonweather.day1forecast)
        retpage = retpage.replace('{day2}', londonweather.day2)
        retpage = retpage.replace('{day2forecast}', londonweather.day2forecast)
        retpage = retpage.replace('{day3}', londonweather.day3)
        retpage = retpage.replace('{day3forecast}', londonweather.day3forecast)
        retpage = retpage.replace('{lastBuildDate}', londonweather.lastBuildDate)
        return retpage.encode('latin-1')
