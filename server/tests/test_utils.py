import pytest
import re
from unittest import TestCase, mock
from collections import namedtuple
from utils import get_mac, get_interface, subnet_from_ifaddr, darwin_iface, linux_iface

@pytest.fixture
def ifaddr():
  '''Returns a string representing a valid IP address'''
  return '255.255.255.0'

@pytest.fixture
def subnet():
  '''Returns a string representing an IP address with a wildcard in the last octet instead of an integer'''
  return '255.255.255.*'

@pytest.fixture
def darwin_netif_list():
  '''Returns a list of Darwin network interface names'''
  return ['lo','en','p2p','stf','gif','bridge','utun','XHC','awdl','vboxnet']

def test_subnet_from_ifaddr(ifaddr, subnet):
  '''Check that subnet_from_ifaddr() returns the expected subnet'''
  assert subnet_from_ifaddr(ifaddr) == subnet

def test_darwin_read_routes(monkeypatch):
  '''Check that read_routes() is called and parsed table values'''
  def mockreturn():
    '''Returns a route table like the one returned by Scapy's read_routes method'''
    data = [
      (0, 0, '192.168.7.1', 'en0', '192.168.7.190', 1), 
      (2130706432, 4278190080, '0.0.0.0', 'lo0', '127.0.0.1', 1)
    ]
    return data
  monkeypatch.setattr('utils.read_routes', mockreturn)
  x = darwin_iface()
  assert len(x) == 3
  assert 7 <= len(x['gw']) <= 15 and x['gw'].count('.') == 3
  assert 7 <= len(x['ifaddr']) <= 15 and x['ifaddr'].count('.') == 3
  assert x['gw'] is not x['ifaddr']

def test_get_interface_darwin(monkeypatch):
  '''Check that when platform.system() returns Darwin, get_interface() should call darwin_iface()'''
  def mockreturn():
    return 'Darwin'
  monkeypatch.setattr('utils.platform.system', mockreturn)
  x = get_interface()
  assert x == darwin_iface()

def test_get_interface_linux(monkeypatch):
  '''Check that when platform.system() returns Linux, get_interface() should call linux_iface()'''
  def mockreturn():
    return 'Linux'
  monkeypatch.setattr('utils.platform.system', mockreturn)
  x = get_interface()
  assert x == linux_iface()

class TestMockScapySr(TestCase):
  @mock.patch('utils.sr')
  def test_scapy_sr(self, mocked_scapy_sr):
    '''Mock Scapy's sr() return and check that packet parsing returns the expected MAC address'''
    arp_response = namedtuple('arp_response', 'op hwdst pdst hwtype ptype hwlen plen hwsrc psrc')
    responses = [
      arp_response(op='who-has', hwdst='ff:ff:ff:ff:ff:ff', pdst='192.168.7.189', hwtype='', ptype='', hwlen='', plen='', hwsrc='', psrc=''),
      arp_response(op='is-at', hwdst='60:03:08:8c:44:72', pdst='192.168.7.190', hwtype='0x1', ptype='0x800', hwlen=6, plen=4, hwsrc='4c:57:ca:e9:b0:83', psrc='192.168.7.189')]
    unanswered_tuple = ((),)
    responded_tuple = (responses, ())
    mocked_scapy_sr.return_value = (responded_tuple, unanswered_tuple)
    resp, unans = mocked_scapy_sr.return_value
    x = get_mac('192.168.7.189')
    assert x == '4c:57:ca:e9:b0:83'

# TODO: This test fails on Darwin
# def test_get_interface_windows(monkeypatch):
#   def mockreturn():
#     return 'Windows'
#   monkeypatch.setattr('utils.platform.system', mockreturn)
#   x = get_interface()
#   assert x == win_iface()

class TestMockPlatformCalls(TestCase):
  @mock.patch('utils.platform')
  def test_get_interface_platform_calls(self, mocked_platform):
    '''Check that get_interface() calls platform.system() 3 times'''
    get_interface()
    assert mocked_platform.system.call_count == 3

  @mock.patch('utils.read_routes')
  def test_darwin_calls_read_routes(self, mocked_read_routes):
    '''Check that darwin_iface() calls read_routes() once'''
    darwin_iface()
    mocked_read_routes.assert_called_once()

  @mock.patch('utils.get_if_list')
  def test_linux_calls_get_if_list(self, mocked_get_if_list):
    '''Check that linux_iface() calls get_if_list() once'''
    linux_iface()
    mocked_get_if_list.assert_called_once()

  # TODO: This test fails on Darwin; removed `from utils import show_interfaces` to run tests
  # @mock.patch('utils.show_interfaces')
  # def test_win_calls_show_interfaces(self, mocked_show_interfaces):
  #   win_iface()
  #   mocked_show_interfaces.assert_called_once()
