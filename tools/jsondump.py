#!/usr/bin/env python

import json

from cement.core import foundation, controller

class JsonDump(controller.CementBaseController):
    class Meta:
        label = 'base'
        arguments = [
            (['file'], {
                'action': 'store',
                'help': 'Path to json file to dump',
            }),
            (['key'], {
                'action': 'store',
                'nargs': '?',
                'help': ('Dump specific key.  If omitted the list of '
                         'keys will be returned.'),
            }),
        ]

    @controller.expose(hide=True)
    def default(self):
        with open(self.app.pargs.file) as source_file:
            data = json.load(source_file)
        if self.app.pargs.key:
            print data[self.app.pargs.key]
        else:
            print '\n'.join(data.keys())

def run():
    app = foundation.CementApp(
        'jsondump',
        base_controller=JsonDump
    )
    try:
        app.setup()
        app.run()
    finally:
        app.close()

if __name__ == '__main__':
    run()
