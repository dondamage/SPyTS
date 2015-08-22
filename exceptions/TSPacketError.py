from . import SPyTS_API_Error

class TSPacketError(SPyTS_API_Error.SPyTS_API_Error):
  def __init__(self, msg="TSPacketError occured."):
    self.msg = msg
