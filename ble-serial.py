#!/usr/bin/env python3
import asyncio
import sys
from bleak import BleakClient

class BLESerial:

    TX_UUID = '6e400002-b5a3-f393-e0a9-e50e24dcca9e'
    RX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

    def __init__(self, address):
        self._client = BleakClient(address)

    def is_connected(self):
        return self._client.is_connected()

    def write(self, data):
        if isinstance(data, str):
            data = bytearray(data, 'utf-8')
        return self._client.write_gatt_char(self.TX_UUID, data)

    async def connect(self):
        await self._client.connect()
        await self._client.start_notify(self.RX_UUID, self._notification_handler)

    def _notification_handler(self, sender, data):
        print(data.decode('utf-8'), end='', file=sys.stdout, flush=True)


async def main():

    if len(sys.argv) != 2:
        print('Please set address',  file=sys.stderr, flush=True)
        sys.exit(1)

    queue = asyncio.Queue()

    ser = BLESerial(sys.argv[1])
    await ser.connect()

    print(f'Connected on {sys.argv[1]}',  file=sys.stderr, flush=True)

    loop = asyncio.get_event_loop()

    def read_line():
        line = sys.stdin.readline()
        if line:
            queue.put_nowait(line)

    task = loop.add_reader(sys.stdin.fileno(), read_line)

    while 1:
        line = await queue.get()
        await ser.write(line)

try:
    asyncio.run(main())
except Exception as e:
    print(str(e), file=sys.stderr, flush=True)
    sys.exit(1)
