import pytest
import json
from unittest.mock import patch

from wallet_lib.wallet_exceptions import WalletException


class WalletBase:

    wallet_factory = None

    @patch('subprocess.Popen')
    def test_create_address_positive(self, PopenMock):
        label = 'abc123'
        self.run_positive_case(
            PopenMock,
            lambda w: w.create_address(label),
            'getnewaddress',
            label
        )

    @patch('subprocess.Popen')
    def test_create_address_negative(self, PopenMock):
        label = 'abc123'
        error = 'error123'
        error_bin = b'  error123  '
        code = 123
        error_message = 'Failed to create address for {}. Reason: {}. Code: {}'.format(
            label, error, code)
        self.run_negative_case(
            PopenMock,
            lambda w: w.create_address(label),
            error_bin,
            code,
            error_message,
            'getnewaddress',
            label
        )

    @patch('subprocess.Popen')
    def test_get_balance_positive(self, PopenMock):
        self.run_positive_case(
            PopenMock,
            lambda w: w.get_balance(),
            'getbalance'
        )

    @patch('subprocess.Popen')
    def test_get_balance_negative(self, PopenMock):
        error = 'error123'
        error_bin = b'  error123  '
        code = 123
        error_message = 'Failed to get balance. Reason: {}. Code: {}'.format(
            error, code)
        self.run_negative_case(
            PopenMock,
            lambda w: w.get_balance(),
            error_bin,
            code,
            error_message,
            'getbalance'
        )

    @patch('subprocess.Popen')
    def test_get_transaction_positive(self, PopenMock):
        tx_id = 'txid123'
        self.run_positive_case(
            PopenMock,
            lambda w: w.get_transaction(tx_id),
            'gettransaction',
            tx_id
        )

    @patch('subprocess.Popen')
    def test_get_transaction_negative(self, PopenMock):
        tx_id = 'txid123'
        error = 'error123'
        error_bin = b'  error123  '
        code = 123
        error_message = 'Failed to get transactiob by {}. Reason: {}. Code: {}'.format(
            tx_id, error, code)
        self.run_negative_case(
            PopenMock,
            lambda w: w.get_transaction(tx_id),
            error_bin,
            code,
            error_message,
            'gettransaction',
            tx_id
        )

    @patch('subprocess.Popen')
    def test_get_transactions_positive(self, PopenMock):
        label = 'abc123'
        count = 1
        offset = 0
        self.run_positive_case_json(
            PopenMock,
            lambda w: w.get_transactions(
                label=label, count=count, offset=offset),
            'listtransactions',
            label,
            str(count),
            str(offset)
        )

    @patch('subprocess.Popen')
    def test_get_transactions_negative(self, PopenMock):
        label = 'abc123'
        count = 1
        offset = 0
        error = 'error123'
        error_bin = b'  error123  '
        code = 123
        error_message = 'Failed to get transactions for {} where count is {} and offset is {}. Reason: {}. Code: {}'.format(
            label, count, offset, error, code)
        self.run_negative_case(
            PopenMock,
            lambda w: w.get_transactions(
                label=label, count=count, offset=offset),
            error_bin,
            code,
            error_message,
            'listtransactions',
            label,
            str(count),
            str(offset)
        )

    @patch('subprocess.Popen')
    def test_get_transactions_since_positive(self, PopenMock):
        block_hash = 'hash123'
        self.run_positive_case_json(
            PopenMock,
            lambda w: w.get_transactions_since(block_hash),
            'listsinceblock',
            block_hash
        )

    @patch('subprocess.Popen')
    def test_get_transactions_since_negative(self, PopenMock):
        block_hash = 'hash123'
        error = 'error123'
        error_bin = b'  error123  '
        code = 123
        error_message = 'Failed to get transactions since {}. Reason: {}. Code: {}'.format(
            block_hash, error, code)
        self.run_negative_case(
            PopenMock,
            lambda w: w.get_transactions_since(block_hash),
            error_bin,
            code,
            error_message,
            'listsinceblock',
            block_hash
        )

    def run_positive_case_json(self, PopenMock, command_run, *args):
        expected_result = {'test123': 'value123'}
        self.run_positive_case_internal(
            expected_result, b'  {"test123":"value123"}  ', PopenMock, command_run, *args)

    def run_positive_case(self, PopenMock, command_run, *args):
        self.run_positive_case_internal(
            'result123', b'  result123  ', PopenMock, command_run, *args)

    def run_positive_case_internal(self, expected_result, result_bin, PopenMock, command_run, *args):
        wallet = self.wallet_factory

        mock_proc = PopenMock.return_value
        mock_proc.returncode = 123
        mock_proc.communicate.return_value = (result_bin, b'')

        actual_result = command_run(wallet)
        PopenMock.assert_called_once_with(
            ['bitcoin-cli', *args], stdout=-1, stderr=-1)
        if(type(expected_result) == dict and type(actual_result) != dict):
            actual_result = json.loads(actual_result)
        assert expected_result == actual_result

    def run_negative_case(self, PopenMock, command_run, error_bin, code, error_message, *args):
        wallet = self.wallet_factory

        mock_proc = PopenMock.return_value
        mock_proc.returncode = code
        mock_proc.communicate.return_value = (b'', error_bin)

        with pytest.raises(WalletException) as exc_info:
            command_run(wallet)

        PopenMock.assert_called_once_with(
            ['bitcoin-cli', *args], stdout=-1, stderr=-1)
        assert error_message == exc_info.value.reason
