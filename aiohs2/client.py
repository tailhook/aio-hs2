import asyncio

from thrift.protocol.TBinaryProtocol import TBinaryProtocolAcceleratedFactory

from .sasl_transport import TSaslAsyncioTransport
from .lowlevel.TCLIService.ttypes import TOpenSessionReq
from .lowlevel.TCLIService.TCLIService import Client as ThriftClient
from .cursor import Cursor


class Client(object):

    def __init__(self, service, session_info):
        self._svc = service
        self._hsession = session_info.sessionHandle

    @classmethod
    @asyncio.coroutine
    def connect(Client, host, port, **auth):
        if not auth:
            auth = {
                'mechanism': 'PLAIN',
                'username': 'anonymous',
                'password': 'anonymous',
                }
        trans = yield from TSaslAsyncioTransport.connect(
            host, port, **auth)
        svc = ThriftClient(trans, TBinaryProtocolAcceleratedFactory())
        info = yield from svc.OpenSession(TOpenSessionReq(client_protocol=0))
        return Client(svc, info)

    def cursor(self):
        return Cursor(self._svc, self._hsession)
