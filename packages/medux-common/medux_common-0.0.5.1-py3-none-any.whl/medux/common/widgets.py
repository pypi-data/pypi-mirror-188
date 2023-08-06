from crispy_forms import bootstrap
from django import forms

# ------------ Django Widgets ------------


class ButtonGroupRadioSelect(forms.RadioSelect):
    """A Bootstrap button-group input widget instead of a radio."""

    template_name = "common/widgets/buttongroup_radioselect.html"


class SwitchInput(forms.CheckboxInput):
    """A Bootstrap switch input widget instead of a checkbox."""

    template_name = "common/widgets/switch.html"

    def __init__(self, wrapper_class: str = None, **kwargs):
        super().__init__(**kwargs)
        self.wrapper_class = wrapper_class or ""

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["attrs"]["class"] = "form-check-input"
        context.update({"wrapper": {"class": self.wrapper_class}})
        return context


# ------------ Crispy Layout Fields ------------


class BooleanTextFieldButtonsGroup(bootstrap.Field):
    template = "%s/layout/textfield_buttonsgroup.html"


class ColorInput(bootstrap.InlineRadios):
    template = "bootstrap5/layout/color_input.html"
