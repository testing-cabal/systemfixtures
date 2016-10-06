=====================================================
Test fixtures for faking out various system resources
=====================================================

.. image:: https://img.shields.io/pypi/v/systemfixtures.svg
    :target: https://pypi.python.org/pypi/systemfixtures
    :alt: Latest Version

.. image:: https://travis-ci.org/freeekanayaka/systemfixtures.svg?branch=master
    :target: https://travis-ci.org/freeekanayaka/systemfixtures
    :alt: Build Status

.. image:: https://coveralls.io/repos/github/freeekanayaka/charm-test/badge.svg?branch=master
    :target: https://coveralls.io/github/freeekanayaka/charm-test?branch=master
    :alt: Coverage

Example
-------

Please see the `full documentation <http://pythonhosted.org/systemfixtures/>`_ for
more information.

.. code:: python

   >>> import pwd

   >>> from systemfixtures import FakeUsers

   >>> users = FakeUsers()
   >>> users.setUp()

   >>> pwd.getpwnam("foo")
   Traceback (most recent call last):
   ...
   KeyError: 'getpwnam(): name not found: foo'

   >>> users.add("foo", 123)
   >>> info = pwd.getpwnam("foo")
   >>> info.pw_uid
   123
   >>> users.cleanUp()
