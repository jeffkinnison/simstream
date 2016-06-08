import resource
import time

from simstream import SimStream, DataReporter, DataCollector

settings = {
    "url": "amqp://localhost:5672",
    "exchange": "simstream",
    "queue": "remote_node",
    "routing_key": "stream_sender",
    "exchange_type": "topic"
}


def mem_callback():
    return {'x': time.time() * 1000,
            'y': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


def mem_postprocessor(rss):
    rss.y  = rss.y / 1000000
    return rss

mem_reporter = DataReporter()
mem_reporter.add_collector("rss",
                           mem_callback,
                           settings["url"],
                           settings["exchange"],
                           limit=100,
                           interval=2,
                           postprocessor=mem_postprocessor,
                           )

mem_reporter.start_streaming("rss", "test")

if __name__ == "__main__":
    resource_streamer = SimStream(reporters={"memory": mem_reporter},
                                  config=settings)
    resource_streamer.setup()
    resource_streamer.start()
