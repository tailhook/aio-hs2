#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

import struct
import enum
import asyncio

from puresasl.client import SASLClient
from thrift.TAsyncio import TAsyncioTransport


sasl_header = struct.Struct('>BI')


class SaslChallenge(enum.Enum):

    START = 1
    OK = 2
    BAD = 3
    ERROR = 4
    COMPLETE = 5


class SaslChallengeException(Exception):
    pass


class TSaslAsyncioTransport(TAsyncioTransport):
    """a framed, buffered transport over a Tornado stream"""

    # not the same number of parameters as TTransportBase.open
    @classmethod
    @asyncio.coroutine
    def connect(TSaslAsyncioTransport, host, port, *,
        mechanism='PLAIN', **auth):
        reader, writer = yield from asyncio.open_connection(host, port)

        # We authorize right there, because packet framing is different
        # here, in authentication and in real message stream
        sasl = SASLClient(host,
            mechanism=mechanism,
            qops = (b'auth',),  # No protection supported so far
            **auth)
        bmech = mechanism.encode('ascii')
        writer.write(sasl_header.pack(
            SaslChallenge.START.value, len(bmech))
            + bmech)
        startseq = sasl.process()
        writer.write(sasl_header.pack(
            SaslChallenge.OK.value, len(startseq))
            + startseq)
        while True:
            header = yield from reader.readexactly(5)
            status, bodylen = sasl_header.unpack(header)
            status = SaslChallenge(status)
            body = yield from reader.readexactly(bodylen)
            if status == SaslChallenge.COMPLETE:
                break
            elif status == SaslChallenge.OK:
                response = sasl.process(body)
                writer.write(sasl_header.pack(
                    SaslChallenge.OK.value, len(response))
                    + response)
            else:
                raise SaslChallengeException(
                    "Bad SASL challenge: {}/{!r}".format(status, body))

        return TSaslAsyncioTransport(reader, writer)
