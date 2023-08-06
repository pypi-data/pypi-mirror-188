import json

from django.contrib.messages import get_messages
from django.http import HttpResponse


# from bs4 import BeautifulSoup

# bases on Benoit Blanchon's
# https://blog.benoitblanchon.fr/django-htmx-messages-framework/
class HtmxMessageMiddleware:
    """Filters out django messages and puts them in to the HX-Trigger header if
    current request is a HTMX request"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response: HttpResponse = self.get_response(request)

        # soup = BeautifulSoup(response.content, "html.parser")
        # body_tag = soup.find("body")
        # body_tag.append(soup.new_tag("div", string="test"))
        # response.content = str(soup)
        # response.content += b"<div id='request-item-15' hx-swap-oob='True'>foo</div>"
        if not request.htmx:
            return response

        # Extract the messages, if response is empty
        if response.status_code == 204:  # Empty
            messages = [
                {
                    "message": message.message,
                    "tags": message.tags,
                    "extra_tags": message.extra_tags,
                }
                for message in get_messages(request)
            ]
            # response.content += (
            #     b"""<div id='toasts' hx-swap-oob='beforeend'>FOO</div>"""
            # )
        else:
            messages = []
        if not messages:
            return response

        # Get the existing HX-Trigger that could have been defined by the view
        hx_trigger = response.headers.get("HX-Trigger")

        if hx_trigger is None:
            # If the HX-Trigger is not set, start with an empty object
            hx_trigger = {}
        elif hx_trigger.startswith("{"):
            # If the HX-Trigger uses the object syntax, parse the object
            hx_trigger = json.loads(hx_trigger)
        else:
            # If the HX-Trigger uses the string syntax, convert to the object syntax
            hx_trigger = {hx_trigger: True}

        # Add the messages array in the HX-Trigger object
        hx_trigger["messages"] = messages

        # Add or update the HX-Trigger
        response.headers["HX-Trigger"] = json.dumps(hx_trigger)
        return response
