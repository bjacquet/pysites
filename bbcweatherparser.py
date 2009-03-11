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
import xml.sax


class BBCWeatherHandler(xml.sax.handler.ContentHandler):
  """Parser handler class for parsing news"""

  def __init__(self):
    xml.sax.handler.ContentHandler.__init__(self)
    self._fItems = []
    self.__fCurItem = None
    self.__fText = []

  def startElement(self, name, attrs):
    if name == 'item':
      self.__fCurItem = {}
    self.__fText = []

  def endElement(self, name):
    if name == 'item':
      self._fItems.append(self.__fCurItem)
      self.__fCurItem = None
    elif self.__fCurItem is not None:
      self.__fCurItem[name] = ''.join(self.__fText).strip()

  def characters(self, content):
      self.__fText.append(content)
  
  def _get_fItems(self):
    return self._fItems

  fItems = property(_get_fItems)


