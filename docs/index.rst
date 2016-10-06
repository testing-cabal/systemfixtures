.. systemfixtures documentation master file, created by
   sphinx-quickstart on Thu Oct 27 06:54:09 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to systemfixtures's documentation!
==========================================

Overview
--------

A collection of Python fixtures_ to fake out  various system resources (processes,
users, groups, etc.).

.. _fixtures: https://github.com/testing-cabal/fixtures

Each fake resource typically behaves as an "overlay" on the real resource, in
that it can be programmed with fake behavior for a set of inputs, but falls
back to the real behavior for the rest. See the examples below for more
information.

The implementation is mostly built upon the basic MonkeyPatch_ fixture.

.. _MonkeyPatch: https://github.com/testing-cabal/fixtures/blob/master/fixtures/_fixtures/monkeypatch.py


Examples
--------

Users
+++++

The :class:`FakeUsers` fixture lets you add fake system users, that do not
exist for real, but behave the same as real ones:

.. doctest::

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

Groups
++++++

The :class:`FakeGroups` fixture lets you add fake system groups, that do not
exist for real, but behave the same as real ones:

.. doctest::

   >>> import grp

   >>> from systemfixtures import FakeGroups

   >>> groups = FakeGroups()
   >>> groups.setUp()

   >>> grp.getgrnam("foo")
   Traceback (most recent call last):
   ...
   KeyError: 'getgrnam(): name not found: foo'

   >>> groups.add("foo", 123)
   >>> info = grp.getgrnam("foo")
   >>> info.gr_gid
   123

   >>> groups.cleanUp()

Filesystem
++++++++++

The :class:`FakeFilesystem` fixture lets you add a temporary directory as
filesystem "overlay". You can declare certain paths as belonging
to the overlay, and filesystem APIs like :func:`open`, :func:`os.mkdir`,
:func:`os.chown`, :func:`os.chmod` and :func:`os.stat` will be transparently
redirected to act on the temporary directory instead of the real filesystem
path:

.. doctest::

   >>> import os
   >>> import tempfile

   >>> from systemfixtures import FakeFilesystem

   >>> filesystem = FakeFilesystem()
   >>> filesystem.setUp()

Trying to create a directory under the root one will fail, since we are
running as unprivileged user:

.. doctest::

   >>> os.mkdir("/foo")
   Traceback (most recent call last):
   ...
   PermissionError: [Errno 13] Permission denied: '/foo'

However, if we add the directory path to the fake filesystem, it will be
possible to create it as overlay directory:

.. doctest::

   >>> filesystem.add("/foo")
   >>> os.mkdir("/foo")
   >>> os.path.isdir("/foo")
   True

The overlay directory actually lives under the temporary tree of the fake
filesystem fixture:

.. doctest::

   >>> filesystem.root.path.startswith(tempfile.gettempdir())
   True
   >>> os.listdir(filesystem.root.path)
   ['foo']

It's possible to operate on the overlay directory as if it was a real
top-level directory:

.. doctest::

   >>> with open("/foo/bar", "w") as fd:
   ...    fd.write("Hello world!")
   12
   >>> with open("/foo/bar") as fd:
   ...    fd.read()
   'Hello world!'
   >>> os.listdir("/foo")
   ['bar']

It's possible to change the ownership of files in the overlay directory,
even without superuser priviliges:

.. doctest::

   >>> os.chown("/foo/bar", 0, 0)
   >>> os.chmod("/foo/bar", 0o600)
   >>> info = os.stat("/foo/bar")
   >>> info.st_uid, info.st_gid
   (0, 0)
   >>> oct(info.st_mode)
   '0o100600'

   >>> filesystem.cleanUp()

Network
+++++++

The :class:`FakeNetwork` fixture is simply fixture-compatible adapter of
the :class:`requests-mock` package, which provides facilities to stub
out responses from the :class:`requests` package. For further details
see the `official documentation <https://requests-mock.readthedocs.io/en/latest/>`_.

.. doctest::

   >>> import requests

   >>> from systemfixtures import FakeNetwork

   >>> network = FakeNetwork()
   >>> network.setUp()

   >>> network.get("http://test.com", text="data")  # doctest: +ELLIPSIS
   <requests_mock.adapter._Matcher object at ...>
   >>> response = requests.get("http://test.com")
   >>> response.text
   'data'

   >>> network.cleanUp()

Time
++++

The :class:`FakeTime` fixture is simply fixture-compatible adapter of
the :class:`fakesleep` package, which provides facilities to stub
out the API of :class:`time` package from the standard library. See
the `external documentation <https://github.com/wearpants/fakesleep>`_

.. doctest::

   >>> import time

   >>> from systemfixtures import FakeTime

   >>> fake_time = FakeTime()
   >>> fake_time.setUp()

   >>> stamp1 = time.time()
   >>> time.sleep(1)
   >>> stamp2 = time.time()

Since :func:`sleep()` and :func:`time()` are fake, we get *exactly* 1.0:

.. doctest::

   >>> stamp2 - stamp1
   1.0

   >>> fake_time.cleanUp()

Processes
+++++++++

The :class:`FakeProcesses` fixture lets you fake out processes spawed with
:class:`subprocess.Popen`, and have custom Python code be executed instead.

You can both override available system executables, or add new ones
are not available on the system:

.. doctest::

   >>> import io
   >>> import subprocess

   >>> from systemfixtures import FakeProcesses

   >>> processes = FakeProcesses()
   >>> processes.setUp()

   >>> subprocess.check_output(["uname"])
   b'Linux\n'

   >>> def uname(proc_args):
   ...     return {"stdout": io.BytesIO(b"Darwin\n")}

   >>> processes.add(uname, name="uname")
   >>> processes.uname  # doctest: +ELLIPSIS
   <function uname at ...>

   >>> subprocess.check_output(["uname"])
   b'Darwin\n'

   >>> def foo(proc_args):
   ...     return {"stdout": io.BytesIO(b"Hello world!")}

   >>> processes.add(foo, name="foo")
   >>> subprocess.check_output(["foo"])
   b'Hello world!'

Some stock fake processes are provided as well:

wget
^^^^

.. doctest::

   >>> from systemfixtures.processes import Wget

   >>> processes.add(Wget())
   >>> processes.wget.locations["http://foo"] = b"Hello world!"

   >>> subprocess.check_output(["wget", "-O", "-", "http://foo"])
   b'Hello world!'

systemctl
^^^^^^^^^

.. doctest::

   >>> from systemfixtures.processes import Systemctl

   >>> processes.add(Systemctl())

   >>> try:
   ...    subprocess.check_output(["systemctl", "is-active", "foo"])
   ... except subprocess.CalledProcessError as error:
   ...     error.output
   b'inactive\n'

   >>> subprocess.check_call(["systemctl", "start", "foo"])
   0
   >>> subprocess.check_output(["systemctl", "is-active", "foo"])
   b'active\n'
   >>> subprocess.check_call(["systemctl", "stop", "foo"])
   0

   >>> processes.systemctl.actions["foo"]
   ['start', 'stop']

dpkg
^^^^

.. doctest::

   >>> from systemfixtures.processes import Dpkg

   >>> processes.add(Dpkg())
   >>> subprocess.check_call(["dpkg", "-i", "foo_1.0-1.deb"])
   0
   >>> processes.dpkg.actions["foo"]
   ['install']

.. doctest::

  >>> processes.cleanUp()


