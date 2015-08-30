
from . import SPyTSError

class TSRecorderError(SPyTSError.SPyTSError):
  def __init__(self, msg="TSRecorderError occured."):
    self.msg = msg

