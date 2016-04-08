"""
Utilties for collecting system data.

Author: Jeff Kinnison (jkinniso@nd.edu)
"""


from . import datacollector


class DataReporter(object):
    """Manages data collection at a specified interval"""

    def __init__(self, interval=1000, **kwargs):
        self.interval = interval
        self.resources = {}
        for key, value in kwargs:
            self.resources[key] = datacollector.DataCollector(
                key,
                value.callback,
                value.postprocessor,
                value.args
            )

    def __getitem__(self, name):
        """Return the data from the collector specified by name"""
        return self.resources[name].data

    def _record_resources(self, resource, value):
        """Run all collectors"""
        for key, value in self.resources:
            value()
