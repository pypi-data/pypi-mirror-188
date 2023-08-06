import re
from logging import getLogger
from typing import List, Dict, Iterable

from crispy_forms.helper import FormHelper
from django.apps import AppConfig
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import path, URLPattern
from django.utils.functional import cached_property
from django.utils.text import slugify
from gdaps.api import Interface, InterfaceRegistry
from gdaps.api.interfaces import IFormExtensionMixin, IViewExtensionMixin

from medux.common.api.http import HttpResponseEmpty
from medux.common.htmx.mixins import HtmxResponseMixin

logger = getLogger(__file__)


class MeduxPluginAppConfig(AppConfig):
    """Common base class for all MedUX AppConfigs.

    All MedUX apps' AppConfigs must inherit from this class (or must at least implement this interface).
    """

    from django.db import models

    # A dict that defines groups and their permissions this Plugin sets.
    #   You can call :class:`medux.common.tools.create_groups_permissions()`
    #   when the application is initialized.
    #   Example:
    #   groups_permissions = {
    #       'Group name': {
    #           SomeModel_or_dotted_model_path: ['add', 'change', 'delete', 'view'],
    #           ...
    #       }
    #   }
    #   Note: the "Group name" is translatable, just set the English name here.
    #   You can use a model class or a dotted model path like "auth.user"
    groups_permissions: Dict[str, Dict[models.Model, List[str]]] = {}

    def initialize(self):
        """Initializes the application at setup time.

        This method is called from the "initialize" management command.
        It should set up basic data in the database etc., and needs to be idempotent.
        """

    @cached_property
    def compatibility_errors(self) -> List[str]:
        """checks for compatibility issues that can't be ignored for correct application function,
         and returns a list of errors.

        :returns a list of error strs"""

        return []

    @cached_property
    def compatibility_warnings(self) -> List[str]:
        """Checks for compatibility issues that can be accepted for continuing.

        :return: a list of warnings"""

        return []


NON_CALLABLE_ATTRIBUTES = [
    "weight",
    "separator",
    "required_permissions",
    "view_name",
    "exact_url",
]
INTERNAL_ATTRIBUTES = [
    "menu",
    "url",
    "slug",
    "title",
    "weight",
    "icon",
    "separator",
    "required_permissions",
    "view_name",
    "badge",
    "disabled",
    "exact_url",
    "check",
    "visible",
    "collapsed",
]


@Interface
class IMenuItem:
    """An extendable and versatile MenuItem Interface

    You can use that for creating menu items in a named menu:
    .. code-block: python

        class AddUserAction(IMenuItem)
            menu = "page_actions"
            title = _("Add user")
            url = reverse_lazy("user:delete")
            icon = "user-delete"

    :param menu str: The menu name where this MenuItem should be rendered. Can be any string.
        This menuitem is then found in templates under the ``menu.<this-menu-attr>`` menu.
        If you don't specify a menu, "main" is used.
    """

    __service__ = False
    menu: str = "main"
    url: str = ""
    slug: str = ""
    title: str = ""
    weight: int = 0
    icon: str = None
    separator: bool = False
    required_permissions: list = []
    view_name: str = ""
    badge = None
    disabled: bool = False
    exact_url = False
    check: bool = True
    visible: bool = True
    collapsed: bool = True
    enabled: bool = True
    attrs: dict = {}

    def __init__(self, request):
        """initializes a menu item during one request"""
        self.request = request
        self._children = []
        # check permissions, and set visible as needed
        if self.required_permissions:
            if isinstance(self.required_permissions, str):
                self.required_permissions = [self.required_permissions]
            if not request.user.has_perms(self.required_permissions):
                self.visible = False
                return
        if self.view_name and not request.resolver_match.view_name == self.view_name:
            self.visible = False
            return

        # we weirdly have to iterate over the __dict__ of self's Meta object,
        # as self.__dict__ is not available in Python for GDAPS plugins...?!?
        # for attr in self.__dict__:
        #     if attr in NON_CALLABLE_ATTRIBUTES:
        for attr in ["title", "url", "badge", "icon", "check"]:
            # if attribute is callable, call it with current request as param
            if callable(getattr(self, attr)):
                # call it as static method to avoid "self" as parameter
                setattr(self, attr, getattr(self.__class__, attr)(request))

        if not self.check:
            self.visible = False
            return
        # create slug form title if not available
        if not self.slug:
            self.slug = slugify(self.title)

    def has_children(self) -> bool:
        if self._children:
            return True
        found = False
        for item in IMenuItem:
            if (
                item.menu == self.menu and "." in item.slug
            ):  # TODO improve children handling
                parts = item.slug.split(".")
                if parts[0] == self.slug:
                    self._children.append(item(self.request))
                    found = True
        self._children.sort(key=lambda item: item.weight)
        return found

    def children(self) -> Iterable:
        if self.has_children():
            for item in self._children:
                yield item
        else:
            return []

    def selected(self) -> bool:
        """check current url against this item"""
        is_current = False
        if self.exact_url:  # FIXME: exact_url does not work
            if re.match(f"{self.url}$", self.request.path):
                is_current = True
        elif re.match(f"{self.url}", self.request.path):
            is_current = True
        return is_current

    def _underline_to_hyphen(self, attr: str):
        return attr.replace("_", "-")

    def attrs(self):
        attr_str = ""
        for attr in type(self).__dict__:
            if not attr.startswith("_") and attr not in INTERNAL_ATTRIBUTES:
                attr_str += f" {self._underline_to_hyphen(attr)}={getattr(self, attr)}"
        return attr_str

    def __getattr__(self, item):
        """For all attrs that are requested in the template and are
        not defined in the class, don't produce an error, just return an empty
        string."""
        return ""


class IHTMXComponentMixin(HtmxResponseMixin):
    """An interface Mixin that describes a component and can be rendered
    as plugin.

    1. Declare an interface for HTMX components
    2. Declare Implementations of that interface which also inherit from `View`.



    Examples:
        ```
        # in your plugin's api/interfaces.py
        @Interface
        class IUserProfileSection(IHTMXComponentMixin, ...):
            params = ["pk"]
            template_name = "core/user_profile_section.html"
            ...

        # in your plugin's views.py
        def PasswordView(IUserProfileSection, UpdateView)
            ...
        def OtherComponentView(IUserProfileSection, templateView)
            ...
        ```

        Use them in your template:
        ```django
        {% for plugin in IUserProfileSection %}
            TODO implement example
        {% endfor %}
        ```

    You can also inherit from other mixins, e.g. PermissionRequiredMixin, etc.

    ```python
    class UserprofilePasswordSection(IUserProfileSection, TemplateView)
        name = "password"
        template_name = "my_app/password_view.html
    ```
    """

    params: list[str] = []
    """A list of params the view is using. These must then be passed when calling
    the view from a template, e.g. via hx-get."""

    name: str = ""
    """The view name of the component. Used in URLs resolution. Must be unique."""

    title: str = ""
    """the title this plugin is rendered with. It's up to you how the plugin uses that title."""

    icon: str = ""
    """the icon name, if the component is listed in a list, and icons are used."""

    weight: int = 0
    """The weight this component is ranked like menu items. The more weight, the more the component sinks
    "down" in the list."""

    # HTMX is always enforced for components
    enforce_htmx = True

    def __init__(self, *args, **kwargs):
        if not self.name:
            raise AttributeError(
                f"{self.__class__.__name__} does not have a 'name' attribute."
            )
        super().__init__(*args, **kwargs)

    def get_path(self) -> URLPattern:
        """Calculates the url where this component is accessible.

        That can be used e.g. in hx-get attributes.
        Returns:
            a URLPattern that can be used in your urls.py
        """
        params = [f"<{p}>" for p in self.params]
        # if in production, hash component name, to hide it from prying eyes...
        component_name = (
            self.__class__.__name__ if settings.DEBUG else hash(self.__class__.__name__)
        )
        if params:
            url = f"{component_name}/{'/'.join(params)}/{self.name}/"
        else:
            url = f"{component_name}/{self.name}/"
        return path(
            url,
            self.__class__.as_view(),
            name=self.name,
        )

    def get_view_name(self) -> str:
        """Returns the component's view name.

        Use it as `{% url mycomponent.view_name ... %}` in a template.
        """
        return f"components:{self.name}"

    @classmethod
    def get_url_patterns(cls) -> list[URLPattern]:
        """Convenience method to add to your urls.py in an include section:

        Example:
            url_patterns = [
                path(...),
                path("profile/",
                    include(
                        (IUserProfileSectionView.get_url_patterns(), "profile"),
                        namespace="profile"
                    )
                ),
            ]

            # or directly add the url_patterns to the main list:

            url_patterns += IUserProfileSectionView.get_url_patterns()
        """
        patterns = []
        for interface in InterfaceRegistry._interfaces:
            if issubclass(interface, cls):
                for plugin in interface:
                    patterns.append(plugin.get_path())
        return patterns

    def enabled(self) -> bool:
        # FIXME: rename into "visible"
        """Hook for implementations to define if the component is enabled.

        Returns:
            True if the component is enabled, False if not.
        """
        return True

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def get_success_url(self):
        return self.request.path


class UseComponentMixin:
    """A mixin that can be added to a class that uses HTMX components.

    Attributes:
        components: a list of Interfaces that are used in the template of this
            view, and can be accessed there using `components.IFooInterface`.
    """

    components: list[IHTMXComponentMixin] = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        component_dict = {}
        if not self.components:
            raise AttributeError(
                f"{self.__class__.__name__} must define a 'components' attribute "
                f"with a list of of used components."
            )
        for component in self.components:
            component_dict[component.__name__] = list(component)
        context.update({"components": component_dict})
        return context


@Interface
class IUserProfileSection(IHTMXComponentMixin):
    """Plugin hook that is rendered as HTMX view in the user profile as section."""

    template_name = "common/user_profile_section.html"
    url_pattern = None

    # always return to the current component after successful save
    success_url = "."

    # This component always uses the pk of the user as parameter
    params = ["pk"]

    def has_permission(self):
        return self.request.user.is_authenticated

    def get_object(self):
        User = get_user_model()
        return User.objects.get(pk=self.kwargs.get("pk"))


class ModalFormViewMixin:
    """Mixin for FormViews that should live in a modal.

    It relies on crispy-forms intensively, and already provides a form
    helper instance attribute you can use.

    In your template, you should extend "common/modal-form.html", this
    template uses a ``header`` with a ``title`` block, a ``body``,
    and a ``footer`` block to override, for your modal dialog. In the
    footer, there is always a "Cancel" button, and as default, a "Save"
    button, which you can override using the "footer" block.

    When the modal pops up, the focus is set to the first visible input
    element.

    If the form is saved successfully, it returns an empty page
    and emits the event specified in ``success_event`` on the client,
    so that it can reload changed content.
    """

    template_name = "common/modal-form.html"
    """The default template name for the modal form. This template provides
    a simple modal form. You can extend it in your own templates too."""

    success_event: str = ""
    """A Javascript event that is triggered on the client after the form
    is saved successfully"""

    modal_title: str = ""
    """The title of the modal form"""

    def get_modal_title(self) -> str:
        """returns: a string that is used as title of the modal."""
        return self.modal_title

    def get_success_url(self):
        return ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"modal_title": self.get_modal_title()})
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # create a default form helper in case of none is created and remove form tag
        if not hasattr(form, "helper"):
            form.helper = FormHelper()
            form.helper.form_tag = False
        return form

    def form_valid(self, form):
        # call the super class, but return another Response
        super().form_valid(form)
        return HttpResponseEmpty(headers={"HX-Trigger": self.success_event})


@Interface
class ILoginFormExtension(IFormExtensionMixin):
    """Hook for FormExtensions for the MedUX login form"""


@Interface
class ILoginViewExtension(IViewExtensionMixin):
    """Hook for LoginView extensions"""
