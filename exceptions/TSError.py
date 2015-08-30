
from . import SPyTSError

class TSError(SPyTSError.SPyTSError):
  def __init__(self, msg="TSError occured."):
    self.msg = msg

