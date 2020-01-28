from wallet_lib import ZMQNotifer
import time
import asyncio
# This should print out all txid for each transaction on the network in real-time
loop = asyncio.get_event_loop()
notifier = ZMQNotifer("tcp://127.0.0.1:28332", loop=loop, verbose=True)
notifier.add_callback(ZMQNotifer.TOPIC_TXID, lambda tx, _: print(tx))
notifier.add_error_callback(lambda tx, _: print(tx))

# notifier.add_callback(ZMQNotifer.TOPIC_BLOCKHASH, lambda bh, _: print(bh))
# notifier.add_callback(ZMQNotifer.TOPIC_RAWBLOCK, lambda blk, _: print(blk))

notifier.start()
notifier.stop()