from . import SPyTS_API_Error

class TSFileReaderError(SPyTS_API_Error.SPyTS_API_Error):
  def __init__(self, msg="TSFileReaderError occured."):
    self.msg = msg