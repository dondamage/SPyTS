
from . import SPyTSError

class TSAnalyserError(SPyTSError.SPyTSError):
  def __init__(self, msg="TSAnalyserError occured."):
    self.msg = msg

