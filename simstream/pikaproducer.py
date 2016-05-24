"""
Utilties for sending data.

Author: Jeff Kinnison (jkinniso@nd.edu)
"""

import pika


class PikaProducer(object):
    """
    Utility for sending job data.

    Instance Variables:
    name -- the unique name of the producer (one-to-one correspondence with the
            name of a collector or monitor)
    exchange -- the name of the exchange to send to
    queue -- the name of the queue to send to
    routing_key -- the routing key to get to the correct receiver
    """

    def __init__(self, name, rabbitmq_url, exchange, queue, routing_key):
        self.name = name
        self._url = rabbitmq_url
        self._exchange = exchange
        self._queue = queue
        self._routing_key = routing_key

        self._connection = None
        self._channel = None
        self._connected = False
        self._shut_down = False

    def __call__(self, data):
        if self._connection is None:
            self.start()
        if self._connected:
            message = self.pack_data(data)
            self.send_data(message)

    def pack_data(self, data):
        # TODO: Convert data from iterable to string
        pass

    def send_data(self, data):
        # TODO: Send the data over the channel
        pass

    def start(self):
        self._connection = self.connect()

    def shutdown(self):
        self.connection.close()

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
        self._connected = True
