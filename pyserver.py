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
import cgi
import logging
import string
import sys
import time
import urlparse
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import dynmod


class PyServer():
    u"""PyServer class.

    Allows an instance of a PyHandler class to have a persistent Dynmod class 
    instance between requests.

    Contents:
    - `modules`: a Dynmod class instance

"""
    modules = dynmod.Dynmod()


class PyHandler(BaseHTTPRequestHandler, PyServer):    
    u"""PyHandler class, inheritages the BaseHTTOReqyestHandler and PyServer 
    classes.

    For `xhtml` files returns the respective page. The handling of `aspx` files 
    it's a bit of a joke, doesn't do anything. The `html` files are generated 
    when the GET request takes places. The `modules` attribute herited from 
    the PyServer class keeps a cache os previously generated pages.
    
    Contents:
    - `do_Get`: method that handles the GET requests.
    - `do_Post`: method that handles the POST requests.

    """
    def do_GET(self):
        u"""Method to handle the GET requests of `xhtml`, `aspx` and `html` 
    files.

    """
        urlsplited = urlparse.urlsplit(self.path)
        self.path = urlsplited[2]

        try:
            if self.path.endswith(".xhtml"):
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return 
            elif self.path.endswith(".aspx"):   #dynamic 
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("today " + str(time.localtime()[7]))
                self.wfile.write("year " + str(time.localtime()[0]))
                return
            elif self.path.endswith(".html"):
                function = self.path.split('/')[-1]
                module = self.path.replace(function, '')[1:-1].replace('/', '.')
                function = function[:-5]
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                func = self.modules.load(module, 'ReqH')
                self.wfile.write(func(function, urlsplited[3]))
                return
            else:
                return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % path)
        except ImportError, e:
            self.send_error(404,'File Not Found: %s' % e)

    def do_POST(self):
        u"""Method to handle the POST requests.

    It's just a scaffold, doesn't do anything yet.

    """
        global rootnode
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                query=cgi.parse_multipart(self.rfile, pdict)
            self.send_response(301)
            
            self.end_headers()
            upfilecontent = query.get('upfile')
            print "filecontent", upfilecontent[0]
            self.wfile.write("<HTML>POST OK.<BR><BR>");
            self.wfile.write(upfilecontent[0]);
            
        except :
            pass


def main(cwd='.'):
    u"""Execution start point.

    Arguments:
    - `cwd`: the directory where this source file is located

    """
    sys.path.append('%s/modules' % cwd)
    logf = logging.Formatter('** %(asctime)s %(levelname)s - %(message)s')
    lcon = logging.StreamHandler()
    lcon.setFormatter(logf)
    logging.getLogger('').addHandler(lcon)
    logging.getLogger('').setLevel(logging.DEBUG)
    logging.info('starting server..')
    try:
        server = HTTPServer(('', 8080), PyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()


if __name__ == '__main__':
    main()
