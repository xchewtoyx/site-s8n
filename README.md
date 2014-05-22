Sphinx2Appserver
================

This repo has a basic skeleton that can be used to deploy a sphinx site to
appengine.


Makefile helpers
----------------

To rebuild the pages:

    make json

or to force rebuild of all files:

    make json-all

To test with the appengine dev server:

    make appserver

And to push up to appserver:

    make deploy
