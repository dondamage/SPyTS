from . import SPyTS_API_Error

class TSFileWriterError(SPyTS_API_Error.SPyTS_API_Error):
  def __init__(self, msg="TSFileWriterError occured."):
    self.msg = msg