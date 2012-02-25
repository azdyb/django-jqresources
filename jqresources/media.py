from django.db.models import Q
from django.forms.widgets import MEDIA_TYPES

from models import JqResourceVersion


class jq(object):

    """Takes resource and version and returns path
    of matching JqResourceVersion.
    """

    resource = None
    version = None

    def __init__(self, resource, version=None):
        self.resource = resource
        self.version = version

    def get_path(self):
        try:
            return JqResourceVersion.objects.get(self._get_q()).path
        except:
            return ""

    def _get_q(self):
        if self.version:
            return Q(resource__slug=self.resource, version=self.version)
        else:
            return Q(resource__slug=self.resource, default_for__isnull=False)


def decode_list(l):
    ll = []
    for it in l:
        if isinstance(it, jq):
            ll.append(it.get_path())
        else:
            ll.append(it)
    return ll


def decode_dict(d):
    dd = {}
    for k, v in d.items():
        if isinstance(v, list) or isinstance(v, tuple):
            dd[k] = decode_list(v)
        elif isinstance(v, jq):
            dd[k] = v.get_path()
        else:
            dd[k] = v
    return dd


# TODO: Should take all occurrences of jq
#       and retrieve them in one database query
class JqResourceDefiningClass(type):

    """Iterates over css and js attributes and replaces all
    occurences of jq with their path values
    """

    def __new__(cls, name, bases, attrs):
        new_attrs = {}
        for m in MEDIA_TYPES:
            medium = attrs.get(m, None)
            if medium is None:
                continue
            if isinstance(medium, list) or isinstance(medium, tuple):
                medium = decode_list(medium)
            elif isinstance(medium, dict):
                medium = decode_dict(medium)
            new_attrs[m] = medium
        attrs.update(new_attrs)

        new_class = super(JqResourceDefiningClass, cls).__new__(
            cls, name, bases, attrs)
        return new_class


class JqResourceMedia:
        __metaclass__ = JqResourceDefiningClass
