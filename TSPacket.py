import binascii # hexlify()
import io # BufferedReader
import struct # unpack()

import TSFileReader
import exceptions.TSPacketError as TSPacketError

class TSPacket(object):
  """A class representing an MPEG2 transport stream packet."""
  _LENGTH = 188
  _SYNC_BYTE = bytes.fromhex("47")
  _NULL_PKT_HDR = bytes.fromhex("471FFFFF")
  def __init__(self, init=None):
    """A TSPacket can be initialized in several ways:
       1. init is None. No initialization is performed.
       2. init is a file descriptor with mode 'rb'.
          The appropriate number of bytes will be read from the file to
          initialize the TSPacket object.
       3. init is a TSFileReader object.
          One TSPacket is read from the TSFileReader and used to
          initialize the TSPacket object.
       4. init is a bytes object of appropriate length.
       5. init is a bytearray object of appropriate length.
       """
    if init == None:
      # self.raw_pkt = None
      self.raw_pkt = bytearray(b''.join([TSPacket._NULL_PKT_HDR,
        bytes(TSPacket._LENGTH - len(TSPacket._NULL_PKT_HDR))]))
    elif isinstance(init, io.BufferedReader):
      if "b" in init.mode and init.readable():
        raw_pkt = init.read(188)
        if len(raw_pkt) == TSPacket._LENGTH:
          self.raw_pkt = bytearray(raw_pkt)
        else:
          raise TSPacketError.TSPacketError("A TSPacket can not be constructed"
            +" from the given object.")
      else:
        raise TSPacketError.TSPacketError("A TSPacket can not be constructed"
          +" from the given object.")
    elif isinstance(init, TSFileReader.TSFileReader):
      tp = init.read(1)
      if tp is not None:
        self.raw_pkt = tp.raw_pkt.copy()
      else:
        raise TSPacketError.TSPacketError("A TSPacket can not be constructed"
          +" from the given object.")
    elif isinstance(init, bytes):
      if len(init) == TSPacket._LENGTH:
        self.raw_pkt = bytearray(init)
      else:
        raise TSPacketError.TSPacketError("A TSPacket can not be constructed"
          +" from the given object.")
    elif isinstance(init, bytearray):
      if len(init) == TSPacket._LENGTH:
        self.raw_pkt = init.copy()
      else:
        raise TSPacketError.TSPacketError("A TSPacket can not be constructed"
          +" from the given object.")
    else:
      raise TypeError("A TSPacket can not be constructed from this type.")
  def __iter__(self):
    self.__iterpos = 0
    return self
  def __next__(self):
    if self.__iterpos < TSPacket._LENGTH:
      pos = self.__iterpos
      self.__iterpos += 1
      return self.raw_pkt[pos]
    else:
      raise StopIteration
  def __repr__(self):
    """Return string representation of the TSPacket object."""
    # TODO: get real payload length.
    repr = "TSPacket: header {0}, payload length {1}.".format(
      binascii.hexlify(self.raw_pkt[0:4]), len(self.raw_pkt))
    return repr
  def __str__(self):
    """Stringify the TSPacket object."""
    return binascii.hexlify(self.raw_pkt)
  def header(self):
    """Return only the packet header."""
    return self.raw_pkt[0:4]
  def body(self):
    """Return only the packet body."""
    return self.raw_pkt[4:]
  def sync_byte(self):
    """Return sync byte."""
    return self.raw_pkt[0]
  def tei(self):
    """Return TEI flag."""
    return (self.raw_pkt[1] & 0x80) >> 7
  def pusi(self):
    """Return PUSI flag."""
    return (self.raw_pkt[1] & 0x40) >> 6
  def tp(self):
    """Return TP flag."""
    return (self.raw_pkt[1] & 0x20) >> 5
  def pid(self):
    """Return PID."""
    (tmp,) = struct.unpack("!H", self.raw_pkt[1:3])
    return tmp & 0x1FFF
  def tsc(self):
    """Return TSC."""
    return (self.raw_pkt[3] & 0xC0) >> 6
  def afc(self):
    """Return AFC."""
    return (self.raw_pkt[3] & 0x30) >> 4
  def cc(self):
    """Return CC."""
    return (self.raw_pkt[3] & 0x0F)
  def has_sync_byte(self):
    """Return True if the sync byte is correct, return False otherwise."""
    return self.sync_byte() == int.from_bytes(TSPacket._SYNC_BYTE, "big")
  def has_payload(self):
    """Return True if the packet contains payload, return False otherwise."""
    return self.afc() & 0x1 != 0
  def payload(self):
    """Return the packet payload."""
    if self.has_payload():
      if self.has_adaptation_field():
        af_len = self.body()[0]
        return self.body[af_len+1:]
      else:
        return self.body()
    else:
      return None
  def has_adaptation_field(self):
    """Return True if the packet contains an adaptation field, return False otherwise."""
    return self.afc() & 0x2 != 0
  def adaptation_field(self):
    """Return the adaptation field."""
    if self.has_adaptation_field():
      af_len = self.body()[0]
      return self.body()[:af_len]
    else:
      return None
