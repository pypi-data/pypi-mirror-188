from django import template
from django.db.models import Model

register = template.Library()


@register.filter
def class_name(model: Model):
    """:returns the singular verbose name of the given object's class.

    This can be used in templates:

    .. code-block:: django

        <div>Should this {{ object|class_name }} really be deleted?</div>
    """
    return model._meta.verbose_name


@register.filter
def class_name_plural(model: Model):
    """:returns the plural verbose name of the given object's class.

    This can be used in templates:

    .. code-block:: django

        <div>Should this {{ object|class_name_plural }} really be deleted?</div>
    """
    return model._meta.verbose_name_plural
