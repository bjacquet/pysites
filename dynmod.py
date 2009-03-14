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
import logging, time, urlparse

class Dynmod(object):
    def __init__(self):
        self.modules = dict()

    def load(self, modulepath, classname):
        logging.debug("load() called for '%s'" % modulepath)
        module = dfunc = None

        # already have the module needed?
        if modulepath in self.modules: 
            the_time = time.mktime(time.localtime())
            time_diff = the_time - time.mktime(self.modules[modulepath][1])
            if time_diff > 100:
                module = reload(self.modules[modulepath][0])
            else:
                module = self.modules[modulepath][0]
        else:
            try: 
                module = __import__(modulepath, globals(), locals(), classname)
            except ImportError, e: 
                logging.error(str(e))

        if module:
            # does the module have the given class?
            if hasattr(module, classname):
                cls = getattr(module, classname)
                # does the class have a dispatch function?
                if hasattr(cls, 'dispatch'):
                    func = getattr(cls, 'dispatch')
                    if callable(func):
                        dfunc = func
                else: 
                    logging.error("no dispatch function in '%s'" % modulepath)
            else: 
                logging.error("no request handler class in '%s'" % modulepath)

        if module and dfunc:
            self.modules[module.__name__] = (module, time.localtime(), dfunc)

        return dfunc

