""" wsgi_micro_web_framework

A WSGI-compatible micro web framework. Inspired by, and built using some open-source software written by Anand Chitipothu, 2012. Major changes include a rewrite of the delegation function, support for enforcing HTTPS, and the inclusion of an error logging module.

http://anandology.com/blog/how-to-write-a-web-framework-in-python/

Written confirmation was attained by electronic mail on Mon, 15 Aug 2016 17:22:10 from Anand Chitipothu to use the software under an MIT license.

The MIT License (MIT)
Copyright (c) 2012 Anand Chitipothu

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import re, traceback
import requests

__author__ = "Greg Brimble"
__copyright__ = "Copyright (c) 2016 Greg Brimble"
__credits__ = ["Greg Brimble", "Anand Chitipothu"]

__license__ = "MIT License"
__version__ = "1.0"
__maintainer__ = "Greg Brimble"
__email__ = "developer@gregbrimble.com"
__status__ = "Production"

class wsgiapp:
    
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
        self._headers = []
    
    def header(self, name, value):
        self._headers.append((name, value))
    	
    def __iter__(self):
        try:
            self.delegate()
        except:
            self.log(traceback.format_exc())
            self.internal_server_error()
        	
        self.start(self.status, self._headers)
        
        if self.content is None:
            return iter([""])
        
        if isinstance(self.content, str):
            return iter([self.content])
        else:
            return iter(self.content)

    def delegate(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']
        
        if self.enforce_https and (self.environ['wsgi.url_scheme'] != 'https'):
            self.header("Location", "https://" + self.environ['SERVER_NAME'] + self.environ['REQUEST_URI'])
            self.status = "303 See Other"
            self.content = None
            return
        else:
            for namespace in self.routes:
                matches = re.findall("/([^/]*)", path)
                
                if matches[0] == "":
                    matches[0] = "index"
                
                if matches[:len(namespace.route)] == namespace.route:
                    namespace_instance = namespace(self, matches[len(namespace.route):])
                    
                    try:
                        method_function = getattr(namespace_instance, method.lower())
                        method_function()
                        return
                    
                    except:
                        self.not_implemented()
                        return
            
            self.not_found()
