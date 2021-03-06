===============================
Asyncio-base Hiveserver2 Client
===============================

This client can connect both hiveserver2 from hive and sharkserver2 for shark
(because latter have same protocol and semantics)

Package contains:

* ``thrift/`` -- a copy of thrift python library adapted for python3.
  The code originally in https://github.com/tailhook/thrift/tree/asyncio
* ``aiohs2/lowlevel`` -- python files generated for ``TCLIService.thrift`` from
  hive.  To regenerate bindings run ``./genbindings.sh`` (you need to build
  thrift from aformentioned branch and you need hive sources, script will not
  do that for you)

To use a library you just install it with ``pip`` or ``setup.py``.


Basic Usage
-----------

.. code-block:: python

    cli = Client('localhost', 10000)
    with (yield from cli.cursor()) as cur:
        yield from cur.execute("SELECT * FROM table LIMIT 10")
        rows = yield from cur.fetch()
        print("ROWS", rows)


Upgrade Notes
-------------

In version 0.1 client was connected by ``Client.connect`` and cursor was
created by a plain function (not coroutine). It's changed to support
transparent reconnection.
