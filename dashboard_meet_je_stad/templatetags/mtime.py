import os.path
import threading
from django import template
from django.conf import settings

register = template.Library()


class UrlCache(object):
    _mtime_sum = {}
    _lock = threading.Lock()

    @classmethod
    def get_mtime(cls, file: str) -> str:
        try:
            return cls._mtime_sum[file]
        except KeyError:
            with cls._lock:
                try:
                    time = round(os.path.getmtime(os.path.join(settings.STATICFILES_DIRS[0], file)))
                    value = '%s%s?v=%s' % (settings.STATIC_URL, file, time)
                except IsADirectoryError:
                    value = settings.STATIC_URL + file
                cls._mtime_sum[file] = value
                return value


@register.simple_tag
def mtime(model_object: str) -> str:
    return UrlCache.get_mtime(model_object)
