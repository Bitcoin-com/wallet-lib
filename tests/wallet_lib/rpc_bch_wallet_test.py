from wallet_lib import WalletFactory
from wallet_lib.adapters import RPCAdapter
from rpc_wallet_base import RPCWalletBase

from unittest import TestCase
from unittest.mock import patch


class BCHWalletTest(RPCWalletBase, TestCase):

    def setUp(self):
        self.rpc_adapter = RPCAdapter('user', 'password', '127.0.0.1', '8332')
        self.wallet_factory = WalletFactory().get('BCH', self.rpc_adapter)

    @patch('bitcoinrpc.authproxy.AuthServiceProxy.batch_')
    def test_get_addresses_positive(self, ASPMock):
        label = 'abc123'
        self.run_positive_case_json(
            ASPMock,
            'getaddressesbyaccount',
            lambda w: w.get_addresses(label),
            label
        )
