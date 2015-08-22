class TSPacketStatistic(object):
    """A class to hold statistics information for a sequence of TSPackets."""
    def __init__(self):
      self.pkt_count = 0
      self.sync_byte_count = 0
      self.tei_count = 0
      self.pusi_count = 0
      self.tp_count = 0
      self.tsc_count = {x : 0 for x in range(0,4)}
      self.afc_count = {x : 0 for x in range(0,4)}
      self.cc_count = {x : 0 for x in range(0,16)}
      self.cc_error_count = 0
      self.cc_repeat_count = 0
      self.cc_skip_count = {x : 0 for x in range(0,16)}
      self.pcr_count = 0
    def __repr__(self):
      return "__repr__ not implemented yet."
    def __str__(self):
      delim = " "
      s = ""
      # s = "{0}{1}".format(self, delim) # TODO: Print some sort of object identifier.
      s += "Packet count : {0}{1}".format(self.pkt_count, delim)
      s += "Sync byte count : {0}{1}\n".format(self.sync_byte_count, delim)
      s += "TEI count : {0}{1}".format(self.tei_count, delim)
      s += "PUSI count : {0}{1}".format(self.pusi_count, delim)
      # s += "PID count : {0}{1}".format(self.pid_count, delim)
      s += "TSC count : {0}{1}".format(self.tsc_count, delim)
      s += "AFC count : {0}{1}".format(self.afc_count, delim)
      # s += "CC count : {0}{1}".format(self.cc_count, delim)
      s += "CC error count : {0}{1}".format(self.cc_error_count, delim)
      # s += "CC repeat count : {0}{1}".format(self.cc_repeat_count, delim)
      # s += "CC skip count : {0}{1}".format(self.cc_skip_count, delim)
      return s
