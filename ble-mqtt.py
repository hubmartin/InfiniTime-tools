#!/usr/bin/env python3
import asyncio
import sys
from bleak import BleakClient
import paho.mqtt.client as mqtt

#https://github.com/sbtinstruments/asyncio-mqtt
#https://github.com/eclipse/paho.mqtt.python/blob/master/examples/loop_asyncio.py

##
## CHANGE MY DEV PORT 1884 to default port 1883 !!!!!
##

class BLESerial:

    TX_UUID = '6e400002-b5a3-f393-e0a9-e50e24dcca9e'
    RX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

    def __init__(self, address, queue):
        self._client = BleakClient(address)
        self._queue = queue

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
        self._queue.put_nowait(data.decode('utf-8'))


async def main():

    if len(sys.argv) != 2:
        print('Please set address',  file=sys.stderr, flush=True)
        sys.exit(1)

    queue = asyncio.Queue()

    ser = BLESerial(sys.argv[1], queue)
    await ser.connect()

    print(f'Connected on {sys.argv[1]}',  file=sys.stderr, flush=True)

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("hello/#")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        queue.put_nowait(msg.payload)


    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1884, 60)

    client.loop_start()

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
