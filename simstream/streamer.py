"""
Streaming utility for system and simulation data.

author: Jeff Kinnison (jkinniso@nd.edu)
"""

import json
import tornado.web


class Streamer(tornado.web.Application):
    """Server that manages background data collection.

    Inherits from tornado.web.application without modifying behavior.

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
    """Handles retrieving and distributing data from reporters.

    Inherits from tornado.web.RequestHandler without modifying underlying
    behavior.

    Instance variables:
    reporter -- the DataReporter instance from which to retrieve data on get()
    template -- the Tornado template to render on get()
    """

    def initialize(self, reporter=None, template=None):
        """Called internally by tornado to init a custom WebHandler."""
        self.template = template
        self.reporter = reporter

    def set_default_headers(self):
        """Called internally by tornado to modify HTTP response headers."""
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    def get(self, name, range=None):
        """Distribute all data from reporter."""
        data = self.reporter[name]
        self.write(json.dumps(data))
