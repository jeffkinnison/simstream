"""
Streaming utility for system and simulation data.

author: Jeff Kinnison (jkinniso@nd.edu)
"""

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

    def start_collecting(self):
        for handler in self.handlers:
            handler.run_reporter()


class ReporterHandler(tornado.web.RequestHandler):
    """ """

    def initialize(self, reporter, template):
        self.template = template
        self.reporter = reporter

    def run_reporter(self):
        self.reporter.run()

    def get(self, name, range):
        render(self.template)
