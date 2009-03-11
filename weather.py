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
import urllib
import xml.sax
import xml.sax.handler
from bbcweatherparser import BBCWeatherHandler

class Weather():
  """s"""

  def __init__(self):
    bbchandler = BBCWeatherHandler()
    bbcrss = urllib.urlopen("http://feeds.bbc.co.uk/weather/feeds/rss/5day/world/8.xml")
    txtrss = bbcrss.read()
    p = xml.sax.parseString(txtrss, bbchandler)

    weather = []
    for item in bbchandler.fItems:
      self.lastupdated = item['pubDate']
      weather.append(item['title'].split(',')[0])

    self.today = weather[0].split()[0][:-1]
    self.tomorrow = weather[1].split()[0][:-1]
    self.aftertomorrow = weather[2].split()[0][:-1]
    self.forecasttoday = weather[0].split()[1]+' '+weather[0].split()[2]
    self.forecasttomorrow = weather[1].split()[1]+' '+weather[1].split()[2]
    self.forecastaftertomorrow = weather[2].split()[1]+' '+weather[2].split()[2]

  def _get_today(self):
    return self._today

  def _set_today(self, value):
    self._today = value

  def _get_tomorrow(self):
    return self._tomorrow

  def _set_tomorrow(self, value):
    self._tomorrow = value

  def _get_aftertomorrow(self):
    return self._aftertomorrow

  def _set_aftertomorrow(self, value):
    self._aftertomorrow = value

  def _get_lastupdated(self):
    return self._lastupdated

  def _set_lastupdated(self, value):
    self._lastupdated = value

  def _get_forecasttoday(self):
    return self._forecasttoday

  def _set_forecasttoday(self, value):
    self._forecasttoday = value

  def _get_forecasttomorrow(self):
    return self._forecasttomorrow

  def _set_forecasttomorrow(self, value):
    self._forecasttomorrow = value

  def _get_forecastaftertomorrow(self):
    return self._forecastaftertomorrow

  def _set_forecastaftertomorrow(self, value):
    self._forecastaftertomorrow = value

  def _get_lastupdated(self):
    return self._lastupdated


  today = property(_get_today, _set_today)
  tomorrow = property(_get_tomorrow, _set_tomorrow)
  aftertomorrow = property(_get_aftertomorrow, _set_aftertomorrow)
  forecasttoday = property(_get_forecasttoday, _set_forecasttoday)
  forecasttomorrow = property(_get_forecasttomorrow, _set_forecasttomorrow)
  forecastaftertomorrow = property(_get_forecastaftertomorrow,
                                   _set_forecastaftertomorrow)
  lastupdated = property(_get_lastupdated, _set_lastupdated)


# if __name__ == '__main__':
#   from lxml import etree
#   todayGifUrl = etree.XML(txtrss).find('.//image/url').text
#   todayGifAux = urllib.urlopen(todayGifUrl).read()
#   todayGif = open('3.gif', 'w')
#   todayGif.write(todayGifAux)
#   todayGif.close()


