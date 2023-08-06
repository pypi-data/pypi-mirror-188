from django.conf import settings

from medux.common.menu import Menu
from ..core import __version__


def globals(request):
    return {
        "globals": {
            "project_title": settings.PROJECT_TITLE,
            "version": __version__,
        },
        "menus": Menu(request),
    }
