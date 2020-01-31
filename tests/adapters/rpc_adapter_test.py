import pytest
from unittest.mock import patch

from unittest import TestCase
from wallet_lib.adapters import RPCAdapter
from wallet_lib.adapters.rpc_adapter import RPCAdapterException, RPCAdapterResponse
from bitcoinrpc.authproxy import JSONRPCException


class RPCAdapterTest(TestCase):
    def setUp(self):
        self.rpc_adapter = RPCAdapter()

    @patch('bitcoinrpc.authproxy.AuthServiceProxy.batch_')
    def test_run_positive(self, ASPMock):
        command = 'abc'
        code = 123
        expected_result = 'abc123'

        ASPMock.return_value = [expected_result]
        ASPMock.code = code

        actual_response = self.rpc_adapter.run([command])
        ASPMock.assert_called_once_with([[[command]]])
        expected_response = RPCAdapterResponse(expected_result, error=None, code=code)
        assert actual_response.error == expected_response.error == None
        assert actual_response.result == expected_response.result == expected_result

    @patch('bitcoinrpc.authproxy.AuthServiceProxy.batch_')
    def test_run_negative(self, ASPMock):
        command = 'abc'
        code = 123
        expected_result = 'Failed to run {} command'.format(command)

        ASPMock.return_value = 123
        ASPMock.message = expected_result
        ASPMock.side_effect = RPCAdapterException(expected_result)
        ASPMock.code = code

        with pytest.raises(RPCAdapterException) as exc_info:
            self.rpc_adapter.run(command)

        ASPMock.assert_called_once_with([[command]])
        assert expected_result == exc_info.value.reason
