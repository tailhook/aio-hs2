import argparse
import asyncio
from aiohs2 import Client


@asyncio.coroutine
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-H', '--host', default='localhost')
    ap.add_argument('-p', '--port', default=10000, type=int)
    ap.add_argument('query')
    options = ap.parse_args()

    cli = yield from Client.connect(options.host, options.port)
    with cli.cursor() as cur:
        yield from cur.execute(options.query)
        rows = yield from cur.fetch()
        print("ROWS", rows)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
