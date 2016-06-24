"""
Utilties for collecting system data.

Author: Jeff Kinnison (jkinniso@nd.edu)
"""

from threading import Thread, Event
import queue

from datacollector import DataCollector
from pikaproducer import PikaProducer


class CollectorExistsException(Exception):
    """Thrown when attempting to add a collector with a conflicting name."""
    pass


class CollectorDoesNotExistException(Exception):
    """Thrown when attempting to access a collector that does not exist."""
    pass


class DataReporter(Thread):
    """Manages collecting specified data.

    Subclass of threading.Thread that modifies Thread.join() and Thread.run()

    Instance variables:
    collectors -- a dict of DataCollectors that are run at interval

    Public methods:
    add_collector -- add a new DataCollector to the list
    run -- start the data collection loop
    join -- end data collection and return control to main thread
    start_collecting -- begin data collection for all collectors
    start_collector -- begin data collection for a specific collector
    stop_collecting -- stop all data collection
    stop_collector -- stop a running DataCollector
    """

    def __init__(self, url, exchange, exchange_type="direct", routing_keys=[], collectors=[], interval=60):
        super(DataReporter, self).__init__()
        self.producer = PikaProducer(url, exchange, exchange_type, routing_keys)
        self.collectors = {}
        self.interval = interval
        self.queue = queue.Queue()
        for collector in collectors:
            self.add_collector(**collector)

    def activate(self):
        self._active = True

    def add_collector(self, name="unknown", callback=lambda x: x, limit=250, interval=10, postprocessor=None,
                      callback_args=[], postprocessor_args=[]):
        """Add a new collector.

        Arguments:
        name -- name of the new DataCollector
        callback -- the data collection callback to run

        Keyword arguments:
        limit -- the number of data points to store (default 100)
        postprocessor -- a postprocessing function to run on each data point
                         (default None)
        callback_args -- a list of arguments to pass to the callback
                         (default [])
        postprocessor_args -- a list of arguments to pass to the postprocessor
                              (default [])

        Raises:
        CollectorExistsException if a collector named name already exists
        """
        if name in self.collectors:
            raise CollectorExistsException

        self.collectors[name] = DataCollector(
            name=name,
            callback=callback,
            limit=limit,
            interval=interval,
            postprocessor=postprocessor,
            callback_args=callback_args,
            postprocessor_args=postprocessor_args
        )

    def deactivate(self):
        self._active = False

    def get_data(self):
        while True:
            try:
                data = self.queue.get(block=False)
                yield data
            except queue.Empty:
                break
        return

    def run(self):
        for collector in self.collectors:
            if self.collectors[collector].queue is not self.queue:
                self.collectors[collector].set_queue(self.queue)
        self.start_collecting()
        self._collection_event = Event()
        self._active = True
        while self._active and not self._collection_event.wait(timeout=self.interval):
            data = {}
            for item in self.get_data():
                for key in item:
                    if key in data:
                        try:
                            data[key].extend(item[key])
                        except TypeError as e:
                            data[key].append(item[key])
                    else:
                        data[key] = [item[key]]
            self.send_data(data)
            print(data)

    def send_data(self, data):
        self.producer.send_data(data)

    def start_collecting(self):
        """
        Start data collection for all associated collectors.
        """
        for collector in self.collectors:
            self.start_collector(collector)

    def start_collector(self, name):
        """
        Activate the specified collector.

        Arguments:
        name -- the name of the collector to start

        Raises:
        RuntimeError if the collector has already been started.
        """
        try:
            self.collectors[name].activate()
            self.collectors[name].start()
        except RuntimeError as e:
            print("Error starting collector ", name)
            print(e)

    def stop(self):
        self.deactivate()
        self.stop_collecting()
        self.producer.shutdown()

    def stop_collecting(self):
        """
        Stop all collectors.
        """
        for collector in self.collectors:
            self.stop_collector(collector)

    def stop_collector(self, name):
        """Deactivate the specified collector.

        Arguments:
        name -- the name of the collector to stop

        Raises:
        CollectorDoesNotExistException if no collector named name exists
        """
        if name not in self.collectors:
            raise CollectorDoesNotExistException

        try:
            self.collectors[name].stop()
            self.collectors[name].join()
        except RuntimeError as e: # Catch deadlock
            print(e)


    def start_streaming(self, routing_key):
        """
        Begin streaming data to a particular recipient.

        Arguments:
        routing_key -- the routing key to reach the intended recipient
        """
        self.producer.add_routing_key(routing_key)

    def stop_streaming(self, routing_key):
        """
        Stop a particular stream.

        Arguments:
        collector_name -- the collector associated with the producer to stop
        routing_key -- the routing key to reach the intended recipient

        Raises:
        ProducerDoesNotExistException if no producer named name exists
        ValueError if the producer is removed by another call to this method
                   after the for loop begins
        """
        self.producer.remove_routing_key(routing_key)

if __name__ == "__main__":
    import resource
    import sys
    import time

    q = queue.Queue()

    def get_mem():
        data = {"x": time.time(), "y": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
        return data

    def get_page_faults():
        data = {"x": time.time(), "y": resource.getrusage(resource.RUSAGE_SELF).ru_minflt}
        return data

    collectors = [
        {
            "name": "rss",
            "callback": get_mem,
            "interval": 2
        },
        {
            "name": "flt",
            "callback": get_page_faults,
            "interval": 3
        }
    ]

    reporter = DataReporter("amqp://guest:guest@localhost:5672",
                            "test",
                            routing_keys=['#'],
                            collectors=collectors,
                            interval=1)

    reporter.start()

    time.sleep(15)

    reporter.stop()
    reporter.join()
