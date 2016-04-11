import time
from simstream import Streamer, ReporterHandler, DataReporter
import resource
import tornado.web
import tornado.ioloop
import tornado.template


html = """
<!DOCTYPE html>

<html lang="en">

<head>

    <meta charset="utf-8" />
    <title>RSS Memory Reporting Test</title>

</head>

<body>

    <h1>Maximum Resident Set of the Server</h1>
    <div id="chartContainer" style="height: 300px; width: 800px;"></div>

<script src="http://canvasjs.com/assets/script/canvasjs.min.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.2/jquery.min.js"></script>
<script type="text/javascript">

window.onload = function () {
    var dps = []

    var chart;

    var updateInterval = 1000;

    var updateChart = function () {
        $.ajax({
            dataType: "json",
            method: "GET",
            crossDomain: true,
            url: "http://localhost:8888/mem/rss/",
            success: function(data) {
                console.log(data)
                dps = data;
                chart = new CanvasJS.Chart("chartContainer", {
                    theme: "theme2",
                    title:{
            			text: "Server Maximum Memory Usage Over Time"
            		},
                    axisX: {
                        title: "Time"
                    },
                    axisY: {
                        title: "Max RSS Memory Usage (MB)"
                    },
            		animationEnabled: false,
            		data: [{
                        xValueType: "dateTime",
            			type: "line",
            			dataPoints: dps
            		}]
                });
                chart.render();
            },
            error: function(e) {
                console.log(e);
            },
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-Test-Header', 'test-value');
            }
        });

    };

setInterval(function(){updateChart()}, updateInterval);
}
</script>

</body>

</html>
"""


def mem_callback():
    return {'x': time.time() * 1000, 'y': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000000}


def mem_postprocessor(rss):
    return rss / 1000


class ChartHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(html)

if __name__ == "__main__":
    print("Creating memory consumption reporter...")
    mem_reporter = DataReporter(interval=1)

    print("Adding RSS collector to the reporter...")
    mem_reporter.add_collector("rss",
                               mem_callback,
                               100,
                               postprocessor=mem_postprocessor
                               )

    print("Setting up Streamer instance...")
    mem_streamer = Streamer(
        reporters=[mem_reporter],
        handlers=[(r"/mem/([a-zA-Z\-0-9\.:,_]+)/$",
                   ReporterHandler, dict(reporter=mem_reporter)),
                  (r"/viewmem/$", ChartHandler)]
    )

    print("Starting data collection...")
    mem_streamer.start_collecting()

    print("Starting server...")
    mem_streamer.listen(8888)
    tornado.ioloop.IOLoop.current().start()
