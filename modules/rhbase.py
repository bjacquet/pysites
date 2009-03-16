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
import urlparse


class ReqHBase(object):
    u"""Request Handler Base class.

    Base class to be inherited.

    Contents:
    - `dispatch`: method that returns the execution of the requested function.

"""

    @classmethod
    def dispatch(cls, func, req):
        u"""Returns the execution of the given function with the given request 
arguments.

    Arguments:
    - `cls`: the class where do_`func` is defined.
    - `func`: the function name.
    - `req`: the do_`func` argument.

"""
        result = -1
        logging.info(func)
        logging.info(req)
        targetf = 'do_%s' % func

        try: 
            handler = getattr(cls, targetf)
        except AttributeError:
            logging.error("no '%s' function in '%s'" % (targetf, str(cls)))
        else: # is it a function?
            if callable(handler):
                try: 
                    result = handler(req)
                except Exception, e: 
                    logging.exception(str(e))
            else:
                logging.error("'%s' not callable in '%s'" % (targetf, str(cls)))
        return(result)
