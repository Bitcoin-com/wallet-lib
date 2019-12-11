from wallet_lib import WalletFactory
from wallet_lib.adapters import RPCAdapter
from rpc_wallet_base import RPCWalletBase

from unittest import TestCase
from unittest.mock import patch


class BTCWalletTest(RPCWalletBase, TestCase):

    def setUp(self):
        self.rpc_adapter = RPCAdapter('user', 'password', '127.0.0.1', '8332')
        self.wallet_factory = WalletFactory().get('BTC', self.rpc_adapter)

    @patch('bitcoinrpc.authproxy.AuthServiceProxy.batch_')
    def test_get_addresses_positive(self, ASPMock):
        label = 'abc123'
        self.run_positive_case_json(
            ASPMock,
            'getaddressesbylabel',
            lambda w: w.get_addresses(label),
            label
        )

    @patch('bitcoinrpc.authproxy.AuthServiceProxy.batch_')
    def test_get_addresses_negative(self, ASPMock):
        label = 'abc123'
        error = 'error123'
        error_bin = 'error123'
        code = 123
        error_message = 'Failed to get addresses by {}. Reason: {}. Code: {}'.format(
            label, error, code)
        self.run_negative_case(
            ASPMock,
            'getaddressesbylabel',
            lambda w: w.get_addresses(label),
            error_bin,
            code,
            error_message,
            label
        )

    @patch('bitcoinrpc.authproxy.AuthServiceProxy.batch_')
    def test_send_negative(self, ASPMock):
        sender = 's123'
        recipient = 'r123'
        amount = 1
        error = 'error123'
        error_bin = 'error123'
        code = 123
        error_message = 'Failed to send {} to {}. Reason: {}. Code: {}'.format(
            amount, recipient, error, code)
        self.run_negative_case(
            ASPMock,
            'sendtoaddress',
            lambda w: w.send(
                sender=sender, recipient=recipient, amount=amount),
            error_bin,
            code,
            error_message,
            recipient,
            str(amount)
        )
