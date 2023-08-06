from crispy_forms.layout import Div, Field
from crispy_forms.utils import flatatt


class Card(Div):
    """
    Layout object. It wraps fields in a Card.

    Example:
        Card(
            'form_field_1',
            'form_field_2',
            title="Sample card"
            subtitle="Always play nice."
        )
    """

    template = "%s/layout/card.html"

    def __init__(
        self,
        *fields,
        title="",
        title_id="",
        title_class="",
        subtitle="",
        **kwargs,
    ):

        super().__init__(*fields, **kwargs)
        self.title = title
        self.title_id = title_id or f"card-title-{hash(self)}"
        self.title_class = title_class
        self.subtitle = subtitle

        kwargs = {
            **kwargs,
            "aria-labelledby": "%s-label" % self.title_id,
        }

        self.flat_attrs = flatatt(kwargs)


class RadioSelectButtonsGroup(Field):
    template = "bootstrap5/layout/radioselect_buttonsgroup.html"
