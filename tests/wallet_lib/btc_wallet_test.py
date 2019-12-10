from wallet_lib import WalletFactory
from wallet_lib.adapters import CMDAdapter
from wallet_base import WalletBase

from unittest import TestCase
from unittest.mock import patch


class BTCWalletTest(WalletBase, TestCase):

    def setUp(self):
        self.cmd_adapter = CMDAdapter('bitcoin-cli')
        self.wallet_factory = WalletFactory().get('BTC', self.cmd_adapter)

    @patch('subprocess.Popen')
    def test_get_addresses_positive(self, PopenMock):
        label = 'abc123'
        self.run_positive_case_json(
            PopenMock,
            lambda w: w.get_addresses(label),
            'getaddressesbylabel',
            label
        )

    @patch('subprocess.Popen')
    def test_get_addresses_negative(self, PopenMock):
        label = 'abc123'
        error = 'error123'
        error_bin = b'  error123  '
        code = 123
        error_message = 'Failed to get addresses by {}. Reason: {}. Code: {}'.format(
            label, error, code)
        self.run_negative_case(
            PopenMock,
            lambda w: w.get_addresses(label),
            error_bin,
            code,
            error_message,
            'getaddressesbylabel',
            label
        )

    @patch('subprocess.Popen')
    def test_send_negative(self, PopenMock):
        sender = 's123'
        recipient = 'r123'
        amount = 1
        error = 'error123'
        error_bin = b'  error123  '
        code = 123
        error_message = 'Failed to send {} to {}. Reason: {}. Code: {}'.format(
            amount, recipient, error, code)
        self.run_negative_case(
            PopenMock,
            lambda w: w.send(
                sender=sender, recipient=recipient, amount=amount),
            error_bin,
            code,
            error_message,
            'sendtoaddress',
            recipient,
            str(amount)
        )
