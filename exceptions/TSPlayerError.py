from . import SPyTS_API_Error

class TSPlayerError(SPyTS_API_Error.SPyTS_API_Error):
  def __init__(self, msg="TSPlayerError occured."):
    self.msg = msg
