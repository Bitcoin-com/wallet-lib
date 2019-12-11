import pytest
import json
from unittest.mock import patch
from bitcoinrpc.authproxy import JSONRPCException
from wallet_lib.wallet_exceptions import WalletException


class RPCWalletBase:
    wallet_factory = None

    @patch('bitcoinrpc.authproxy.AuthServiceProxy.batch_')
    def test_create_address_positive(self, ASPMock):
        label = 'abc123'
        self.run_positive_case(
            ASPMock,
            'getnewaddress',
            lambda w: w.create_address(label),
            label
        )

    @patch('bitcoinrpc.authproxy.AuthServiceProxy.batch_')
    def test_get_balance_positive(self, ASPMock):
        self.run_positive_case(
            ASPMock,
            'getbalance',
            lambda w: w.get_balance(),
        )

    @patch('bitcoinrpc.authproxy.AuthServiceProxy.batch_')
    def test_get_transaction_positive(self, ASPMock):
        tx_id = 'txid123'
        self.run_positive_case(
            ASPMock,
            'gettransaction',
            lambda w: w.get_transaction(tx_id),
            tx_id
        )

    @patch('bitcoinrpc.authproxy.AuthServiceProxy.batch_')
    def test_get_transactions_positive(self, ASPMock):
        label = 'abc123'
        count = 1
        offset = 0
        self.run_positive_case_json(
            ASPMock,
            'listtransactions',
            lambda w: w.get_transactions(
                label=label, count=count, offset=offset),
            label,
            count,
            offset
        )

    @patch('bitcoinrpc.authproxy.AuthServiceProxy.batch_')
    def test_get_transactions_since_positive(self, ASPMock):
        block_hash = 'hash123'
        self.run_positive_case_json(
            ASPMock,
            'listsinceblock',
            lambda w: w.get_transactions_since(block_hash),
            block_hash
        )

    @patch('bitcoinrpc.authproxy.AuthServiceProxy.batch_')
    def test_create_address_negative(self, ASPMock):
        label = 'abc1234'
        error = 'error1234'
        error_bin = 'error1234'
        code = 123
        error_message = 'Failed to create address for {}. Reason: {}. Code: {}'.format(
            label, error, code)
        self.run_negative_case(
            ASPMock,
            'getnewaddress',
            lambda w: w.create_address(label),
            error_bin,
            code,
            error_message,
            label
        )

    @patch('bitcoinrpc.authproxy.AuthServiceProxy.batch_')
    def test_get_balance_negative(self, ASPMock):
        error = 'error123'
        error_bin = 'error123'
        code = 123
        error_message = 'Failed to get balance. Reason: {}. Code: {}'.format(
            error, code)
        self.run_negative_case(
            ASPMock,
            'getbalance',
            lambda w: w.get_balance(),
            error_bin,
            code,
            error_message,
        )

    @patch('bitcoinrpc.authproxy.AuthServiceProxy.batch_')
    def test_get_transaction_negative(self, ASPMock):
        tx_id = 'txid123'
        error = 'error123'
        error_bin = 'error123'
        code = 123
        error_message = 'Failed to get transactiob by {}. Reason: {}. Code: {}'.format(
            tx_id, error, code)
        self.run_negative_case(
            ASPMock,
            'gettransaction',
            lambda w: w.get_transaction(tx_id),
            error_bin,
            code,
            error_message,
            tx_id
        )

    @patch('bitcoinrpc.authproxy.AuthServiceProxy.batch_')
    def test_get_transactions_negative(self, ASPMock):
        label = 'abc123'
        count = 1
        offset = 0
        error = 'error123'
        error_bin = 'error123'
        code = 123
        error_message = 'Failed to get transactions for {} where count is {} and offset is {}. Reason: {}. Code: {}'.format(
            label, count, offset, error, code)
        self.run_negative_case(
            ASPMock,
            'listtransactions',
            lambda w: w.get_transactions(
                label=label, count=count, offset=offset),
            error_bin,
            code,
            error_message,
            label,
            count,
            offset
        )

    @patch('bitcoinrpc.authproxy.AuthServiceProxy.batch_')
    def test_get_transactions_since_negative(self, ASPMock):
        block_hash = 'hash123'
        error = 'error123'
        error_bin = 'error123'
        code = 123
        error_message = 'Failed to get transactions since {}. Reason: {}. Code: {}'.format(
            block_hash, error, code)
        self.run_negative_case(
            ASPMock,
            'listsinceblock',
            lambda w: w.get_transactions_since(block_hash),
            error_bin,
            code,
            error_message,
            block_hash
        )

    def run_positive_case_json(self, ASPMock, command, command_run, *args):
        expected_result = {'test123': 'value123'}
        self.run_positive_case_internal(
            expected_result, '{"test123":"value123"}', ASPMock, command, command_run, *args)

    def run_positive_case(self, ASPMock, command, command_run, *args):
        self.run_positive_case_internal(
            'result123', 'result123', ASPMock, command, command_run, *args)

    def run_positive_case_internal(self, expected_result, result_bin, ASPMock, command, command_run, *args):
        wallet = self.wallet_factory
        ASPMock.return_value = (result_bin, b'')
        ASPMock.returncode = 123

        actual_result = command_run(wallet)

        temp_commands = list(args)
        temp_commands.insert(0, command)
        ASPMock.assert_called_once_with([temp_commands])
        if(type(expected_result) == dict and type(actual_result) != dict):
            actual_result = json.loads(actual_result)
        assert actual_result == expected_result

    def run_negative_case(self, ASPMock, command, command_run, error_bin, code, error_message, *args):
        wallet = self.wallet_factory

        ASPMock.return_value = (error_bin, b'')
        ASPMock.side_effect = JSONRPCException(
            {"code": code, "message": error_bin})
        ASPMock.returncode = code

        with pytest.raises(WalletException) as exc_info:
            command_run(wallet)
        temp_commands = list(args)
        temp_commands.insert(0, command)
        ASPMock.assert_called_once_with([temp_commands])
        assert error_message == exc_info.value.reason
