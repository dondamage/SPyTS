import unittest
from SPyTS.TSPacket import TSPacket
from SPyTS.exceptions.TSPacketError import TSPacketError

class TestTsPacket(unittest.TestCase):
  def setUp(self):
    # Create an test packet with AFC = 3 and AF_LENGTH = 4
    tsp_bytes = bytes.fromhex("47000130"+"04"+183*"00")
    self.tsp = TSPacket(tsp_bytes)
    
  def tearDown(self):
    pass
  
  def test_ctor(self):
    """Test the constructor of TSPacket for correct behavior."""
    tspkt_bytes = bytes.fromhex("47000100"+184*"00")
    tspkt = TSPacket(tspkt_bytes)
    
  def test_ctor_2(self):
    """Test the constructor of TSPacket when a wrong type is passed."""
    tsp_bytes = bytearray.fromhex("47000100"+184*"00")
    tsp = TSPacket(tsp_bytes)
    
  def test_ctor_3(self):
    """Test the constructor of TSPacket if insufficient number of bytes are passed."""
    tspkt_bytes = bytes.fromhex("470001")
    with self.assertRaises(TSPacketError) as cm:
      tspkt = TSPacket(tspkt_bytes)
  
  def test_get_sync(self):
    """Test TSPacket.sync_byte method."""
    sync_byte = self.tsp.sync_byte()
    assert sync_byte == 0x47
    
  def test_get_tei(self):
    """Test TSPacket.tei method."""
    tei = self.tsp.tei()
    assert tei == 0
    
  def test_get_pusi(self):
    """Test TSPacket.pusi method."""
    pusi = self.tsp.pusi()
    assert pusi == 0
    
  def test_get_tp(self):
    """Test TSPacket.tp method."""
    tp = self.tsp.tp()
    assert tp == 0
    
  def test_get_pid(self):
    """Test TSPacket.pid method."""
    pid = self.tsp.pid()
    assert pid == 1
    
  def test_get_tsc(self):
    """Test TSPacket.tsc method."""
    tsc = self.tsp.tsc()
    assert tsc == 0
    
  def test_get_afc(self):
    """Test TSPacket.afc method."""
    afc = self.tsp.afc()
    assert afc == 3
    
  def test_get_cc(self):
    """Test TSPacket.cc method."""
    cc = self.tsp.cc()
    assert cc == 0
    
  def test_get_header(self):
    """Test TSPacket.header method."""
    hdr = self.tsp.header()
    assert len(hdr) == 4
    
  def test_get_body(self):
    """Test TSPacket.body method."""
    body = self.tsp.body()
    assert len(body) == 184
    
  def test_has_payload(self):
    """Test TSPacket.has_payload method."""
    assert self.tsp.has_payload()
  
  def test_get_payload(self):
    """Test TSPacket.payload method."""
    payload = self.tsp.payload()
    assert len(payload) == 179
  
  def test_has_adaptation_field(self):
    """Test TSPacket.has_adaptation_field method."""
    assert self.tsp.has_adaptation_field()
        
  def test_get_adaptation_field(self):
    """Test TSPacket.adaptation_field method."""
    af = self.tsp.adaptation_field()
    assert len(af) == 4
    
if __name__ == '__main__':
  unittest.main()

