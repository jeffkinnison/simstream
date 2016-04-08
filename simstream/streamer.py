"""
Streaming utility for system and simulation data.

author: Jeff Kinnison (jkinniso@nd.edu)
"""

from . import datareporter

import tornado.ioloop
import tornado.web


class Streamer(tornado.web.Application):
    """ """

    def __init__(self, handlers=None, default_host='',
                 transforms=None, **settings):
        super(Streamer, self).__init__(
            handlers,
            default_host,
            transforms,
            **settings
        )


class ReporterHandler(tornado.web.RequestHandler):
    """ """

    def initialize(self, reporters, template):
        self.template = template
        self.reporters = {}
        for reporter in reporters:
            self.reporters[reporter.name] = reporter

    def get(self, name, range):
        render(self.template)
