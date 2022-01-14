from unittest.mock import patch
from app.events import *
from app.tests.fixtures import *


def test_suscribe():
    fake_address = "0x0000000000000000000000000000000000000000"
    assert len(suscriptors) == 0
    suscribe(fake_address)
    assert fake_address in suscriptors
    assert len(suscriptors) == 1


@pytest.mark.parametrize(
    "mock_minimum_confirmations, expected",
    [(9, True), (10, True), (11, False)],
    indirect=["mock_minimum_confirmations"],
)
@patch("app.events.w3.eth")
def test_has_min_confirmations(mock_eth, mock_minimum_confirmations, expected):
    mock_eth.block_number = 15
    assert has_min_confirmations(5) == expected


@patch("app.events.print")
def test_event_action(mock_print):
    event = "fake event"
    event_action(event)
    mock_print.assert_called_with(event)


@patch("app.events.listen_event")
def test_listen_new_products(mock_listen_event, mock_contract_events):
    listen_new_products()
    mock_listen_event.assert_called()


@patch("app.events.listen_event")
def test_listen_delegated_products(mock_listen_event, mock_contract_events):
    listen_delegated_products()
    mock_listen_event.assert_called()


@patch("app.events.listen_event")
def test_listen_accepted_products(mock_listen_event, mock_contract_events):
    listen_accepted_products()
    mock_listen_event.assert_called()
