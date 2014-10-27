from django import template


register = template.Library()


@register.simple_tag
def verbose_name(instance, field_name):
    """Returns the verbose name of a model field

    :param instance: model class instance
    :param field_name: string model field name
    :returns: string verbose name of the field name
    """
    return instance._meta.get_field(field_name).verbose_name
