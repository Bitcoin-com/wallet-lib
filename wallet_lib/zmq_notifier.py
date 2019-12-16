""" Implementation based on: https://github.com/bitcoin/bitcoin/blob/master/contrib/zmq/zmq_sub.py """

import traceback
import binascii
import asyncio
import zmq
import zmq.asyncio as zmq_asyncio
import signal
import struct
import time
import sys
import os

class ZMQNotifer():

    TOPIC_BLOCKHASH = 'hashblock'
    TOPIC_TXID = 'hashtx'
    TOPIC_RAWBLOCK = 'rawblock'
    TOPIC_RAWTX = 'rawtx'

    def __init__(self, zmq_address, timeout=0, topics=['hashblock', 'hashtx', 'rawblock', 'rawtx'], **kwargs):
        self.timeout = timeout
        self.zmqContext = zmq_asyncio.Context()
        self.topic_set = set([s.strip() for s in topics])

        self.zmqSubSocket = self.zmqContext.socket(zmq.SUB)
        self.zmqSubSocket.setsockopt(zmq.RCVHWM, 0)
        earg = 'error_callback'
        ecb = kwargs[earg] if earg in kwargs else []
        self.listeners = {'error': ecb }

        for topic in self.topic_set:
            targ = topic + '_callback'
            self.listeners[topic] = kwargs[targ] if targ in kwargs else []
            self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, topic)

        self.zmqSubSocket.connect(zmq_address)

    def add_callback(self, topic, callback):
        self.listeners['tx'].append(callback)

    def add_error_callback(self, callback):
        self.listeners['error'].append(callback)

    async def handle(self):
        try:
            msg = await self.zmqSubSocket.recv_multipart()
            topic = msg[0].decode('utf8')
            body = msg[1]

            if topic in self.topic_set:
                hex_body = binascii.hexlify(body)
                for callback in self.listeners[topic]:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(hex_body, body)
                    else: callback(hex_body, body)

            if self.timeout > 0:
                time.sleep(self.timeout / 1000)

            asyncio.ensure_future(self.handle())
        except Exception as e:
            for callback in self.listeners['error']:
                if asyncio.iscoroutinefunction(callback):
                    tb = await callback(e)
                else: tb = callback(e)
                if tb: traceback.print_exc()
            self.stop()

    def start(self, forever):
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, self.stop)
        loop.create_task(self.handle())
        if forever: loop.run_forever()
        else: loop.run_until_complete(self.stop())
        return loop

    def stop(self):
        self.zmqContext.destroy()