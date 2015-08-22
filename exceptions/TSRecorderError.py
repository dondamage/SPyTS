TSMuxErrorfrom . import SPyTS_API_Error

class TSRecorderError(SPyTS_API_Error.SPyTS_API_Error):
  def __init__(self, msg="TSRecorderError occured."):
    self.msg = msg
