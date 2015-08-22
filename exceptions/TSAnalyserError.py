from . import SPyTS_API_Error

class TSAnalyserError(SPyTS_API_Error.SPyTS_API_Error):
  def __init__(self, msg="TSAnalyserError occured."):
    self.msg = msg
