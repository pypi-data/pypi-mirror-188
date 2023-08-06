from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from medux.common.api.interfaces import IMenuItem


def is_superuser(request):
    return request.user.is_superuser


def is_staff(request):
    return request.user.is_staff


def is_authenticated(request):
    return request.user.is_authenticated


def is_employee(request):
    return request.user.is_employee


class Admin(IMenuItem):
    menu = "user"
    title = _("Admin")
    url = reverse_lazy("admin:index")
    weight = 80
    icon = "gear"
    separator = True
    check = is_staff


class Logout(IMenuItem):
    menu = "user"
    title = _("Logout")
    url = reverse_lazy("logout")
    weight = 90
    separator = True
    icon = "box-arrow-right"
    check = is_authenticated
