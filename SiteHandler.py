# IMPORT STATEMENTS
import webapp2
import jinja2
import urllib2
import logging 
import time
import json
import os
import sys
import re 

from string import letters
from DataStore import *

from google.appengine.api import urlfetch
from google.appengine.api import images
from google.appengine.api import users

# PATH TO TEMPLATES DIRECTORY FOR JINJA2
sys.path.insert(0, 'libs')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'), autoescape = True)

#Setting Universal Logging Level To INFO
logging.getLogger().setLevel(logging.INFO)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

# CLASS PROVIDES BASIC CONVENIENCE FUNCTIONS
class SiteHandler(webapp2.RequestHandler):
    #avoids having to write out self.response.write() every time
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    #calls above two functions to render the template
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))