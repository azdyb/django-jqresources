from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import patterns, include, url

from jqresources.models import JqResourceVersion, JqResource


class IsDefaultListFilter(admin.SimpleListFilter):
    title = _("default")
    parameter_name = "is_default"

    def lookups(self, request, model_admin):
        return (
            ("1", _("Default versions")),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(default_for__isnull=False)
        return queryset


class JqResourceVersionAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "resource", "version", "is_default", "path"]
    list_filter = ["resource", IsDefaultListFilter]

    def get_fieldsets(self, request, obj=None):
        full_edit = ((obj is None) and (not "resource" in request.GET))
        if full_edit:
            return super(JqResourceVersionAdmin, self).get_fieldsets(request,
                                                                     obj)
        return (
            (None, {
                "fields": ("version", "path")
            }),
            ("Hidden", {
                "fields": ("resource", ),
                "classes": ("hidden-fields", )
            })
        )

    class Media:
        css = {
            "all": ["jqresources/admin.css"]
        }


class JqResourceVersionInline(admin.TabularInline):
    model = JqResourceVersion
    readonly_fields = ["Default"]
    fields = ["Default", "version", "path"]
    can_delete = True
    max_num = 0
    extra = 0
    verbose_name = _("Version")
    verbose_name_plural = _("Versions")

    def Default(self, obj=None):
        if obj.pk is None:
            return ""
        is_default = ""
        if obj.is_default():
            is_default = " checked"
        return "<input%(checked)s type=\"radio\" class=\"radiolist\" " \
        "id=\"id_default_version_%(pk)d\" value=\"%(pk)d\" " \
        "name=\"default_version\" >" % {
            "pk": obj.pk,
            "checked": is_default
        }
    Default.allow_tags = True


class JqResourceAdminForm(forms.ModelForm):
    have_default_version = forms.BooleanField(label=_("Have default version"),
                                              initial=False, required=False)

    class Meta:
        model = JqResource

    def __init__(self, *args, **kwargs):
        super(JqResourceAdminForm, self).__init__(*args, **kwargs)
        self.fields["default_version"].queryset = \
            JqResourceVersion.objects.filter(resource=self.instance.pk)
        self.fields["have_default_version"].initial = \
            self.instance.default_version is not None

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data["have_default_version"] == False:
            cleaned_data["default_version"] = None
        return cleaned_data


class JqResourceAdmin(admin.ModelAdmin):
    form = JqResourceAdminForm
    list_display = ["name", "slug", "type", "default_Version",
                    "versions_count"]
    list_filter = ["type"]
    inlines = [JqResourceVersionInline, ]
    radio_fields = {"default_version": admin.VERTICAL}

    def get_fieldsets(self, request, obj=None):
        if (obj is None) or (obj.versions.count() == 0):
            return (
                (_("Resource"), {
                    "fields": ("name", "slug", "type")
                }),
                ("Hidden", {
                    "fields": ("default_version", )
                })
            )
        else:
            return (
                    (_("Resource"), {
                        "fields": ("name", "slug", "type",
                                   "have_default_version")
                    }),
                    ("Hidden", {
                        "fields": ("default_version", )
                    })
                )

    def get_formsets(self, request, obj=None):
        if (obj is None) or (obj.versions.count() == 0):
            return []
        else:
            return super(JqResourceAdmin, self).get_formsets(request, obj)

    class Media:
        js = ["jqresources/admin.js"]
        css = {
            "all": ["jqresources/admin.css"]
        }

    def default_Version(self, obj):
        ver = obj.default_version
        if ver:
            html = "<a href=\"../jqresourceversion/%(pk)d\" >" \
                   "%(version)s</a>" % {
                "pk": ver.pk,
                "version": ver.version
            }
            return html
        else:
            return None
    default_Version.allow_tags = True

    def versions_count(self, obj):
        html = "<a href=\"../jqresourceversion/?resource__id__exact=" \
        "%(pk)d\">%(versions_count)d</a>" % {
            "pk": obj.pk,
            "versions_count": obj.versions.count()
        }
        return html
    versions_count.allow_tags = True
