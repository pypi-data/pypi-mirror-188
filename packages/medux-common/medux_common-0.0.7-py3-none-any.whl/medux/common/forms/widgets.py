# https://gist.github.com/andytwoods/76f18f5ddeba9192d51dccc922086e43#file-minimalsplitdatetimemultiwidget-py
from datetime import datetime

from django import forms
from django.utils.timezone import make_aware
from django.forms import TextInput, MultiWidget, DateTimeField

# FIXME: none of *SplitDateTimeMultiWidget work correctly...


# nightmare discussion here https://stackoverflow.com/questions/38601/using-django-time-date-widgets-in-custom-form
class MinimalSplitDateTimeMultiWidget(MultiWidget):
    def __init__(self, widgets=None, attrs=None):
        if widgets is None:
            if attrs is None:
                attrs = {}
            date_attrs = attrs.copy()
            time_attrs = attrs.copy()

            date_attrs["type"] = "date"
            time_attrs["type"] = "time"

            widgets = [
                TextInput(attrs=date_attrs),
                TextInput(attrs=time_attrs),
            ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.date(), value.strftime("%H:%M")]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        date_str, time_str = super().value_from_datadict(data, files, name)
        # DateField expects a single string that it can parse into a date.

        if date_str == time_str == "":
            return None

        if time_str == "":
            time_str = "00:00"

        my_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        # make it timezone aware
        return make_aware(my_datetime)


class SplitDateTimeWidget(forms.SplitDateTimeWidget):
    """
    A widget that splits datetime input into two <input type="text"> boxes,
    and uses HTML5 'date' and 'time' inputs.
    """

    def __init__(
        self,
        attrs=None,
        date_format=None,
        time_format=None,
        date_attrs=None,
        time_attrs=None,
    ):
        date_attrs = date_attrs or {}
        time_attrs = time_attrs or {}
        if "type" not in date_attrs:
            date_attrs["type"] = "date"
        if "type" not in time_attrs:
            time_attrs["type"] = "time"
        super().__init__(
            attrs=attrs,
            date_format=date_format,
            time_format=time_format,
            date_attrs=date_attrs,
            time_attrs=time_attrs,
        )

    def decompress(self, value):
        if value:
            return [value.date(), value.strftime("%H:%M")]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        date_str, time_str = super().value_from_datadict(data, files, name)
        # DateField expects a single string that it can parse into a date.

        if date_str == time_str == "":
            return None

        if time_str == "":
            time_str = "00:00"

        my_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        # make it timezone aware
        return make_aware(my_datetime)


class SplitDateTimeField(forms.SplitDateTimeField):
    widget = SplitDateTimeWidget
