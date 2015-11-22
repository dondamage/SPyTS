import SPyTS.TSPacket as TSPacket
import SPyTS.TSPacketStatistic as TSPacketStatistic

class TSAnalyser(object):
  """A class to perform analysis of a sequence of MPEG2 transport stream
  packets and store the results thereof."""
  def __init__(self):
    # Use an object of TSPacketStatistic for the total TS statistics information.
    self.ts_analysis = TSPacketStatistic.TSPacketStatistic()
    # Use an object of TSPacketStatistic for the per PID statistics information.
    self.pid_analysis = {}
    # Store the previous TSPacket of each PID as status information.
    self.pid_status = {}
    # PCR analysis.
    self.perform_pcr_analysis = False # NOTE: not implemented yet.
    self.pcr_pid = None
  def __repr__(self):
    """Return string representation of the TSPacket object."""
    return "{0} not implemented.".format(self.__repr__.__name__)
  def __str__(self):
    """Stringify the TSPacket object."""
    s = "Transport stream analysis:\n"
    s += str(self.ts_analysis)
    s += "\nPID analysis:\n"
    for pid in self.pid_analysis.keys():
      s += "PID {} analysis:\n".format(pid)
      s += str(self.pid_analysis[pid])
      s += "\n"
    return s
  def add_pkt(self, pkt):
    """Analyse the TSPacket pkt and add the results to the internal statistics."""
    # First get the PID to allow per PID analysis.
    pid = pkt.pid()
    if pid not in self.pid_analysis.keys():
      self.pid_analysis[pid] = TSPacketStatistic.TSPacketStatistic()
      self.pid_status[pid] = None
    
    self.ts_analysis.pkt_count += 1
    self.pid_analysis[pid].pkt_count += 1
    
    if pkt.has_sync_byte():
      self.ts_analysis.sync_byte_count += 1
      self.pid_analysis[pid].sync_byte_count += 1
    
    if pkt.tei() == 1:
      self.ts_analysis.tei_count += 1
      self.pid_analysis[pid].tei_count += 1
    
    if pkt.pusi() == 1:
      self.ts_analysis.pusi_count += 1
      self.pid_analysis[pid].pusi_count += 1
    
    if pkt.tp() == 1:
      self.ts_analysis.tp_count += 1
      self.pid_analysis[pid].tp_count += 1
    
    tsc = pkt.tsc()
    self.ts_analysis.tsc_count[tsc] += 1
    self.pid_analysis[pid].tsc_count[tsc] += 1
    
    afc = pkt.afc()
    self.ts_analysis.afc_count[afc] += 1
    self.pid_analysis[pid].afc_count[afc] += 1
    
    cc = pkt.cc()
    if self.pid_status[pid] is not None:
      prev_cc = self.pid_status[pid].cc()
    else:
      prev_cc = ((cc - 1) % 16)
    self.ts_analysis.cc_count[cc] += 1
    self.pid_analysis[pid].cc_count[cc] += 1
    if cc == (prev_cc + 1) % 16:
      pass
    elif cc == prev_cc:
      self.ts_analysis.cc_repeat_count += 1
      self.pid_analysis[pid].cc_repeat_count += 1
    else:
      self.ts_analysis.cc_error_count += 1
      self.pid_analysis[pid].cc_error_count += 1
      skip_cc = (cc - prev_cc) % 16
      self.ts_analysis.cc_skip_count[skip_cc] += 1
      self.pid_analysis[pid].cc_skip_count[skip_cc] += 1
    
    af = pkt.adaptation_field()
    if af is not None and len(af) > 1:
      # The AdaptationField class is not implemented yet, so the PCR flag must
      # be extracted manually.
      # pcr_flag = af.pcr_flag()
      pcr_flag = af[1] & 0x10
      if pcr_flag == 1:
        self.ts_analysis.pcr_count += 1
        self.pid_analysis[pid].pcr_count += 1
    
    self.pid_status[pid] = pkt
    
  def get_pcr_pids(self):
    """Return a list of PIDs which contain PCR values."""
    pcr_pids = [x for x in self.pid_analysis.keys() if self.pid_analysis[x].pcr_count > 0]
    return pcr_pids

