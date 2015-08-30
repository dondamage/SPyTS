
from SPyTS.exceptions.SPyTSError import SPyTSError

class TSPacketError(SPyTSError):
  def __init__(self, msg="TSPacketError occured."):
    self.msg = msg

