""" Implementation based on: https://github.com/bitcoin/bitcoin/blob/master/contrib/zmq/zmq_sub.py """

import zmq.asyncio
import traceback
import binascii
import asyncio
import signal
import struct
import time
import sys
import zmq
import os

class ZMQNotifer():

    TOPIC_BLOCKHASH = 'hashblock'
    TOPIC_TXID = 'hashtx'
    TOPIC_RAWBLOCK = 'rawblock'
    TOPIC_RAWTX = 'rawtx'

    def __init__(self, zmq_address, topics=[TOPIC_BLOCKHASH, TOPIC_TXID, TOPIC_RAWBLOCK, TOPIC_RAWBLOCK], **kwargs):
        self.zmqContext = zmq.asyncio.Context()
        self.topic_set = set([s.strip() for s in topics])

        self.zmqSubSocket = self.zmqContext.socket(zmq.SUB)
        self.zmqSubSocket.setsockopt(zmq.RCVHWM, 0)
        earg = 'error_callback'
        ecb = [kwargs[earg]] if earg in kwargs else []
        self.listeners = {'_error_': ecb }

        for topic in self.topic_set:
            targ = topic + '_callback'
            self.listeners[topic] = [kwargs[targ]] if targ in kwargs else []
            self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, topic)

        self.zmqSubSocket.connect(zmq_address)

    def add_callback(self, topic, callback):
        self.listeners[topic].append(callback)

    def add_error_callback(self, callback):
        self.listeners['_error_'].append(callback)

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

            asyncio.ensure_future(self.handle())
        except Exception as e:
            for callback in self.listeners['error']:
                if asyncio.iscoroutinefunction(callback):
                    tb = await callback(e)
                else: tb = callback(e)
                if tb: traceback.print_exc()
            self.stop()

    def start(self, forever=True):
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, self.stop)
        loop.create_task(self.handle())
        if forever: loop.run_forever()
        else: loop.run_until_complete(self.stop())
        return loop

    def stop(self):
        self.zmqContext.destroy()