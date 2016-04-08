"""
Utilties for collecting system data.

Author: Jeff Kinnison (jkinniso@nd.edu)
"""


class DataCollector(object):
    def __init__(self, name, limit=250, callback, postprocessor=None, *args):
        self.name = name if name else "Unknown Resource"
        self._callback = callback
        self._callback_args = args
        self._postprocessor = postprocessor
        self._data = []

    def __call__(self):
        try:
            result = callback(*self.callback_args)
            self.data.append(
                self.postprocessor(result) if self.postprocessor else result
            )
        except Exception as e:
            print("Error: ", e)

    @property
    def data(self, start=0, end=-1):
        return self._data[start:end]
