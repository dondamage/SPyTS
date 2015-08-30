
from . import SPyTSError

class TSDemuxError(SPyTSError.SPyTSError):
  def __init__(self, msg="TSDemuxError occured."):
    self.msg = msg

