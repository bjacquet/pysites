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
import string,logging
from weather import Weather
from rhbase import ReqHBase
from urlparse import urlsplit

html = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <title>Next 3 days forecast</title>
  </head>
  <body>
    <h1>London weather forecast</h1>
    <h2>Today</h2>
    <p><strong>{today}:</strong> {forecasttoday}</p>
    <h2>Tomorrow</h2>
    <p><strong>{tomorrow}:</strong> {forecasttomorrow}</p>
    <h2>After Tomorrow</h2>
    <p><strong>{aftertomorrow}:</strong> {forecastaftertomorrow}</p>
  </body>
</html>
"""

class ReqH(ReqHBase):
    do_nothing = 0

    @staticmethod
    def do_purge(req=None):
        logging.info("do_purge() called for params: '%s'" % urlsplit(req)[3])
        londonweather = Weather()
        retpage = html.replace('{today}', londonweather.today)
        retpage = retpage.replace('{forecasttoday}',
                                  londonweather.forecasttoday)
        retpage = retpage.replace('{tomorrow}', londonweather.tomorrow)
        retpage = retpage.replace('{forecasttomorrow}',
                                  londonweather.forecasttomorrow)
        retpage = retpage.replace('{aftertomorrow}',
                                  londonweather.aftertomorrow)
        retpage = retpage.replace('{forecastaftertomorrow}', 
                                  londonweather.forecastaftertomorrow)
        return retpage
