
from . import SPyTSError

class TSPlayerError(SPyTSError.SPyTSError):
  def __init__(self, msg="TSPlayerError occured."):
    self.msg = msg

