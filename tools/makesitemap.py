#!/usr/bin/env python

import pickle
from urlparse import urljoin

from cement.core import foundation, controller

class MakeSiteMap(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = ''
        arguments = [
            (['--source', '-s'], {
                'action': 'store',
                'help': 'Path to source environment.pickle file',
                'default': 'build/doctrees/environment.pickle',
            }),
            (['--destination', '-d'], {
                'action': 'store',
                'help': 'Path to destination sitemap pickle file',
                'default': 'appengine/sitemap.pkl',
            }),
            (['--base_url', '-b'], {
                'action': 'store',
                'help': 'Base url for sitemap entries',
                'default': '',
            }),
        ]

    def _apply_base_url(self, docs):
        for doc in docs:
            yield urljoin(self.app.pargs.base_url, doc)

    @controller.expose(hide=True)
    def default(self):
        with open(self.app.pargs.source) as env_file:
            env = pickle.load(env_file)
            self.app.log.debug('Source evironment loaded')
        sitemap_urls = list(self._apply_base_url(env.all_docs))
        with open(self.app.pargs.destination, 'w') as map_file:
            pickle.dump(sitemap_urls, map_file)
            self.app.log.debug('destination pickle written')

def run():
    sitemap = foundation.CementApp(
        'makesitemap',
        base_controller=MakeSiteMap
    )
    try:
        sitemap.setup()
        sitemap.run()
    finally:
        sitemap.close()

if __name__ == '__main__':
    run()
