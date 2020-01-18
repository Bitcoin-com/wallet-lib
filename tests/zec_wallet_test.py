import pytest
from unittest.mock import patch

from unittest import TestCase
from wallet_test_base import WalletTestBase


class ZECWalletTest(WalletTestBase, TestCase):

    @patch('wallet_lib.adapters.WalletAdapterBase.run')
    def test_create_address_positive(self, Mock):
        label = 'abc123'
        self.run_positive_case(
            Mock,
            lambda w: w.run('getnewaddress', label),
            'getnewaddress',
            label
        )

    @patch('wallet_lib.adapters.WalletAdapterBase.run')
    def test_get_balance_positive(self, Mock):
        self.run_positive_case(
            Mock,
            lambda w: w.run('z_getbalance'),
            'z_getbalance'
        )

    @patch('wallet_lib.adapters.WalletAdapterBase.run')
    def test_get_transaction_positive(self, Mock):
        tx_id = 'txid123'
        self.run_positive_case(
            Mock,
            lambda w: w.run('gettransaction', tx_id),
            'gettransaction',
            tx_id
        )

    @patch('wallet_lib.adapters.WalletAdapterBase.run')
    def test_get_transactions_positive(self, Mock):
        label = 'abc123'
        count = 1
        offset = 0
        self.run_positive_case_json(
            Mock,
            lambda w: w.run('listtransactions',
                            label, count, offset),
            'listtransactions',
            label,
            count,
            offset
        )

    @patch('wallet_lib.adapters.WalletAdapterBase.run')
    def test_get_transactions_since_positive(self, Mock):
        block_hash = 'hash123'
        self.run_positive_case_json(
            Mock,
            lambda w: w.run('listsinceblock',  block_hash),
            'listsinceblock',
            block_hash
        )

    @patch('wallet_lib.adapters.WalletAdapterBase.run')
    def test_create_address_negative(self, Mock):
        label = 'abc1234'
        error = 'error1234'
        error_bin = 'error1234'
        code = 123
        error_message = {'code': code, 'message': error}
        self.run_negative_case(
            Mock,
            lambda w: w.run('getnewaddress', label),
            error_bin,
            code,
            error_message,
            'getnewaddress',
            label
        )

    @patch('wallet_lib.adapters.WalletAdapterBase.run')
    def test_get_balance_negative(self, Mock):
        error = 'error123'
        error_bin = 'error123'
        code = 123
        error_message = {'code': code, 'message': error}
        self.run_negative_case(
            Mock,
            lambda w: w.run('z_getbalance'),
            error_bin,
            code,
            error_message,
            'z_getbalance'
        )

    @patch('wallet_lib.adapters.WalletAdapterBase.run')
    def test_get_transaction_negative(self, Mock):
        tx_id = 'txid123'
        error = 'error123'
        error_bin = 'error123'
        code = 123
        error_message = {'code': code, 'message': error}
        self.run_negative_case(
            Mock,
            lambda w: w.run('gettransaction', tx_id),
            error_bin,
            code,
            error_message,
            'gettransaction',
            tx_id
        )

    @patch('wallet_lib.adapters.WalletAdapterBase.run')
    def test_get_transactions_negative(self, Mock):
        label = 'abc123'
        count = 1
        offset = 0
        error = 'error123'
        error_bin = 'error123'
        code = 123
        error_message = {'code': code, 'message': error}
        self.run_negative_case(
            Mock,
            lambda w: w.run('listtransactions', label, count, offset),
            error_bin,
            code,
            error_message,
            'listtransactions',
            label,
            count,
            offset
        )

    @patch('wallet_lib.adapters.WalletAdapterBase.run')
    def test_get_transactions_since_negative(self, Mock):
        block_hash = 'hash123'
        error = 'error123'
        error_bin = 'error123'
        code = 123
        error_message = {'code': code, 'message': error}
        self.run_negative_case(
            Mock,
            lambda w: w.run('listsinceblock', block_hash),
            error_bin,
            code,
            error_message,
            'listsinceblock',
            block_hash
        )

    @patch('wallet_lib.adapters.WalletAdapterBase.run')
    def test_send_negative(self, Mock):
        sender = 's123'
        recipient = 'r123'
        amount = 1
        error = 'error123'
        error_bin = 'error123'
        code = 123
        error_message = {'code': code, 'message': error}
        self.run_negative_case(
            Mock,
            lambda w: w.run('sendtoaddress',
                            sender, recipient, amount),
            error_bin,
            code,
            error_message,
            'sendtoaddress',
            sender,
            recipient,
            amount
        )
