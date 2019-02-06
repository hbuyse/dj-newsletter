=====
Usage
=====

To use Django Newsletter in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'newsletter.apps.DjNewsletterConfig',
        ...
    )

Add Django Newsletter's URL patterns:

.. code-block:: python

    from newsletter import urls as newsletter_urls


    urlpatterns = [
        ...
        url(r'^', include(newsletter_urls)),
        ...
    ]
