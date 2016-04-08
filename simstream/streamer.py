"""
Streaming utility for system and simulation data.

author: Jeff Kinnison (jkinniso@nd.edu)
"""

from . import datareporter

import tornado.ioloop
import tornado.web


class Streamer(tornado.web.Application):
    """ """

    def __init__(self, handlers=None, default_host='', transforms=None, **settings):
        super(Streamer, self).__init__(handlers, default_host, transforms, **settings)
        self.sysreporter = datareporter.DataReporter()
        self.simreporter = datareporter.DataReporter()


class SimHandler(tornado.web.RequestHandler):
    """ """

    def __init__(self):
