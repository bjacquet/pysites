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
from lxml import etree
from urllib import urlopen
from StringIO import StringIO


class RSSParser():
    """Parser handler class for parsing rss feeds"""

    def __init__(self):
        pass

    def _set_tags(self, value):
        self._tags = value

    def _get_tags(self):
        return self._tags

    def _set_urlfeed(self, value):
        self._urlfeed = value
    
    def _get_urlfeed(self):
        return self._urlfeed
    
    tags = property(_get_tags, _set_tags)
    urlfeed = property(_get_urlfeed, _set_urlfeed)

    def parseFeed(self, child=False):
        if self.tags is None or self.urlfeed is None:
            return None
        rssfeed = urlopen(self.urlfeed)
        txtrss = rssfeed.read()
        self._tree = etree.parse(StringIO(txtrss))
        parsedTags = self._parseTags(child)

        return parsedTags
    
    def _parseElement(self, element, childs=False):
	dic = {}
	dic['text'] = self._getText(element)
	dic['attributes'] = self._getAttributes(element)
	if not self._isFinalElement(element) and childs:
		dic['children'] = self._parseElementChildrens(element.getchildren())
	return dic

    def _isFinalElement(self, element):
        if [] == element.getchildren():
            return True
        else:
            return False

    def _parseElementChildrens(self, childrens):
	childs = {}
	for children in childrens:
		childs[children.tag] = self._parseElement(children)
	return childs

    def _getAttributes(self, element):
	return element.attrib

    def _getText(self, element):
	return element.text

    def _parseTags(self, child=False):
        rettags = {}
        for tag in self.tags:
		rettags[tag] = self._parseElement(self._tree.xpath(tag)[0], 
                                                  child)
	return rettags
