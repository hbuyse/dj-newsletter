=============================
Django Newsletter
=============================

.. image:: https://gitlab.com/hbuyse/dj-newsletter/badges/dev/build.svg
    :target: https://gitlab.com/hbuyse/dj-newsletter

.. image:: https://gitlab.com/hbuyse/dj-newsletter/badges/dev/coverage.svg
    :target: https://gitlab.com/hbuyse/dj-newsletter

.. image:: https://codecov.io/gh/hbuyse/dj-newsletter/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/hbuyse/dj-newsletter

Django Newsletter for django

Documentation
-------------

The full documentation is at https://dj-newsletter.readthedocs.io.

Quickstart
----------

Install Django Newsletter::

    pip install dj-newsletter

Add it to your `INSTALLED_APPS`:

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

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
