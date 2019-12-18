import pytest

from unittest import TestCase
from unittest.mock import patch, Mock
from wallet_lib import ZMQNotifer

# For constants
import zmq
import signal

# TODO:
"""
    zmqnotifier:
    add example

    add test case: error callback called
    add test case: topic callbacks called
    add test case: consume topic message

    add test case: wallet_base_test + ***_wallet_test.py
"""

class ZMQNotifierTest(TestCase):

    def test_zmq_socket(self):
        with patch('zmq.asyncio.Context') as zmq_socket:
            zmq_socket.return_value.connect()
            fake_url= "protocol://ip_address:port"
            notifier = ZMQNotifer(fake_url)
            notifier.zmqSubSocket.setsockopt.assert_called_once_with(zmq.RCVHWM, 0)
            notifier.zmqSubSocket.connect.assert_called_once_with(fake_url)
            notifier.zmqContext.socket.assert_called_once_with(zmq.SUB)

    def test_zmq_subscribe_to_topic(self):
        with patch('zmq.asyncio.Context') as zmq_socket:
            zmq_socket.return_value.setsockopt_string()
            topics = ['topic1', 'topic2']
            notifier = ZMQNotifer("zmq_address", topics=topics)
            notifier.zmqSubSocket.setsockopt_string.assert_any_call(zmq.SUBSCRIBE, topics[0])
            notifier.zmqSubSocket.setsockopt_string.assert_any_call(zmq.SUBSCRIBE, topics[1])

    def test_get_positive_callbacks_in_listener_map(self):
        with patch('zmq.asyncio.Context'):
            t1cb = Mock(return_value=None)
            t2cb = Mock(return_value=None)
            ecb = Mock(return_value=None)

            actual = ZMQNotifer(
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

            notifier = ZMQNotifer("zmq_address", topics=['topic1', 'topic2'])

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

    # @patch('asyncio.get_event_loop')
    # def test_get_positive_zmq_start_forever(self, mock_loop):
    #     mock_loop.return_value.add_signal_handler()
    #     mock_loop.return_value.create_task()
    #     mock_loop.return_value.run_until_complete()
    #     mock_loop.return_value.run_forever()
        
    #     with patch('zmq.asyncio.Context') as zmq_socket:
    #         zmq_socket.return_value.connect()
    #         notifier = ZMQNotifer("zmq_address")
    #         notifier.start() # Ensures that 'forever' is True by default
    #         mock_loop.add_signal_handler.assert_called_once_with(signal.SIGINT, notifier.stop)
    #         mock_loop.create_task.assert_called_once_with(notifier.handle())
    #         mock_loop.run_until_complete.assert_called_once_with(notifier.stop())
    #         mock_loop.run_forever.assert_called_once()

    # @patch('asyncio.get_event_loop')
    # def test_get_positive_zmq_start(self, mockLoop):
    #     ml = mockLoop.return_value
    #     ml.add_signal_handler.return_value = None
    #     ml.create_task.return_value = None
    #     ml.run_until_complete.return_value = None
    #     ml.run_forever.return_value = None
    #     with patch('zmq.asyncio.Context'):
    #         notifier = ZMQNotifer("zmq_address")
    #         loop = notifier.start(False)
    #         mockLoop.add_signal_handler.assert_called_once_with(signal.SIGINT, notifier.stop)
    #         mockLoop.create_task.assert_called_once_with(notifier.handle())
    #         mockLoop.run_until_complete.assert_called_once_with(notifier.stop())
    #         assert loop is mockLoop()