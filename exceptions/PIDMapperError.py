from . import SPyTS_API_Error

class PIDMapperError(SPyTS_API_Error.SPyTS_API_Error):
  def __init__(self, msg="PIDMapperError occured."):
    self.msg = msg
