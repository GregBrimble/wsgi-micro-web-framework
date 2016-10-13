# wsgi-micro-web-framework
A WSGI-compatible micro web framework. Inspired by, and built using some open-source software written by Anand Chitipothu, 2012. Major changes include a rewrite of the delegation function, support for enforcing HTTPS, and the inclusion of an error logging module.

http://anandology.com/blog/how-to-write-a-web-framework-in-python/

Written confirmation was attained by electronic mail on Mon, 15 Aug 2016 17:22:10 from Anand Chitipothu to use the software under an MIT license.

## To Do
Handle pages more elegantly. I want to be able to import from all pages from a module, and automatically delegate to the relevant functions, where each function handles the HTTP request method.

## Dependencies
[requests](https://github.com/kennethreitz/requests)

## Usage
Where appropriate (usually the web root), create `passenger_wsgi.py`. An example file is below.

```python
from webframework import wsgiapp

def log_function(error_message):
  # Do some logging

def index(self, app, method):
  app.header("Content-Type", "text/html")
  app.content = "<html><head><title>Hello, world!</title></head><body><h1>Hello, world!</h1></body></html>"
  app.status = "200 OK"

class application(wsgiapp):

  enforce_https = True
  urls = {}
  urls["/"] = "index"
  log = log_function
	
  index = index
	
  def not_found(self):
    self.header("Content-Type", "text/plain")
    self.content = "<html><head><title>404 Not Found</title></head><body><h1>Uh oh!</h1><h2>You're lost!</h2></body></html>"
    self.status = "404 Not Found"
		
  def internal_server_error(self):
    self.header("Content-Type", "text/plain")
    self.content = "Internal Server Error. Greg has been notified. If you have the time, please send him an email saying what happened at developer@gregbrimble.com. Thanks!"
    self.status = "500 Internal Server Error"
```
