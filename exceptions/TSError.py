from . import SPyTS_API_Error

class TSError(SPyTS_API_Error.SPyTS_API_Error):
  def __init__(self, msg="TSError occured."):
    self.msg = msg