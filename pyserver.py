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
import cgi, logging, string, sys, time, urlparse
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class PyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
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
                func = self.load(module)
                self.wfile.write(func(function, urlsplited[3]))
                return
            else:
                return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % path)
        except ImportError, e:
            self.send_error(404,'File Not Found: %s' % e)

    def do_POST(self):
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

    def load(self, req_path):
        logging.debug("load() called for '%s'" % req_path)
        m = dfunc = None
        mpath = 'modules.%s' % req_path
        try: 
            m = __import__(mpath, globals(), locals(), ['ReqH'])
        except ImportError, e: 
            logging.error(str(e))
            raise ImportError, 'Feature not implemented (yet)'

        if m:
            # got the module, does it have a 'ReqH' class?
            if hasattr(m, 'ReqH'):
                # yes, does the 'ReqH' class have a dispatch function?
                if hasattr(m.ReqH, 'dispatch') and callable(m.ReqH.dispatch):
                    dfunc = m.ReqH.dispatch
                else: 
                    logging.error("no dispatch function in '%s'" % mpath)
            else: 
                logging.error("no request handler class in '%s'" % mpath)
        return dfunc


def main(): 
    sys.path.append('modules')
    logf = logging.Formatter('** %(asctime)s %(levelname)s - %(message)s')
    lcon = logging.StreamHandler()
    lcon.setFormatter(logf)
    logging.getLogger('').addHandler(lcon)
    logging.getLogger('').setLevel(logging.DEBUG)
    logging.info('starting server..')
    try:
        server = HTTPServer(('', 80), PyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
