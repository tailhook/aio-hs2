#!/bin/sh
THRIFT=${THRIFT:-thrift}
HIVE_SOURCE_DIR=${HIVE_SOURCE_DIR:-./hive}
$THRIFT -gen py:python3,asyncio,utf8strings -out aiohs2/lowlevel $HIVE_SOURCE_DIR/service/if/TCLIService.thrift

