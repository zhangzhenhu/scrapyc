import glob
import os
from cStringIO import StringIO
from pkgutil import get_data
from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError

from scrapy.utils.conf import closest_scrapy_cfg

class Config(object):
    """A ConfigParser wrapper to support defaults when calling instance
    methods, and also tied to a single section"""

    SECTION = 'deploy'

    def __init__(self, filename, extra_sources=()):


        self.cp = SafeConfigParser()
        self.cp.read(filename)
        if not self.cp.has_section(self.SECTION):
            self.cp.add_section(self.SECTION)
        self.cp.set(self.SECTION,"source_path",os.path.dirname(filename))


    def _getsources(self):
        sources = ['/etc/scrapyd/scrapyd.conf', r'c:\scrapyd\scrapyd.conf']
        sources += sorted(glob.glob('/etc/scrapyd/conf.d/*'))
        sources += ['scrapyd.conf']
        scrapy_cfg = closest_scrapy_cfg()
        if scrapy_cfg:
            sources.append(scrapy_cfg)
        return sources

    def _getany(self, method, option, default,section=None):
        if not section:
            section = self.SECTION
        try:
            return method(section, option)
        except (NoSectionError, NoOptionError):
            if default is not None:
                return default
            raise

    def get(self, option, default=None,section=None):
        return self._getany(self.cp.get, option, default,section)

    def getint(self, option, default=None,section=None):
        return self._getany(self.cp.getint, option, default)

    def getfloat(self, option, default=None,section=None):
        return self._getany(self.cp.getfloat, option, default,section)

    def getboolean(self, option, default=None,section=None):
        return self._getany(self.cp.getboolean, option, default,section)

    def items(self,  default=None,section=None):
        if not section:
            section =  self.SECTION
        try:
            return self.cp.items(section)
        except (NoSectionError, NoOptionError):
            if default is not None:
                return default
            raise
    def set(self,option,value,section=None):
        if not section:
            section = self.SECTION
        self.cp.set(section, option, value)
