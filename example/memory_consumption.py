from simstream import Streamer, ReporterHandler, DataReporter
import resource
import tornado.web
import tornado.ioloop
import tornado.template

mem_template = tornado.template.Template("""
<!DOCTYPE html>

<html lang="en">

<head>

    <meta charset="utf-8" />
    <title>RSS Memory Reporting Test</title>

</head>

<body>

    <h1>Maximum Resident Set of the Server</h1>
    <ul>
        {% for point in data %}
            {% block point %}
            <li>{{ escape(point) }}</li>
            {% end %}
        {% end %}
    </ul>

</body>

</html>
""")

def mem_callback():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def mem_postprocessor(rss):
    return rss / 1000

if __name__ == "__main__":
    print("Creating memory consumption reporter...")
    mem_reporter = DataReporter(interval=3)

    print("Adding RSS collector to the reporter...")
    mem_reporter.add_collector("rss",
                               100,
                               mem_callback,
                               postprocessor=mem_postprocessor
                               )
    print("Setting up Streamer instance...")
    mem_streamer = Streamer(handlers=[
        (r"/mem/([a-zA-Z\-0-9\.:,_]+)/[\d]+\-[\d]+$",
            ReporterHandler, dict(reporter=mem_reporter,
                                  template=mem_template))
    ])

    print("Starting data collection...")
    mem_streamer.start_collecting()

    print("Starting server...")
    mem_streamer.listen(8888)
    tornado.ioloop.IOLoop.current().start()
