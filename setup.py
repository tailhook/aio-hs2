#!/usr/bin/env python

from distutils.core import setup

setup(name='aio-hs2',
      version='0.1',
      description='Asyncio-based client for hiveserver2 (and sharkserver2)',
      author='Paul Colomiets',
      author_email='paul@colomiets.name',
      url='http://github.com/tailhook/aio-hs2',
      packages=[
        'aiohs2',
        'aiohs2.lowlevel',
        'thrift',
        'thrift.protocol',
        'thrift.transport',
        'thrift.server',
        ],
      requires=['puresasl'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        ],
     )
