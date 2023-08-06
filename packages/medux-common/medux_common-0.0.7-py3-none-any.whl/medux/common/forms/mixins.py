import logging

logger = logging.getLogger(__file__)


class ErrorLogMixin:
    """A mixin that can be added to a Form, so that it logs all form
    errors."""

    def add_error(self, field, error):
        if field:
            logger.info("Form error on field %s: %s", field, error)
        else:
            logger.info("Form error: %s", error)
        super().add_error(field, error)
