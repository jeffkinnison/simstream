import resource
import time

from simstream import Simstream, DataReporter, DataCollector


def mem_callback():
    return {'x': time.time() * 1000,
            'y': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}

def mem_postprocessor(rss):
    rss.y  = rss.y / 1000000
    return rss

mem_reporter = DataReporter(interval=1)
mem_reporter.add_collector("rss",
                           mem_callback,
                           100,
                           postprocessor=mem_postprocessor)

resource_streamer = SimStream()
resource_streamer.start()
