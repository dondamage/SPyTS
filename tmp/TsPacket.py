import TsPacketError

class TsPacket(object):
  """
  A wrapper class to represent an MPEG2-TS packet.
  """
  TS_PKT_LEN_188 = 188
  TS_PKT_LEN_204 = 204
  def __init__(self, pkt):
    if isinstance(pkt, bytes):
      if len(pkt) in (TsPacket.TS_PKT_LEN_188, TsPacket.TS_PKT_LEN_204):
        self._content = pkt
        self._header = self._content[:4]
        self._payload = self._content[4:]
      else:
        raise TsPacketError.TsPacketError("Invalid length of bytes object.")
    else:
      raise TypeError("Argument must be a bytes object.")
  
  def _bytes_to_int(self, b, endianness="big"):
    return int.from_bytes(b, endianness)
  
  def get_header(self):
    """Return only the header."""
    return self._header
  
  def get_payload(self):
    """Return only the payload."""
    return self._payload
  
  def get_sync(self):
    """Return sync byte."""
    sync = self._header[0]
    return sync
  
  def get_tei(self):
    """Return TEI flag."""
    tei = (self._bytes_to_int(self._header[1:1+1]) & 0x80) >> 7
    return tei
  
  def get_pusi(self):
    """Return PUSI flag."""
    pusi = (self._bytes_to_int(self._header[1:1+1]) & 0x40) >> 6
    return pusi
  
  def get_tp(self):
    """Return TP flag."""
    tp = (self._bytes_to_int(self._header[1:1+1]) & 0x20) >> 5
    return tp
  
  def get_pid(self):
    """Return PID."""
    pid = (self._bytes_to_int(self._header[1:2+1]) & 0x1FFF) >> 0
    return pid
  
  def get_tsc(self):
    """Return TSC."""
    tsc = (self._bytes_to_int(self._header[3:3+1]) & 0xC0) >> 6
    return tsc
  
  def get_afc(self):
    """Return AFC."""
    afc = (self._bytes_to_int(self._header[3:3+1]) & 0x30) >> 4
    return afc
  
  def get_cc(self):
    """Return CC."""
    cc = (self._bytes_to_int(self._header[3:3+1]) & 0x0F)
    return cc
  
  def get_af(self):
    """Return the adaptation field as an immutable bytes object, if present."""
    if self.get_afc() >= 2:
      af_len = self._payload[0]
      if af_len > 0:
        return bytes(self._payload[1:af_len+2])
      else:
        return bytes(0)
    else:
      return None
  
  def get_pcr_flag(self):
    """Return value of the PCR flag of TS packet pkt, if present."""
    pcr_flag = None
    if self.get_afc() >= 2:
      af = self.get_af()
      af_length = af[0]
      if af_length > 0:
        pcr_flag = (af[1] & 0x10) >> 4
    return pcr_flag
  
  def get_pcr(self):
    """Return value of the PCR field of TS packet pkt, if present."""
    pcr = None
    if (self.get_pcr_flag == 1):
      pcr_base = int.from_bytes((self._content[1:6] & 0xFFFFFFFF80) >> 7, "big")
      pcr_reserved = int.from_bytes((self._content[5:6] & 0x7E) >> 1, "big")
      pcr_extension = int.from_bytes((self._content[5:7] & 0x1FF), "big")
      pcr = pcr_base*300 + pcr_extension
    return pcr
    