# -*- coding: utf-8
"""Representation of the newsletter application and its configuration."""

# Standard library
import logging

# Django
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class NewsletterConfig(AppConfig):
    """Representation of the newsletter application and its configuration."""

    name = 'newsletter'

    def ready(self):
        """Run when Django starts."""
        logger.debug("App {} ready.".format(self.name))
