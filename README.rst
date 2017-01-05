System fixtures
===============

.. image:: https://img.shields.io/pypi/v/systemfixtures.svg
    :target: https://pypi.python.org/pypi/systemfixtures
    :alt: Latest Version

.. image:: https://travis-ci.org/freeekanayaka/systemfixtures.svg?branch=master
    :target: https://travis-ci.org/freeekanayaka/systemfixtures
    :alt: Build Status

.. image:: https://coveralls.io/repos/github/freeekanayaka/systemfixtures/badge.svg?branch=master
    :target: https://coveralls.io/github/freeekanayaka/systemfixtures?branch=master
    :alt: Coverage

.. image:: https://readthedocs.org/projects/systemfixtures/badge/?version=latest
    :target: http://systemfixtures.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

A collection of Python fixtures_ to fake out  various system resources (processes,
users, groups, etc.).

.. _fixtures: https://github.com/testing-cabal/fixtures

Each fake resource typically behaves as an "overlay" on the real resource, in
that it can be programmed with fake behavior for a set of inputs, but falls
back to the real behavior for the rest.

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

Support and Documentation
-------------------------

See the `online documentation <http://systemfixtures.readthedocs.io/>`_ for
a complete reference.

Developing and Contributing
---------------------------

See the `GitHub project <https://github.com/freeekanayaka/systemfixtures>`_. Bugs
can be filed in the issues tracker.
