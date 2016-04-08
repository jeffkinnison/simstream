"""
Utilties for collecting system data.

Author: Jeff Kinnison (jkinniso@nd.edu)
"""

import psutil


class DataReporter(object):
    """Collect and distribute user-specified system data."""

    def __init__(self, interval=1000, **kwargs):
        self.interval = interval
        self.resources = {}
        for key, value in kwargs:
            self.resources[key] = ResourceCollector(key,
                                                    value.callback,
                                                    value.postprocessor,
                                                    value.args)

    def __getitem__(self, name):
        return self.resources[name].data

    def _record_resources(self, resource, value):
        for key, value in self.resources:
            value()
