import simstream
import resource


def mem_callback():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def mem_postprocessor(rss):
    return rss / 1000

mem_reporter = simstream.DataReporter(3)
mem_reporter.add_collector("rss",
                           limit=100,
                           callback=mem_callback,
                           postprocessor=mem_postprocessor
                           )

mem_handler = simstream.ReporterHandler(reporter=mem_reporter,
                                        template="mem_template.html")

mem_streamer = simstream.Streamer()
