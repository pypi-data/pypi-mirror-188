import logging

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.generic import DeleteView

logger = logging.getLogger(__file__)


class HtmxResponseMixin:
    """View Mixin to add HTMX functionality.

    Attributes:
        enforce_htmx: if True, all requests that do not come from a HTMX
            component are blocked

    Raises:
        PermissionDenied: if enforce_htmx==True and request origins from a
            non-HTMX caller.
    """

    enforce_htmx: bool = True

    def get_template_names(self):
        # if self.request.htmx:
        #     if self.template_name_suffix:
        #         self.template_name_suffix += "_htmx"
        #     else:
        #         self.template_name_suffix = "_htmx"
        return super().get_template_names()

    def dispatch(self, request, *args, **kwargs):
        if self.enforce_htmx and not self.request.htmx:
            raise PermissionDenied(
                f"Permission denied: View {self.__class__.__name__} can only be "
                "called by a HTMX request."
            )
        response = super().dispatch(request, *args, **kwargs)
        return response


class HtmxDeleteView(HtmxResponseMixin, DeleteView):
    response_status = 200
    success_event = ""

    def form_valid(self, form):
        self.object.delete()
        return HttpResponse(
            status=self.response_status, headers={"HX-Trigger": self.success_event}
        )
