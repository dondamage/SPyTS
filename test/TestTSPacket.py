import unittest
import SPyTS_API.TsPacket as TsP
import exceptions.TsPacketError as TsPE

class TestTsPacket(unittest.TestCase):
  def setUp(self):
    tsp_bytes = bytes.fromhex("47000100"+184*"00")
    self.tsp = TsP.TsPacket(tsp_bytes)
    
  def tearDown(self):
    pass
  
  def test_ctor(self):
    """Test the constructor of TsPacket for correct behavior."""
    tspkt_bytes = bytes.fromhex("47000100"+184*"00")
    tspkt = TsP.TsPacket(tspkt_bytes)
    
  @unittest.expectedFailure
  def test_ctor_2(self):
    """Test the constructor of TsPacket when a wrong type is passed."""
    tsp_bytes = bytearray.fromhex("47000100"+184*"00")
    tsp = TsP.TsPacket(tsp_bytes)
    
  def test_ctor_3(self):
    """Test the constructor of TsPacket if insufficient number of bytes are passed."""
    tspkt_bytes = bytes.fromhex("470001")
    with self.assertRaises(TsPE.TsPacketError) as cm:
      tspkt = TsP.TsPacket(tspkt_bytes)
    
  def test_get_header(self):
    """Test TsPacket.get_header method."""
    hdr = self.tsp.get_header()
    assert len(hdr) == 4
    
  def test_get_payload(self):
    """Test TsPacket.get_payload method."""
    payld = self.tsp.get_payload()
    assert len(payld) == 184
  
  def test_get_sync(self):
    """Test TsPacket.get_sync method."""
    sync_byte = self.tsp.get_sync()
    assert sync_byte == 0x47
    
  def test_get_tei(self):
    """Test TsPacket.get_tei method."""
    tei = self.tsp.get_tei()
    assert tei == 0
    
  def test_get_pusi(self):
    """Test TsPacket.get_pusi method."""
    pusi = self.tsp.get_pusi()
    assert pusi == 0
    
  def test_get_tp(self):
    """Test TsPacket.get_tp method."""
    tp = self.tsp.get_tp(self)
    assert tp == 0
    
  def test_get_pid(self):
    """Test TsPacket.get_pid method."""
    pid = self.tsp.get_pid()
    assert pid == 1
    
  def test_get_tsc(self):
    """Test TsPacket.get_tsc method."""
    tsc = self.tsp.get_tsc()
    assert tsc == 0
    
  def test_get_afc(self):
    """Test TsPacket.get_afc method."""
    afc = self.tsp.get_afc()
    assert afc == 0
    
  def test_get_cc(self):
    """Test TsPacket.get_cc method."""
    cc = self.tsp.get_cc()
    assert cc == 0
    
  def test_get_af(self):
    """Test TsPacket.get_af method."""
    af = self.tsp.get_af()
    assert af is None
    
  def test_get_pcr_flag(self):
    """Test TsPacket.get_pcr_flag method."""
    pcr_flag = self.tsp.get_pcr_flag()
    assert pcr_flag is None
    
  def test_get_pcr(self):
    """Test TsPacket.get_pcr method."""
    pcr = self.tsp.get_pcr()
    assert pcr is None
    
if __name__ == '__main__':
  unittest.main()
  