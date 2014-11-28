import pkgutil
__version__ = pkgutil.get_data(__package__, 'VERSION').strip()
version_info = tuple(__version__.split('.')[:3])
