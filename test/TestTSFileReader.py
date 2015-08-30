
import unittest
import SPyTS.TSFileReader as TSFR
import SPyTS.exceptions.TSFileReaderError as TSFRE
import SPyTS.TSPacket as TSP

class TestTSFileReader(unittest.TestCase):
  def setUp(self):
    self.tsfr = TSFR.TSFileReader("test.ts")
    
  def tearDown(self):
    self.tsfr = None

