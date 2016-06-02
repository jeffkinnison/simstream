"""
Streaming utility for system and simulation data.

author: Jeff Kinnison (jkinniso@nd.edu)
"""

import json
import pika

class PikaAsyncConsumer(object):
    """
    The primary entry point for routing incoming messages to the proper handler.
    """

    def __init__(self, rabbitmq_url, exchange_name, queue_name, route_message,
                 exchange_type=direct, routing_keys=["#"]):
        """
        Create a new instance of Streamer.

        Arguments:
        rabbitmq_url -- URL to RabbitMQ server
        exchange_name -- name of RabbitMQ exchange to join
        queue_name -- name of RabbitMQ queue to join

        Keyword Arguments:
        exchange_type -- one of 'direct', 'topic', 'fanout', 'headers'
                         (default 'direct')
        routing_keys -- the routing key that this consumer listens for
                        (default '#', receives all messages)
        """
        self._connection = None
        self._channel = None
        self._shut_down = False
        self._consumer_tag = None
        self._url = rabbitmq_url
        self._route_message = route_message

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
        self._connection.channel(on_open_callback=self.on_channel_open,
                                 on_close_callback=self.on_channel_close)

    def on_connection_close(self, connection, code, text):
        """
        Actions to perform when the connection is unexpectedly closed by the
        RabbitMQ server.

        Arguments:
        connection -- the connection that was closed (same as self._connection)
        code -- response code from the RabbitMQ server
        text -- response body from the RabbitMQ server
        """
        self._channel = None
        if self._shut_down:
            self._connection.ioloop.stop()
        else:
            self._connection.add_timeout(5, self.reconnect)

    def on_channel_open(self, channel):
        """
        Store the opened channel for future use and set up the exchange and
        queue to be used.

        Arguments:
        channel -- the Channel instance opened by the Channel.Open RPC
        """
        self._channel = channel
        self.declare_exchange()


    def on_channel_close(self, channel, code, text):
        """
        Actions to perform when the channel is unexpectedly closed by the
        RabbitMQ server.

        Arguments:
        connection -- the connection that was closed (same as self._connection)
        code -- response code from the RabbitMQ server
        text -- response body from the RabbitMQ server
        """
        self._connection_close()

    def declare_exchange(self):
        """
        Set up the exchange that will route messages to this consumer. Each
        RabbitMQ exchange is uniquely identified by its name, so it does not
        matter if the exchange has already been declared.
        """
        self._channel._exchange_declare(self.declare_exchange_success,
                                        self._exchange,
                                        self._exchange_type)

    def declare_exchange_success(self):
        """
        Actions to perform on successful exchange declaration.
        """
        self.declare_queue()

    def declare_queue(self):
        """
        Set up the queue that will route messages to this consumer. Each
        RabbitMQ queue can be defined with routing keys to use only one
        queue for multiple jobs.
        """
        self._channel.queue_declare(self.declare_queue_success,
                                    self._queue)

    def declare_queue_success(self):
        """
        Actions to perform on successful queue declaration.
        """
        self._channel.queue_bind(self.munch,
                                 self._queue,
                                 self._exchange,
                                 self._routing_key
                                )

    def munch(self):
        """
        Begin consuming messages from the Airavata API server.
        """
        self._channel.basic_consume(self._process_message)

    def _process_message(self, ch, method, properties, body):
        """
        Receive and verify a message, then pass it to the router.

        Arguments:
        ch -- the channel that routed the message
        method -- delivery information
        properties -- message properties
        body -- the message
        """
        self._route_message(body)
        self.basic_ack()

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
