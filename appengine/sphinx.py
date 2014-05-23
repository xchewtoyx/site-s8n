import json
import logging
import os
import pickle

from google.appengine.api import memcache
from google.appengine.ext.webapp.util import run_wsgi_app
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
  def _fixup_parents(self, context):
    # the parents list is a mess.  The list gives relative urls, with
    # no file extension and has a habit of stripping 'index' for index
    # pages even though it is inluded in the 'current_page_name' of
    # the relevant page.  Ugh.
    parents = context['parents']
    if context['current_page_name'].endswith('/index'):
      current_path = context['current_page_name'][:-6]
    else:
      current_path = context['current_page_name']
    for index in range(len(parents)):
      parent = parents[index]['link']
      # Work out the relative path difference
      link_path = os.path.join('/', current_path, parent)
      link_path = os.path.relpath(link_path)
      # if the relative link ends with a /, destination is index
      if parent.endswith('/'):
        link_path = os.path.join(link_path, index)
      parents[index]['link'] = link_path

  def get(self, document_path):
    # Fixup the request path
    document_path = os.path.join('json', document_path.strip('/'))
    if os.path.isdir(document_path):
      document_path = os.path.join(document_path, "index.html")
    if document_path.endswith('.html'):
      document_path = document_path.rsplit('.', 1)[0]
    document_path = '.'.join([document_path, 'fjson'])

    page_data = memcache.get('document_path')
    if not page_data:
      if os.path.exists(document_path):
        logging.debug('Rendering source file : %r', document_path)
        with open(document_path) as document_data:
          context = json.load(document_data)
        self._fixup_parents(context)
        template = JINJA_ENVIRONMENT.get_template('site.html')
        page_data = template.render(context)
      else:
        self.abort(404)

    self.response.write(page_data)

app = webapp.WSGIApplication([
  # Render the sitemap
  webapp.Route('/sitemap.xml', SitemapHandler),

  # Attempt to render any unmatched urls
  (r'/([^.]*)(?:.html|$)', SphinxJsonHandler),
], debug=True)
