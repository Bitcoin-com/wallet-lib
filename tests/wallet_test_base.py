import pytest
import json

from wallet_lib.adapters import WalletAdapterBase
from wallet_lib.wallet_exceptions import WalletException
from bitcoinrpc.authproxy import JSONRPCException


class WalletTestBase:

    def run_positive_case_json(self, Mock, command_run, *args):
        expected_result = {'test123': 'value123'}
        self.run_positive_case_internal(
            expected_result, '{"test123":"value123"}', Mock, command_run, *args)

    def run_positive_case(self, Mock, command_run, *args):
        self.run_positive_case_internal(
            'result123', 'result123', Mock, command_run, *args)

    def run_positive_case_internal(self, expected_result, result_bin, Mock, command_run, *args):
        wallet = WalletAdapterBase()
        Mock.return_value = result_bin
        Mock.returncode = 123

        actual_result = command_run(wallet)
        Mock.assert_called_once_with(*args)

        if(type(expected_result) == dict and type(actual_result) != dict):
            actual_result = json.loads(actual_result)
        assert expected_result == actual_result

    def run_negative_case(self, Mock, command_run, error_bin, code, error_message, *args):
        wallet = WalletAdapterBase()

        Mock.return_value = error_bin
        Mock.side_effect = WalletException(error_bin, code)
        Mock.returncode = code

        with pytest.raises(WalletException) as exc_info:
            command_run(wallet)

        Mock.assert_called_once_with(*args)
        assert error_bin == exc_info.value.reason
