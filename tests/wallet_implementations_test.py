import pytest
from unittest.mock import patch, Mock

from wallet_lib import BCHWallet, BTCWallet, DASHWallet, ZECWallet
from wallet_lib.wallet_exceptions import WalletException

wallet_classes = [BCHWallet, BTCWallet, DASHWallet, ZECWallet]

@patch('wallet_lib.wallet_base.WalletBase')
def test_send_invalid(MockWalletBase):
    for wallet_class in wallet_classes:
        wallet = wallet_class(MockWalletBase)
        with pytest.raises(WalletException) as excinfo:
            wallet.send(None, 100)
        assert "Address is invalid" in str(excinfo)
        with pytest.raises(WalletException) as excinfo:
            wallet.send("recipient", 0)
        assert "Amount should be greater than 0" in str(excinfo)

#Check reason and code in run command failure
@patch('wallet_lib.wallet_base.WalletBase')
def test_fail_run(MockWalletBase):

    error = "Something went wrong test"
    code = 322

    def adapter_fail(*args):
        mock = Mock()
        mock.error = "Something went wrong test"
        mock.code = 322
        return mock

    MockWalletBase.run = adapter_fail

    for wallet_class in wallet_classes:
        with pytest.raises(WalletException) as excinfo:
            wallet = wallet_class(MockWalletBase)
            wallet.run("command")
            assert error == excinfo.reason
            assert code == excinfo.code

#Generic adapter returns value
#(This is for the simpler commands that don't need logic to test)
def pass_test(MockWalletBase, method_name, args):

    def adapter_run(*args):
        mock = Mock()
        mock.result = "test"
        mock.error = None
        return mock

    MockWalletBase.run = adapter_run

    for wallet_class in wallet_classes:
        wallet = wallet_class(MockWalletBase)
        method = getattr(wallet, method_name)
        return_value = method(*args)
        assert return_value == "test"

@patch('wallet_lib.wallet_base.WalletBase')
def test_pass_all_commands(MockWalletBase):

    pass_test(MockWalletBase, "create_address", ("label",))
    pass_test(MockWalletBase, "get_transaction", ("tx_id",))
    pass_test(MockWalletBase, "send", ("recipient", 100))
    pass_test(MockWalletBase, "run", ("command", ()))

    def fake_json_loads(val):
        return val

    with patch('json.loads', fake_json_loads):
        pass_test(MockWalletBase, "get_balance", ())
        pass_test(MockWalletBase, "get_transactions", (None, 25, 0))
        pass_test(MockWalletBase, "get_transactions_since", ("block_hash",))


#Generic adapter fails to run
def fail_test(MockWalletBase, method_name, args):

    def adapter_fail(*args):
        mock = Mock()
        mock.error = "Something went wrong test"
        return mock

    MockWalletBase.run = adapter_fail

    for wallet_class in wallet_classes:
        with pytest.raises(WalletException) as excinfo:
            wallet = wallet_class(MockWalletBase)
            method = getattr(wallet, method_name)
            if len(args) == 0:
                method()
            else:
                method(*args)
        assert "Something went wrong test" in str(excinfo)

@patch('wallet_lib.wallet_base.WalletBase')
def test_fail_all_commands(MockWalletBase):
    fail_test(MockWalletBase, "create_address", ("",))
    fail_test(MockWalletBase, "get_balance", ())
    fail_test(MockWalletBase, "get_transaction", ("tx_id",))
    fail_test(MockWalletBase, "get_transactions", (None, 25, 0))
    fail_test(MockWalletBase, "send", ("recipient", 100))
    fail_test(MockWalletBase, "get_transactions_since", ("block_hash",))
