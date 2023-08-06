import logging

from django import template
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

logger = logging.getLogger(__file__)
register = template.Library()


def render_crumb(title, url=None, link=True):
    """Helper function"""
    title = escape(title)
    if url:
        crumb = f'<li class="breadcrumb-item"><a href="{url}">{title}</a></li>'
    else:
        crumb = f'<li class="breadcrumb-item active" aria-current="page">{title}</li>'

    return crumb


@register.simple_tag(takes_context=True)
def breadcrumb(context, title: str, view_name: str = "", path: str = "", **kwargs):
    """Renders a breadcrumb.

    Usage:
        {% breadcrumb "Start" "home" %}
        {% breadcrumb context_var  url_var %}


    :param title str: The title of the breadcrumb. This string is
        translated within the templatetag.
    :param view_name str: The (optional) URL name of the breadcrumb, which is resolved automatically.
    :param path str: The raw path which is used directly as link

    TODO: use the context to match current page -> don't show as link
    """
    # if title is an object, use its __str__:
    title = str(title)

    link = True
    if view_name:
        url = reverse(view_name, kwargs=kwargs)
        # link = url == context["sd"]
    elif path:
        url = path
    else:
        raise AttributeError(
            "Either 'url' or 'path' attribute must be provided in 'breadcrumb' templatetag."
        )

    return mark_safe(render_crumb(_(title), url, link))
