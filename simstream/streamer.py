"""
Streaming utility for system and simulation data.

author: Jeff Kinnison (jkinniso@nd.edu)
"""

import tornado.web


class Streamer(tornado.web.Application):
    """ """

    def __init__(self, reporters, handlers=None, default_host='',
                 transforms=None, **settings):
        super(Streamer, self).__init__(
            handlers,
            default_host,
            transforms,
            **settings
        )
        self.reporters = reporters

    def start_collecting(self):
        for reporter in self.reporters:
            reporter.start()


class ReporterHandler(tornado.web.RequestHandler):
    """ """

    def initialize(self, reporter=None, template=None):
        self.template = template
        self.reporter = reporter

    def run_reporter(self):
        print("Running reporter")
        self.reporter.run()

    def get(self, name, range=None):
        data = map(lambda x: str(x), self.reporter[name])
        self.finish(self.template.generate(data=data))
