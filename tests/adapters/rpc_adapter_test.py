import os
import pytest
from unittest.mock import patch

from unittest import TestCase
from wallet_lib.adapters import RPCAdapter
from wallet_lib.adapters.rpc_adapter import RPCAdapterException
from bitcoinrpc.authproxy import JSONRPCException


class RPCAdapterTest(TestCase):
    def setUp(self):
        self.rpc_adapter = RPCAdapter(
            os.environ['RPC_USER'],
            os.environ['RPC_PASSWORD'],
            os.environ['RPC_URL'],
            os.environ['RPC_PORT'])

    @patch('bitcoinrpc.authproxy.AuthServiceProxy.batch_')
    def test_run_positive(self, ASPMock):
        command = 'abc'
        code = 123
        expected_result = 'abc123'

        ASPMock.return_value = [expected_result]
        ASPMock.code = code

        actual_result = self.rpc_adapter.run([command])
        ASPMock.assert_called_once_with([[[command]]])
        assert expected_result == actual_result.result

    @patch('bitcoinrpc.authproxy.AuthServiceProxy.batch_')
    def test_run_negative(self, ASPMock):
        command = 'abc'
        code = 123
        expected_result = 'Failed to run {} command'.format(command)
        error_bin = 'abc'

        ASPMock.return_value = 123
        ASPMock.message = expected_result
        ASPMock.side_effect = RPCAdapterException(reason=expected_result)
        ASPMock.code = code

        with pytest.raises(RPCAdapterException) as exc_info:
            self.rpc_adapter.run(command)

        ASPMock.assert_called_once_with([[command]])
        assert expected_result == exc_info.value.reason
