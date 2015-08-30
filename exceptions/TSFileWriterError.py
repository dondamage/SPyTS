
from . import SPyTSError

class TSFileWriterError(SPyTSError.SPyTSError):
  def __init__(self, msg="TSFileWriterError occured."):
    self.msg = msg

