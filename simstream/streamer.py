"""
Streaming utility for system and simulation data.

author: Jeff Kinnison (jkinniso@nd.edu)
"""

import json
import tornado.web


class Streamer(tornado.web.Application):
    """Server that manages background data collection.

    Inherits from tornado.web.application with no behavior modification.

    Instance variables:
    reporters -- a list of DataReporter objects managed by the Streamer

    Public methods:
    start_collecting -- initiate data collection for all managed reporters
    """

    def __init__(self, reporters, handlers=None, default_host='',
                 transforms=None, **settings):
        """Initialize a new Streamer.

        Arguments:
        reporters -- a list of DataReporters that will run in parallel with
                     the server

        Keyword arguments:
        handlers -- standard tornado.web.Application argument (default None)
        default_host -- standard tornado.web.Application argument (default '')
        transforms -- standard tornado.web.Application argument (default None)
        standard tornado.web.Application argument (default None)
        """
        super(Streamer, self).__init__(
            handlers,
            default_host,
            transforms,
            **settings
        )
        self.reporters = reporters

    def start_collecting(self):
        """Tell all reporters to start collecting data"""
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
