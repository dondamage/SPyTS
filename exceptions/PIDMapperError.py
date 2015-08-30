
from . import SPyTSError

class PIDMapperError(SPyTS_API_Error.SPyTSError):
  def __init__(self, msg="PIDMapperError occured."):
    self.msg = msg

