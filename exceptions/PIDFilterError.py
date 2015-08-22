from . import SPyTS_API_Error

class PIDFilterError(SPyTS_API_Error.SPyTS_API_Error):
  def __init__(self, msg="PIDFilterError occured."):
    self.msg = msg
