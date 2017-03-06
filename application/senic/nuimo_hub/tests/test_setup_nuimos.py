import pytest


@pytest.fixture
def url(route_url):
    return route_url('connected_nuimos')


def test_find_nuimo(browser, url):
    assert browser.get_json(url).json['connectedControllers'] == ['AA:BB:CC:DD:EE:FF']


@pytest.fixture
def no_such_nuimo(settings):
    settings['nuimo_mac_address_filepath'] = '/no/such/file'
    return settings


def test_get_scanned_wifi_empty(no_such_nuimo, browser, url):
    assert browser.get_json(url).json == []
