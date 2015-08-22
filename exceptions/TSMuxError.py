from . import SPyTS_API_Error

class TSMuxError(SPyTS_API_Error.SPyTS_API_Error):
  def __init__(self, msg="TSMuxError occured."):
    self.msg = msg
