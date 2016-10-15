# wsgi-micro-web-framework
A WSGI-compatible micro web framework. Inspired by, and built using some open-source software written by Anand Chitipothu, 2012. Major changes include a rewrite of the delegation function, support for enforcing HTTPS, and the inclusion of an error logging module.

http://anandology.com/blog/how-to-write-a-web-framework-in-python/

Written confirmation was attained by electronic mail on Mon, 15 Aug 2016 17:22:10 from Anand Chitipothu to use the software under an MIT license.

## Dependencies
[Python Requests: HTTP for Humans](https://github.com/kennethreitz/requests)

## Usage
Where appropriate (usually the web root), create `passenger_wsgi.py`. An example file is below.

```python
from wsgi_micro_web_framework import wsgiapp

# Can be imported from an external file
class index:
    
    # This array holds a routing pattern for the URL to match, in order to delegate to this class.
    # Please note: an "index" class can be viewed from www.domain.com. There is an clause to pass any lack of path, to "index".
    route = ["index"]
    
    # The wsgiapp is passed in as a parameter when the class is initialised. POST/GET data etc. can be extracted from it as normal.
    # The arguments parameter is similar to the "route" array above. However, it contains the full URL path.
    def __init__(self, app, arguments):
        self.app = app
        self.arguments = arguments
    
    def get(self):
        self.app.header("Content-Type", "text/html")
        self.app.content = "<html><head><title>Homepage</title></head><body><h1>Welcome</h1></body></html>"
        self.app.status = "200 OK"

# Likewise, can be imported.
class blog:
    
    # Similarly as above, but with an extra layer, this class is viewed at www.domain.com/blog/view/any_additional_arguments
    route = ["blog", "view"]
    
    def __init__(self, app, arguments):
        self.app = app
        self.arguments = arguments
    
    def get(self):
        self.app.header("Content-Type", "text/plain")
        self.app.content = "Article Number: " + str(self.arguments) # ["blog", "view", "any_additional_arguments"]
        self.app.status = "200 OK"

def log_function(error_message):
    # Do some logging

class application(wsgiapp):

    enforce_https = True
    log = log_function
    
    # Adds the page classes to the delegator.
    routes = [
        index,
        blog,
    ]
    
    def not_found(self):
        self.header("Content-Type", "text/html")
        self.content = "<html><head><title>404 Not Found</title></head><body><h1>Uh oh!</h1><h2>You're lost!</h2></body></html>"
        self.status = "404 Not Found"
	
    def internal_server_error(self):
        self.header("Content-Type", "text/plain")
        self.content = "Internal Server Error. Greg has been notified. If you have the time, please send him an email saying what happened at developer@gregbrimble.com. Thanks!"
        self.status = "500 Internal Server Error"

    def not_implemented(self):
        self.header("Content-Type", "text/plain")
	self.content = "Woah. You used a HTTP request I haven't implemented yet. Give it time. If you need it, send me an email at hello@gregbrimble.com, and I'll see what I can do."
	self.status = "501 Not Implemented"
```
