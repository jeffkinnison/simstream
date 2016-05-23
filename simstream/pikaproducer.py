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

    def __init__(self, name, exchange, queue, routing_key):
        pass

    def __call__(self, data):
        # TODO: set up producer
        # TODO: pack data
        # TODO: send data
        pass

    def setup_producer(self):
        # TODO: Create connection
        # TODO: Create channel
        # TODO: Bind exchange
        # TODO: Bind queue
        pass

    def pack_data(self, data):
        # TODO: Convert data from iterable to string
        pass

    def send_data(self, data):
        # TODO: Send the data over the channel
        pass

    def shutdown(self):
        # TODO: Close channel
        # TODO: Close connection
