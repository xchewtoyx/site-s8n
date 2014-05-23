import json
import logging
import os
import pickle

from google.appengine.api import memcache
import jinja2
import webapp2 as webapp

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.join(
    os.path.dirname(__file__), 'templates'
  )),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)

class SitemapHandler(webapp.RequestHandler):
  def get(self):
    sitemap_data = memcache.get('sitemap')
    if not sitemap_data:
      with open('sitemap.pkl') as urls_file:
        urls = pickle.load(urls_file)
      context = {
        'urls': urls,
      }
      template = JINJA_ENVIRONMENT.get_template('sitemap.xml')
      sitemap_data = template.render(context)
      memcache.add('sitemap', sitemap_data)

    self.response.headers['Content-Type'] = 'text/xml'
    self.response.write(sitemap_data)

class SphinxJsonHandler(webapp.RequestHandler):
  def _redirect_or_abort(self, request_path, document_path):
    if document_path.endswith('.html'):
      if os.path.exists(document_path[:-5]):
        self.redirect(request_path[:-5], permanent=True, abort=True)
    if not request_path.endswith('/'):
      if (os.path.isdir(document_path) or
          os.path.exists(document_path + '.fjson')):
        self.redirect(self.request.path + '/', permanent=True, abort=True)
    self.abort(404)

  def _check_path(self):
    request_path = self.request.path.lstrip('/')
    if not request_path:
      # Need a special case for the '/' url
      request_path = './'
    document_path = os.path.join('json', request_path)
    match = False
    if request_path.endswith('/'):
      document_path = document_path.rstrip('/')
      if os.path.isdir(document_path):
        document_path = os.path.join(document_path, 'index')
      if os.path.exists(document_path + '.fjson'):
        match = True
    if not match:
      self._redirect_or_abort(request_path, document_path)
    return document_path + '.fjson'

  def get(self):
    document_path = self._check_path()
    page_data = memcache.get(self.request.path)
    if not page_data:
      logging.debug('Rendering source file : %r', document_path)
      with open(document_path) as document_data:
        context = json.load(document_data)
      template = JINJA_ENVIRONMENT.get_template('site.html')
      page_data = template.render(context)
      memcache.add(self.request.path, page_data)

    self.response.write(page_data)

app = webapp.WSGIApplication([
  # Render the sitemap
  webapp.Route('/sitemap.xml', SitemapHandler),

  # Attempt to render any unmatched urls
  (r'/.*', SphinxJsonHandler),
], debug=True)
