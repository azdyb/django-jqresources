from django import template

register = template.Library()

from jqresources.models import JqResource, JqResourceVersion


@register.inclusion_tag('jqresources/resource.html')
def resource(resource, version=None):

    if version:
        return {
            "resource_version":
                JqResourceVersion.objects.get_by_version(resource, version)
        }

    return {
        "resource_version":
            JqResource.objects.get(slug=resource).default_version
    }


@register.assignment_tag(takes_context=True)
def get_resource(context, resource_id):
    try:
        return JqResource.objects.get(pk=resource_id)
    except:
        return None
