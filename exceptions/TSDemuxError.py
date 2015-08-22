from . import SPyTS_API_Error

class TSDemuxError(SPyTS_API_Error.SPyTS_API_Error):
  def __init__(self, msg="TSDemuxError occured."):
    self.msg = msg
