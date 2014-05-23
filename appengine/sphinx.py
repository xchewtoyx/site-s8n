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
  def _fixup_parents(self, context):
    # links in the parents list are relative to the canonical location
    # of the served page.  Links served need to be relative to the
    # current url
    page_path = os.path.dirname(context['current_page_name'])
    request_path = os.path.dirname(self.request.path.lstrip('/'))
    parents = context['parents']
    for parent in parents:
      dest_path = os.path.normpath(
        os.path.join(page_path, parent['link']))
      link_path = os.path.relpath(dest_path, start=request_path)
      parent['link'] = link_path

  def _fixup_path(self, request_path):
    # Fixup the request path
    document_path = os.path.join('json', request_path.strip('/'))
    if os.path.isdir(document_path):
      document_path = os.path.join(document_path, "index")
    if document_path.endswith('.html'):
      document_path = document_path.rsplit('.', 1)[0]
    document_path = '.'.join([document_path, 'fjson'])
    return document_path

  def get(self, request_path):
    document_path = self._fixup_path(request_path)
    page_data = memcache.get(self.request.path)
    if not page_data:
      if os.path.exists(document_path):
        logging.debug('Rendering source file : %r', document_path)
        with open(document_path) as document_data:
          context = json.load(document_data)
        self._fixup_parents(context)
        template = JINJA_ENVIRONMENT.get_template('site.html')
        page_data = template.render(context)
        memcache.add(self.request.path, page_data)
      else:
        self.abort(404)

    self.response.write(page_data)

app = webapp.WSGIApplication([
  # Render the sitemap
  webapp.Route('/sitemap.xml', SitemapHandler),

  # Attempt to render any unmatched urls
  (r'/([^.]*)(?:.html|$)', SphinxJsonHandler),
], debug=True)
