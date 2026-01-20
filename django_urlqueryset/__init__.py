from importlib.metadata import version

__all__ = ('UrlQuerySet', 'UrlFileField', 'UrlImageField', 'UrlModel', 'VERSION')

__version__ = version(__name__)

VERSION = __version__.split('.')


def __getattr__(name):
    if name == 'UrlQuerySet':
        from .urlqueryset import UrlQuerySet
        return UrlQuerySet
    if name == 'UrlFileField':
        from .fields import UrlFileField
        return UrlFileField
    if name == 'UrlImageField':
        from .fields import UrlImageField
        return UrlImageField
    if name == 'UrlModel':
        from .models import UrlModel
        return UrlModel
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")