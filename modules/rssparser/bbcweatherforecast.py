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
from rssparser import RSSParser


class BBCWeatherForecast(RSSParser):
    """Parser handler class for the BBC Weather RSS fedd"""

    __title = '/rss/channel/title'
    __lastBuildDate = '/rss/channel/lastBuildDate'
    __day1 = '/rss/channel/item[1]'
    __day2 = '/rss/channel/item[2]'
    __day3 = '/rss/channel/item[3]'

    def __init__(self, urlfeed=None):
        self.tree = None
        self.urlfeed = urlfeed
        self.tags = [self.__title,  self.__lastBuildDate, 
                     self.__day1, self.__day2, self.__day3]

    def parseFeed(self, child=False):
        self.parsedTags = RSSParser.parseFeed(self, child)
        self._setValues()

    def _setValues(self):
        self.day1 = self._get_children_node_text(self.__day1, 'title')

    def _get_text(self, tag):
        return tag['text']

    def _get_children_node_text(self, tag, node):
        return self._get_text(self.parsedTags[tag]['children'][node])

    def _get_title(self):
        return self._get_text(self.parsedTags[self.__title])

    def _get_lastBuildDate(self):
        return self._get_text(self.parsedTags[self.__lastBuildDate])

    def _get_day1(self):
        return self._day1

    def _set_day1(self, value):
        #self._day1 = value.replace(u'\xb0', u'00B0')
        self._day1 = value#.replace(u'\xb0', u'deg')

    def _get_day2(self):
        return self._get_children_node_text(self.__day2, 'title')

    def _get_day3(self):
        return self._get_children_node_text(self.__day3, 'title')

    def _get_day1forecast(self):
        return self._get_children_node_text(self.__day1, 'description')

    def _get_day2forecast(self):
        return self._get_children_node_text(self.__day2, 'description')

    def _get_day3forecast(self):
        return self._get_children_node_text(self.__day3, 'description')

    day1 = property(_get_day1, _set_day1)
    day2 = property(_get_day2)
    day3 = property(_get_day3)
    day1forecast = property(_get_day1forecast)
    day2forecast = property(_get_day2forecast)
    day3forecast = property(_get_day3forecast)
    lastBuildDate = property(_get_lastBuildDate)
    title = property(_get_title)
