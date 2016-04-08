"""
Utilties for collecting system data.

Author: Jeff Kinnison (jkinniso@nd.edu)
"""

import psutil


class SystemReporter(object):
    """Collect and distribute user-specified system data."""

    def __init__(self, **kwargs):
        self.resources = {}

        for key, value in kwargs:
            if key == "cpu" and value:


    def resource_values(self, *args):
        pass

    def _read_resources(self):
        pass

    def _record_resource(self, resource, value):
        pass


class ResourceCollector(object):
    def __init__(self, name, callback, postprocessor=None, *args):
        self.name = name if name else "Unknown Resource"
        self.callback = callback
        self.callback_args = args
        self.postprocessor = postprocessor
        self.data = []

    def __call__(self):
        try:
            result = callback(*self.callback_args)
            self.data.append(self.postprocessor(result) if self.postprocessor else result)
        except Exception as e:
            print("Error: ", e)
