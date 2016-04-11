"""
Streaming utility for system and simulation data.

author: Jeff Kinnison (jkinniso@nd.edu)
"""

import json
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

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    def run_reporter(self):
        print("Running reporter")
        self.reporter.run()

    def get(self, name, range=None):
        #self.reporter.join()
        data = self.reporter[name]
        #self.reporter.start()
        #data = map(lambda x: str(x), data)
        self.write(json.dumps(data))
