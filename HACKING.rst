Run the tests
=============

You can run the tests using either system packages or a tox-generated virtualenv.

System packages
---------------

Using system packages makes test runs significantly faster.

If you are on a Debian-based system, install the relevant dependencies
once with:

.. code:: shell

   make dependencies

Then you can run tests with:

.. code:: shell

   make

The default Python version is 2, to run tests against Python 3 just
prepend `PYTHON=python3` to the make commands above, for
example:

.. code:: shell

   PYTHON=python3 make

Tox
---

Using tox to run the tests is easier since you won't have to deal with
not-packaged or not-recent-enough versions in your system, but it's also
a tad slower. Just run:

.. code:: shell

    tox

Cutting a release
=================

Tag and sign the new version:

.. code:: shell

    git tag -s X.Y.Z

Upload to PyPI:

.. code:: shell

    python3 setup.py sdist bdist_wheel upload -r pypi --sign -i <your key>
