=====
Usage
=====

To use Django Newsletter in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'dj_newsletter.apps.DjNewsletterConfig',
        ...
    )

Add Django Newsletter's URL patterns:

.. code-block:: python

    from dj_newsletter import urls as dj_newsletter_urls


    urlpatterns = [
        ...
        url(r'^', include(dj_newsletter_urls)),
        ...
    ]
