import pytest

from unittest import TestCase
from unittest.mock import patch

from wallet_lib import BCHWallet
from wallet_lib.wallet_exceptions import WalletException

class BCHWalletTest(TestCase):

    @patch('subprocess.Popen')
    def test_create_address(self, PopenMock):
        label = 'abc123'
        expected_result = 'result123'
        
        wallet = BCHWallet()
        self.assertEqual('bitcoin-cli', wallet.program_name)
        
        mock_proc = PopenMock.return_value
        mock_proc.returncode = 123
        mock_proc.communicate.return_value = (b'  result123  ', b'')

        actual_result = wallet.create_address(label)
        PopenMock.assert_called_once_with(['bitcoin-cli', 'getnewaddress', label], stdout=-1, stderr=-1)
        self.assertEqual(expected_result, actual_result)

    @patch('subprocess.Popen')
    def test_create_address_negative(self, PopenMock):
        label = 'abc123'
        error = 'error123'
        error_bin = b'  error123  '
        code = 123
        error_message = 'Failed to create address for {}. Reason: {}. Code: {}'.format(label, error, code)
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
    def test_get_addresses_negative(self, PopenMock):
        label = 'abc123'
        error = 'error123'
        error_bin = b'  error123  '
        code = 123
        error_message = 'Failed to get addresses by {}. Reason: {}. Code: {}'.format(label, error, code)
        self.run_negative_case(
            PopenMock,
            lambda w: w.get_addresses(label),
            error_bin,
            code,
            error_message,
            'getaddressesbyaccount',
            label
        )

    @patch('subprocess.Popen')
    def test_get_balance_negative(self, PopenMock):
        error = 'error123'
        error_bin = b'  error123  '
        code = 123
        error_message = 'Failed to get balance. Reason: {}. Code: {}'.format(error, code)
        self.run_negative_case(
            PopenMock,
            lambda w: w.get_balance(),
            error_bin,
            code,
            error_message,
            'getbalance'
        )

    @patch('subprocess.Popen')
    def test_get_transaction_negative(self, PopenMock):
        tx_id = 'txid123'
        error = 'error123'
        error_bin = b'  error123  '
        code = 123
        error_message = 'Failed to get transactiob by {}. Reason: {}. Code: {}'.format(tx_id, error, code)
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
    def test_get_transactions_negative(self, PopenMock):
        label = 'abc123'
        count = 1
        offset = 0
        error = 'error123'
        error_bin = b'  error123  '
        code = 123
        error_message = 'Failed to get transactions for {} where count is {} and offset is {}. Reason: {}. Code: {}'.format(label, count, offset, error, code)
        self.run_negative_case(
            PopenMock,
            lambda w: w.get_transactions(label=label, count=count, offset=offset),
            error_bin,
            code,
            error_message,
            'listtransactions',
            label,
            str(count),
            str(offset)
        )

    @patch('subprocess.Popen')
    def test_send_negative(self, PopenMock):
        sender = 's123'
        recipient = 'r123'
        amount = 1
        error = 'error123'
        error_bin = b'  error123  '
        code = 123
        error_message = 'Failed to send {} from {} to {}. Reason: {}. Code: {}'.format(amount, sender, recipient, error, code)
        self.run_negative_case(
            PopenMock,
            lambda w: w.send(sender=sender, recipient=recipient, amount=amount),
            error_bin,
            code,
            error_message,
            'sendfrom',
            sender,
            recipient,
            str(amount)
        )

    @patch('subprocess.Popen')
    def test_get_transactions_since_negative(self, PopenMock):
        block_hash = 'hash123'
        error = 'error123'
        error_bin = b'  error123  '
        code = 123
        error_message = 'Failed to get transactions since {}. Reason: {}. Code: {}'.format(block_hash, error, code)
        self.run_negative_case(
            PopenMock,
            lambda w: w.get_transactions_since(block_hash),
            error_bin,
            code,
            error_message,
            'listsinceblock',
            block_hash
        )

    def run_negative_case(self, PopenMock, command_run, error_bin, code, error_message, *args):        
        wallet = BCHWallet()
        self.assertEqual('bitcoin-cli', wallet.program_name)
        
        mock_proc = PopenMock.return_value
        mock_proc.returncode = code
        mock_proc.communicate.return_value = (b'', error_bin)

        with pytest.raises(WalletException) as exc_info:
            command_run(wallet)

        PopenMock.assert_called_once_with(['bitcoin-cli', *args], stdout=-1, stderr=-1)
        self.assertEqual(error_message, exc_info.value.reason)
