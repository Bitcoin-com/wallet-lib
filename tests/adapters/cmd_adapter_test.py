import os
import pytest
from unittest.mock import patch

from unittest import TestCase
from wallet_lib.adapters import CMDAdapter
from wallet_lib.adapters.cmd_adapter import CMDAdapterException
from bitcoinrpc.authproxy import JSONRPCException


class CMDAdapterTest(TestCase):
    def setUp(self):
        self.cmd_adapter = CMDAdapter('abc')

    @patch('subprocess.Popen')
    def test_run_positive(self, PopenMock):
        command = 'abc123'
        result_bin = b'  abc123  '
        expected_result = 'abc123'

        mock_proc = PopenMock.return_value
        mock_proc.returncode = 123
        mock_proc.communicate.return_value = (result_bin, b'')

        actual_result = self.cmd_adapter.run(command)

        PopenMock.assert_called_once_with(
            ['abc', command], stdout=-1, stderr=-1)

        assert expected_result == actual_result.result

    @patch('subprocess.Popen', autospec=True)
    def test_run_negative(self, PopenMock):
        command = 'abc123'
        result_bin = b'  abc123  '
        expected_result = "Failed to run %s command" % (command)

        PopenMock.return_value.returncode = 123
        PopenMock.side_effect = CMDAdapterException(reason=expected_result)
        PopenMock.return_value.communicate.return_value = (result_bin, b'')
        with pytest.raises(CMDAdapterException) as exc_info:
            self.cmd_adapter.run(command)

        PopenMock.assert_called_once_with(
            ['abc', command], stdout=-1, stderr=-1)
        assert expected_result == exc_info.value.reason
