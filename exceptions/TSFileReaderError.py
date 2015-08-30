
from . import SPyTSError

class TSFileReaderError(SPyTSError.SPyTSError):
  def __init__(self, msg="TSFileReaderError occured."):
    self.msg = msg

