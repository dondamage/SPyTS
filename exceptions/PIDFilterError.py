
from . import SPyTSError

class PIDFilterError(SPyTSError.SPyTSError):
  def __init__(self, msg="PIDFilterError occured."):
    self.msg = msg

