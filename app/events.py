import asyncio
from app.settings import contract, w3, minimum_confirmations

suscriptors = []


def suscribe(address):
    suscriptors.append(address)


def event_action(event):
    """
    This function can be used to do something with the event (e.g. send an email)
    """
    print(event)


async def handle_event(event):
    if event.event != "DelegateProduct" or event.args.newOwner in suscriptors:
        # check every 3 seconds if it has the minimum confirmations
        while not has_min_confirmations(event.blockNumber):
            await asyncio.sleep(3)
        event_action(event)


def has_min_confirmations(transaction_block_number):
    return w3.eth.block_number - transaction_block_number >= minimum_confirmations


async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            asyncio.create_task(handle_event(event))
        await asyncio.sleep(poll_interval)


def listen_event(event_filter):
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(log_loop(event_filter, 2)))
    finally:
        loop.close()


def listen_new_products():
    new_product_event_filter = contract.events.NewProduct.createFilter(
        fromBlock="latest"
    )
    listen_event(new_product_event_filter)


def listen_delegated_products():
    delegated_product_event_filter = contract.events.DelegateProduct.createFilter(
        fromBlock="latest"
    )
    listen_event(delegated_product_event_filter)


def listen_accepted_products():
    accepted_product_event_filter = contract.events.AcceptProduct.createFilter(
        fromBlock="latest"
    )
    listen_event(accepted_product_event_filter)
