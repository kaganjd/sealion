import pytest
from utils import subnet_from_ifaddr

@pytest.fixture
def ifaddr():
  '''Returns an string representing a valid IP address'''
  return '255.255.255.0'

def test_validate_ifaddr(ifaddr):
  assert 7 <= len(ifaddr) <= 15 and ifaddr.count('.') == 3

def test_subnet_from_ifaddr(ifaddr):
  subnet_from_ifaddr(ifaddr)
  assert '255.255.255.*'
