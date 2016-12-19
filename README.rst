Tuteria-Application-Test
========================

These are the tests that needs to be passed before getting an interview to work with Tuteria

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django




:License: MIT


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Activities to be Carried out
----------------------------
Create a fork of this repo and implement the below Activities


Create a postgres Database
^^^^^^^^^^^^^^^^^^^^^^^^^^

* Create a postgres database and setup the environmental variable `DATABASE_URL` to point to the url format of the database created.


For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Work to be done
^^^^^^^^^^^^^^^
1. Ensure that all tests in `users/test/test_models.py` are all passing.

2. Ensure that the tests in `users/test/test_views.py` are all passing. This would require knowledge of `djangorestframework` usage.
3. Ensure that any dependency added used is added to the `requirements/local.txt` file.


Do not change the contents of the test files. 
==============================================


Even if it appears there are errors in the tests. your solution should fix it
==============================================================================


After Completion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Initiate a pull request back to the repo and ensure that all the test are passing,

This repo has been setup with a continous integration server known as Travis that 
automatically runs all the tests and would only proceed when all the tests are passing.

Once the CI indicates that all tests are passing, You would be contacted.

Ensure that the application runs locally on your system and all the tests pass before submitting a pull request
=================================================================================================================
