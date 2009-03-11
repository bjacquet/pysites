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
import logging, urlparse

class ReqHBase(object):
    @classmethod
    def dispatch(cls, req):
        result = -1
        targetf = 'do_%s' % urlparse.urlsplit(req)[2].split('/')[-1]

        try: handler = getattr(cls, targetf)
        except AttributeError:
            logging.error("no '%s' function in '%s'" % (targetf, str(cls)))
        else: # is it a function?
            if callable(handler):
                try: result = handler(req)
                except Exception, e: logging.exception(str(e))
            else:
                logging.error("'%s' not callable in '%s'" % (targetf, str(cls)))
        return(result)
