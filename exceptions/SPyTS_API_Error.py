
class SPyTS_API_Error(Exception):
  def __init__(self, msg="SPyTS_API_Error occured."):
    self.msg = msg
