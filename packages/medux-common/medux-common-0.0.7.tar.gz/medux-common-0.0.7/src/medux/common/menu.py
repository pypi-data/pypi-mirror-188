from .api.interfaces import IMenuItem


class Menu:
    """Represents a named menu during a request.

    Usually it is used in Django templates by calling ``menus.<name>``
    which then will return all ``MenuItem``s with a matching "menu" name
    attribute. Therefore, Menu will be instantiated by a context_processor,
    so that the ``menu`` variable in the template

    .. code-block:: django

        <ul>
        {% for item in menus.user %}
            <li><a href="{{item.url}}">{{ item.title }}</a></li>
        {% endfor %}
        </ul>
    """

    def __init__(self, request):
        self.request = request
        self._cache = []
        for menu_item_class in IMenuItem:
            item = menu_item_class(self.request)
            self._cache.append(item)

    def _items(self):
        """walk through"""

    def __getitem__(self, item):
        """returns filtered out menu items with the given '.menu' name."""
        for menu_item in self._cache:
            # TODO: handle submenus
            if (
                menu_item.menu == item  # only items in requested menu
                and "." not in menu_item.slug  # only top level items
                and menu_item.visible  # only visible items
            ):
                yield menu_item
