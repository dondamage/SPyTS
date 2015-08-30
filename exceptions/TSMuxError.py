
from . import SPyTSError

class TSMuxError(SPyTSError.SPyTSError):
  def __init__(self, msg="TSMuxError occured."):
    self.msg = msg

