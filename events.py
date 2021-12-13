import asyncio
from settings import contract

suscriptors = []

def suscribe(address):
    suscriptors.append(address)

def handle_event(event):
    if event.event == 'DelegateProduct':
        if event.args.newOwner in suscriptors:
            print(event)
    else:
        print(event)

async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(poll_interval)

def listen_event(event_filter):    
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)
            )
        )
    finally:
        loop.close()

def listen_new_products():
    new_product_event_filter = contract.events.NewProduct.createFilter(fromBlock='latest')
    listen_event(new_product_event_filter)

def listen_delegated_products():
    delegated_product_event_filter = contract.events.DelegateProduct.createFilter(fromBlock='latest')
    listen_event(delegated_product_event_filter)

def listen_accepted_products():
    accepted_product_event_filter = contract.events.AcceptProduct.createFilter(fromBlock='latest')
    listen_event(accepted_product_event_filter)
