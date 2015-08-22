import TSPacket
import exceptions.TSPacketError as TSPacketError

class TSFileReader(object):
  """A class for reading of transport stream files."""
  SYNC_LOCK_BYTES = 3 # After N correct sync_bytes sync is achieved.
  SYNC_LOSS_BYTES = 2 # After N corrupted sync_bytes sync is lost.
  PKT_LEN = 188
  def __init__(self, file=None):
    self._fd = None
    self.closed = True
    self._pos = 0
    self._iterpos = 0
    if file is not None:
      self.open(file)
  def __iter__(self):
    self._iterpos = 0
    return self
  def __next__(self):
    try:
      tp = self.read()
    except Exception as e:
      raise StopIteration
    return tp
  def open(self, file):
    """Open file for reading."""
    if self.closed:
      if isinstance(file, str):
        try:
          self._fd = open(file, "rb")
        except Exception as e:
          raise e
        self.closed = False
        self._pos = 0
        self.resync()
        return True
      else:
        raise TSFileReaderError("Invalid file name. Must provide a string.")
    else:
      raise TSFileReaderError("There is already a file open.")
  def reopen(self):
    """Same as open, but will restore the previous file pointer."""
    if self.closed:
      try:
        self._fd = open(file, "rb")
      except Exception as e:
        raise e
      self.closed = False
      self._fd.seek(self._pos)
      return True
    else:
      raise TSFileReaderError("There is already a file open.")
  def resync(self):
    """Resynchronize to the file."""
    sync = False
    sync_pos = 0
    chunk_size = (TSFileReader.SYNC_LOCK_BYTES - 1) * PKT_LEN + 1
    tmp = self._fd.peek(chunk_size)
    while len(tmp) == chunk_size:
      for pos in range(len(tmp)):
        if tmp[pos] == TSPacket._SYNC_BYTE:
          for i in range(1, TSFileReader.SYNC_LOCK_BYTES + 1):
            if tmp[pos + i * TSPacket._LENGTH] != TSPacket._SYNC_BYTE:
              continue
          sync_pos += pos
          sync = True
          break
      sync_pos += chunk_size
      self._fd.seek(self._fd.tell() + chunk_size)
      tmp = self._fd.peek(chunk_size)
    self._fd.seek(sync_pos)
    self._pos = sync_pos
    return sync
  def read(self):
    """Read one TSPacket and return it."""
    tp = TSPacket.TSPacket(self._fd.read(PKT_LEN))
    return tp
  def read_raw(self):
    """Read one raw TS packet and return it."""
    return self._fd.read(PKT_LEN)
  def close(self):
    """Close the current file."""
    if self.closed:
      raise TSFileReaderError("Failed to close file. File already closed.")
    else:
      self._fd.close()
      self.closed = True
      return True
  def tell(self):
    """Return current file pointer."""
    pos = self._fd.tell()
    if pos == self._pos:
      return pos
    else:
      raise TSFileReaderError("TSFileReader is out of sync.")
  def seek(self, pos):
    """Move file pointer to given position."""
    try: self._fd.seek(pos)
    except Exception as e: raise e
    self._pos = pos
    return self._pos
