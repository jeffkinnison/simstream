import simstream
import resource
import tornado.web
import tornado.ioloop


def mem_callback():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def mem_postprocessor(rss):
    return rss / 1000

if __name__ == "__main__":
    mem_reporter = simstream.DataReporter(3)
    mem_reporter.add_collector("rss",
                               limit=100,
                               callback=mem_callback,
                               postprocessor=mem_postprocessor
                               )

    mem_handler = simstream.ReporterHandler(reporter=mem_reporter,
                                            template="mem_template.html")

    mem_streamer = simstream.Streamer()

    mem_streamer.add_handlers([
        (r"/mem/(.*)", mem_handler)
    ])

    mem_streamer.listen(8888)
    tornado.ioloop.IOLoop.current().start()
