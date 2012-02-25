from django.db import models
from django.utils.translation import ugettext_lazy as _

from jqresources.manager import JqResourceVersionManager


JQRESOURCE_TYPE = (
    ("js", _("Javascript")),
    ("css", _("Stylesheet")),
    ("other", _("Other"))
)


class JqResource(models.Model):
    slug = models.SlugField(verbose_name=_("Slug"), max_length=20, unique=True)
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    type = models.CharField(
        max_length=5, choices=JQRESOURCE_TYPE, default="other")
    default_version = models.OneToOneField(
        "JqResourceVersion", related_name="default_for",
        on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _("JqResource")
        verbose_name_plural = _("JqResources")

    def __unicode__(self):
        return self.name


class JqResourceVersion(models.Model):
    resource = models.ForeignKey(JqResource, verbose_name=_("Resource"),
                                 related_name="versions")
    version = models.CharField(max_length=50, verbose_name=_("Version"))
    path = models.CharField(max_length=100, verbose_name=_("Path"),
        help_text=_(
            "A local filesystem path that will be "
            "appended to your STATIC_ROOT setting "
            "to determine the value of the url attribute."))

    objects = JqResourceVersionManager()

    class Meta:
        verbose_name = _("JqResource Version")
        verbose_name_plural = _("JqResource Versions")

    def __unicode__(self):
        return "%(resource)s (%(version)s)" % {
            "resource": self.resource,
            "version": self.version
        }

    def is_default(self):
        try:
            self.default_for
            return True
        except JqResource.DoesNotExist:
            return False
    is_default.boolean = True
