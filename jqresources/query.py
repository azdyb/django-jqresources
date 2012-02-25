from django.db.models import Q
from django.db.models.query import QuerySet


class JqResourceVersionQuerySet(QuerySet):

    def in_order(self, *args, **kwargs):
        clone = self.select_related("resource")

        if len(args):
            # Can afford searching for index (args won't be a long list)
            return sorted(clone, key=lambda x: args.index(x.resource.slug))
        return list(clone)

    def in_order_list(self, *args, **kwargs):
        clone = self.select_related("resource")

        if len(args):
            # Can afford searching for index (args won't be a long list)
            s = sorted(clone, key=lambda x: args.index(x.resource.slug))
        else:
            s = list(clone)

        field = kwargs.get("field", "path")
        return [getattr(x, field) for x in s]

    def get_by_version(self, resource, version):
        return self.get(resource__slug=resource, version=version)
