from django.db import models

from jqresources.query import JqResourceVersionQuerySet


class JqResourceVersionManager(models.Manager):

    def get_query_set(self):
        return JqResourceVersionQuerySet(self.model, using=self._db)

    def in_order(self, *args, **kwargs):
        return self.get_query_set().in_order(*args, **kwargs)

    def in_order_list(self, *args, **kwargs):
        return self.get_query_set().in_order_list(*args, **kwargs)

    def get_by_version(self, resource, version):
        return self.get_query_set().get_by_version(resource, version)
