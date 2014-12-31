import sys
try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading


class BaseData(_threading.Thread):
    """docstring for BaseData"""
    def __init__(self, arg):
        super(BaseData, self).__init__()
        self.arg = arg

    def run(self):
        pass
        