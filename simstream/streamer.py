"""
Streaming utility for system and simulation data.

author: Jeff Kinnison (jkinniso@nd.edu)
"""

import json
import pika

class Streamer(object):
    """
    The primary entry point for routing incoming messages to the proper handler.
    """

    def __init__(self, rabbitmq_url, exchange_name, queue_name,
                 exchange_type=direct, routing_keys=["#"]):
        """
        Create a new instance of Streamer.

        Arguments:
        rabbitmq_url -- URL to RabbitMQ server
        exchange_name -- name of RabbitMQ exchange to join
        queue_name -- name of RabbitMQ queue to join
        """
        self._connection = None
        self._channel = None
        self._closing = None
        self._consumer_tag = None
        self._url = rabbitmq_url

        # The following are necessary to guarantee that both the RabbitMQ
        # server and Streamer know where to look for messages. These names will
        # be decided before dispatch and should be recorded in a config file or
        # else on a per-job basis.
        self._exchange = exchange_name
        self._exchange_type = exchange_type
        self._queue = queue_name
        self._routing_keys = routing_keys

    def connect(self):
        """
        Create an asynchronous connection to the RabbitMQ server at URL.
        """
        return pika.SelectConnection(pika.URLParameters(self._url).
                                     on_open_callback=self.on_connection_open,
                                     on_close_callback=self.on_conection_close,
                                     stop_ioloop_on_close=False)

    def on_connection_open(self, unused_connection):
        """
        Actions to perform when the connection opens. This may not happen
        immediately, so defer action to this callback.

        Arguments:
        unused_connection -- the created connection (by this point already
                             available as self._connection)
        """
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_connection_close(self, connection, code, text):
        """
        Actions to perform when the connection is unexpectedly closed by the
        RabbitMQ server.

        Arguments:
        connection -- the connection that was closed (same as self._connection)
        code -- response code from the RabbitMQ server
        text -- response body from the RabbitMQ server
        """
        pass

    def start(self):
        """
        Start a connection with the RabbitMQ server.
        """
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        """
        Stop an active connection with the RabbitMQ server.
        """
        self._connection.ioloop.stop()


#import tornado.web


# class Streamer(tornado.web.Application):
#     """Server that manages background data collection.
#
#     Inherits from tornado.web.application without modifying behavior.
#
#     Instance variables:
#     reporters -- a list of DataReporter objects managed by the Streamer
#
#     Public methods:
#     start_collecting -- initiate data collection for all managed reporters
#     """
#
#     def __init__(self, reporters, handlers=None, default_host='',
#                  transforms=None, **settings):
#         """Initialize a new Streamer.
#
#         Arguments:
#         reporters -- a list of DataReporters that will run in parallel with
#                      the server
#
#         Keyword arguments:
#         handlers -- standard tornado.web.Application argument (default None)
#         default_host -- standard tornado.web.Application argument (default '')
#         transforms -- standard tornado.web.Application argument (default None)
#         standard tornado.web.Application argument (default None)
#         """
#         super(Streamer, self).__init__(
#             handlers,
#             default_host,
#             transforms,
#             **settings
#         )
#         self.reporters = reporters
#
#     def start_collecting(self):
#         """Tell all reporters to start collecting data"""
#         for reporter in self.reporters:
#             reporter.start()
#
#
# class ReporterHandler(tornado.web.RequestHandler):
#     """Handles retrieving and distributing data from reporters.
#
#     Inherits from tornado.web.RequestHandler without modifying underlying
#     behavior.
#
#     Instance variables:
#     reporter -- the DataReporter instance from which to retrieve data on get()
#     template -- the Tornado template to render on get()
#     """
#
#     def initialize(self, reporter=None, template=None):
#         """Called internally by tornado to init a custom WebHandler."""
#         self.template = template
#         self.reporter = reporter
#
#     def set_default_headers(self):
#         """Called internally by tornado to modify HTTP response headers."""
#         self.set_header("Access-Control-Allow-Origin", "*")
#         self.set_header("Access-Control-Allow-Headers", "*")
#         self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
#
#     def get(self, name, range=None):
#         """Distribute all data from reporter."""
#         data = self.reporter[name]
#         self.write(json.dumps(data))
