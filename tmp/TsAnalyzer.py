import TsPacket
import TsPacketError

class TsAnalyzer(object):
  """
  A class to perform analysis of a sequence of TS packets.
  """
  def __init__(self):
    """Initialize."""
    self.ts_statistic = TsStatistics()
    self.psi_statistic = PSIStatistics()
    self.pid_statistics = {}
    self.pid_stati = {}
    self.pcr_pids = []
    self.buf_pkts = []
    self.buf_pcr = []

  def __repr__(self):
    """Representation."""
    return "{0} not implemented.".format(self.__repr__.__name__)

  def __str__(self):
    """Stringify."""
    return "{0} not implemented.".format(self.__str__.__name__)

  def reset_statistics(self):
    """Reset all internal statistics and counters."""
    self.ts_statistic = TsStatistics()
    self.pid_statistics = {}

  def add_pkt(self, pkt):
    """Add a TsPacket or a list of TsPackets for analysis."""
    if isinstance(pkt, list):
      for p in pkt:
        self.add_pkt(p)
    else:
      if isinstance(pkt, TsPacket.TsPacket):
        self.analyse_pkt(pkt)
      else:
        raise TsPacketError.TsPacketError()

  def add_raw_pkt(self, raw_pkt):
    """Add a raw TS packet or a list of raw TS packets for analysis."""
    pass

  def add(self, iter):
    """Add all TS packets in the iterable object iter.
    Return the number of added TS packets."""
    cnt = 0
    for p in iter:
      self.add_pkt(p)
      cnt += 1
    return cnt

  def analyse_pkt(self, pkt):
    # Count the packet.
    self.ts_statistic.pkt_count += 1
    pid = pkt.get_pid()
    if pid not in self.pid_statistics.keys():
      self.pid_statistics[pid] = TsStatistics()
      self.pid_statistics[pid].pkt_count = 1
      self.pid_stati[pid] = PIDStatus()
    else:
      self.pid_statistics[pid].pkt_count += 1

    # Count correct sync bytes.
    sync_byte = pkt.get_sync()
    if sync_byte == b'\x47':
      self.ts_statistic.sync_byte_count += 1
      self.pid_statistics[pid].sync_byte_count += 1

    # Count transport errors.
    tei = pkt.get_tei()
    if tei == 1:
      self.ts_statistic.tei_count += 1
      self.pid_statistics[pid].tei_count += 1

    # Count payload unit start.
    pusi = pkt.get_pusi()
    if pusi == 1:
      self.ts_statistic.pusi_count += 1
      self.pid_statistics[pid].pusi_count += 1

    # Count transport priotity.
    tp = pkt.get_tp()
    if tp == 1:
      self.ts_statistic.tp_count += 1
      self.pid_statistics[pid].tp_count += 1

    # Count scrambling status bits.
    tsc = pkt.get_tsc()
    self.ts_statistic.tsc_count[tsc] += 1
    self.pid_statistics[pid].tsc_count[tsc] += 1

    # Count adaptation field control bits.
    afc = pkt.get_afc()
    self.ts_statistic.afc_count[tsc] += 1
    self.pid_statistics[pid].afc_count[tsc] += 1

    # Count CC errors and CC repetitions.
    cc = pkt.get_cc()
    prev_cc = self.pid_stati[pid].cc
    if afc & 0x1 != 0: # Only check for CC errors if pkt contains payload.
      if (prev_cc+1) % 16 == cc:
        pass
      elif prev_cc == cc:
        self.ts_statistic.cc_rep_count += 1
      else:
        self.ts_statistic.cc_err_count += 1
        self.ts_statistic.cc_jmp_count[(cc - prev_cc) % 16]
    prev_cc = cc

    # Count PCR samples.
    pcr_flag = pkt.get_pcr_flag()
    if pcr_flag == 1:
      self.ts_statistic.pcr_count += 1
      self.pid_statistics[pid].pcr_count += 1

    # Perform PCR analysis, i.e. calculate arrival timestamps per pkt.
    # TODO.
    
    # Invoke callbacks for PID status changes.
    # TODO.
    
    # Update PID status.
    self.status_update(pkt)

  def status_update(self, pkt):
    """Use pkt to update the status of the respective PID."""
    # Update PID status.
    pid = pkt.get_pid()
    if pid not in self.pid_stati:
      self.pid_stati[pid] = PIDStatus()
    self.pid_stati[pid].sync_byte = pkt.get_sync()
    self.pid_stati[pid].tei = pkt.get_tei()
    self.pid_stati[pid].pusi = pkt.get_pusi()
    self.pid_stati[pid].tp = pkt.get_tp()
    self.pid_stati[pid].tsc = pkt.get_tsc()
    self.pid_stati[pid].afc = pkt.get_afc()
    self.pid_stati[pid].cc = pkt.get_cc()

  def calc_pcr_bitrate(self):
    """Calculate the TS bitrate based on PCR values."""
    pass
  
  def get_pcr_pids(self):
    """Return a list of PIDs which carry PCR values."""
    pcr_pids = [p for p in self.pid_statistics.keys() if self.pid_statistics[p].pcr_count > 0]
    return pcr_pids

class TsStatistics(object):
  """A structure to hold statistics information of a sequence of TS packets."""
  def __init__(self):
    self.pkt_count = 0
    self.sync_byte_count = 0
    self.tei_count = 0
    self.pusi_count = 0
    self.tp_count = 0
    self.tsc_count = {x : 0 for x in range(4)}
    self.afc_count = {x : 0 for x in range(4)}
    self.pcr_count = 0
    self.cc_err_count = 0
    self.cc_rep_count = 0
    self.cc_jmp_count = {x : 0 for x in range(16)}

class PSIStatistics(object):
  """A structure to hold statistics information for PSI tables."""
  def __init__(self):
    self.pat_count = 0
    self.cat_count = 0
    self.nit_count = 0
    self.pmt_count = {}
    self.pat_version = None
    self.cat_version = None
    self.nit_version = None
    self.pmt_version = {}

class PIDStatus(object):
  """A structure to hold PID status information."""
  def __init__(self):
    self.sync_byte = 0x47
    self.tei = 0
    self.pusi = 0
    self.tp = 0
    self.tsc = 0
    self.afc = 0
    self.cc = 0
