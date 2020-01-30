import time
import pytest
import asyncio
import pytest_asyncio.plugin

from unittest import TestCase
from unittest.mock import patch, Mock
from wallet_lib import ZMQNotifier

# For constants
import zmq
import signal

class ZMQNotifierTest(TestCase):

    def test_zmq_socket(self):
        with patch('zmq.asyncio.Context') as zmq_socket:
            zmq_socket.return_value.connect()
            fake_url= "protocol://ip_address:port"
            notifier = ZMQNotifier(fake_url)
            notifier.zmqSubSocket.setsockopt.assert_called_once_with(zmq.RCVHWM, 0)
            notifier.zmqSubSocket.connect.assert_called_once_with(fake_url)
            notifier.zmqContext.socket.assert_called_once_with(zmq.SUB)

    def test_zmq_subscribe_to_topic(self):
        with patch('zmq.asyncio.Context') as zmq_socket:
            zmq_socket.return_value.setsockopt_string()
            topics = ['topic1', 'topic2']
            notifier = ZMQNotifier("zmq_address", topics=topics)
            notifier.zmqSubSocket.setsockopt_string.assert_any_call(zmq.SUBSCRIBE, topics[0])
            notifier.zmqSubSocket.setsockopt_string.assert_any_call(zmq.SUBSCRIBE, topics[1])

    def test_get_positive_callbacks_in_listener_map(self):
        with patch('zmq.asyncio.Context'):
            t1cb = Mock(return_value=None)
            t2cb = Mock(return_value=None)
            ecb = Mock(return_value=None)

            actual = ZMQNotifier(
                "zmq_address",
                topics=['topic1', 'topic2'],
                topic1_callback=t1cb,
                topic2_callback=t2cb,
                error_callback=ecb
            ).listeners

            expected = {
                'topic1': [t1cb],
                'topic2': [t2cb],
                '_error_': [ecb],
            }
            
            TestCase().assertDictEqual(expected, actual)

    def test_get_positive_add_multiple_callbacks_in_listener_map(self):
        with patch('zmq.asyncio.Context'):
            t1cb1 = Mock(return_value=None)
            t1cb2 = Mock(return_value=None)
            t2cb1 = Mock(return_value=None)
            t2cb2 = Mock(return_value=None)
            ecb1 = Mock(return_value=None)
            ecb2 = Mock(return_value=None)

            notifier = ZMQNotifier("zmq_address", topics=['topic1', 'topic2'])

            notifier.add_callback('topic1', t1cb1)
            notifier.add_callback('topic1', t1cb2)
            notifier.add_callback('topic2', t2cb1)
            notifier.add_callback('topic2', t2cb2)
            notifier.add_error_callback(ecb1)
            notifier.add_error_callback(ecb2)

            actual = notifier.listeners

            expected = {
                'topic1': [t1cb1, t1cb2],
                'topic2': [t2cb1, t2cb2],
                '_error_': [ecb1, ecb2],
            }
            
            TestCase().assertDictEqual(expected, actual)

    @patch('asyncio.get_event_loop')
    @patch('wallet_lib.ZMQNotifier.handle')
    def test_get_positive_zmq_notifier_start(self, mock_loop, _):
        mock_loop.return_value.add_signal_handler
        mock_loop.return_value.create_task
        mock_loop.return_value.run_forever
        
        with patch('zmq.asyncio.Context') as zmq_socket:
            zmq_socket.return_value.connect()
            notifier = ZMQNotifier("zmq_address")
            loop = notifier.start()
            loop.add_signal_handler.assert_called()
            loop.run_forever.assert_called_once()
