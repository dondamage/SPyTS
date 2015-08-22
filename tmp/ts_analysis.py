#!/bin/python

import io
import os
import struct

# RD_FILE = "./test.ts"

# RD_FILE = "D:/workspace/Test/GT42/gt42_descrambling_brakes_if_gt31_muxes/parallel_streams/Polsat_GT42_out_08062015.ts"
# RD_FILE = "D:/workspace/Test/GT42/gt42_descrambling_brakes_if_gt31_muxes/parallel_streams/Polsat_transparent_GT31_out_08062015.ts"
# RD_FILE = "D:/workspace/Test/GT42/gt42_descrambling_brakes_if_gt31_muxes/parallel_streams/Polsat_mux_GT31_out_08062015.ts"

# RD_FILE = "D:/workspace/Test/GT42/gt42_descrambling_brakes_if_gt31_muxes/parallel_streams_3/03Polsat_GT42_out_10072015.ts"
# RD_FILE = "D:/workspace/Test/GT42/gt42_descrambling_brakes_if_gt31_muxes/parallel_streams_3/03Polsat_mux_GT31_out_10072015.ts"
# RD_FILE = "D:/workspace/Test/GT42/gt42_descrambling_brakes_if_gt31_muxes/parallel_streams_3/03Polsat_transparent_GT31_out_10072015.ts"

# RD_FILE = "D:\workspace\Test\GT23\gt23_2.1_cc_errors_high_bitrate_vbrs\AmcHD.ts"
# RD_FILE = "D:\workspace\Test\GT23\gt23_2.1_cc_errors_high_bitrate_vbrs\HollywoodHD.ts"
# RD_FILE = "D:\workspace\Test\GT23\gt23_2.1_cc_errors_high_bitrate_vbrs\XtremeHD.ts"
RD_FILE = "D:/tmp/WISI.ts"

rd_path, rd_name = os.path.split(RD_FILE)
WR_FILE_PCR = os.path.join(rd_path, rd_name+"_pcr_analysis.csv")
WR_FILE_TS = os.path.join(rd_path, rd_name+"_ts_packets.csv")
WR_FILE_PCR_PID = os.path.join(rd_path, rd_name+"_pcr_pid_packets.csv")
WR_FILE_PID = os.path.join(rd_path, rd_name+"_pid_statistics.csv")
MPEG2TS_PKT_SIZE = 188
MPEG2TS_SYNC_BYTE = 0x47
monitored_pcr_pid = 0x65 # 0x186B # 0x184D # 0x1843 # 257 # NOTE: must be set manually for the time being.

class TsAnalyzer(object):
  """
  A class for the analysis of MPEG2 transport streams.
  """
  def __init__(self):
    """Initialize."""
    self.pat_count = 0
    self.cat_count = 0
    self.pmt_count = {}
  def __repr__(self):
    """Stringify object."""
    pass
  def reset(self):
    """Reset the internal state."""
    pass
  def add_pkt(self, pkt):
    """Add one or more TS packets for analysis."""
    pass
  def read_file(self, ts_filename):
    """Read a TS file for analysis."""
    pass
  def parse_pat(self):
    """Parse PAT."""
    # Check if a valid PAT was supplied.
    # Must handle sections.
    self.pat_count = self.pat_count + 1
  def parse_cat(self):
    """Parse CAT."""
    # Check if a valid CAT was supplied.
    # Must handle sections.
    self.cat_count = self.cat_count + 1
  def parse_pmt(self, pmt):
    """Parse PMT."""
    # Check if a valid PMT was supplied.
    # Must handle sections.
    pid = self.get_pid(pmt)
    self.pmt_count[pid] = self.pmt_count[pid] + 1
  def calc_bitrate(self):
    """Calculate TS bitrate based on packet arrivals."""
    pass
  def calc_pcr_bitrate(self):
    """Calculate TS bitrate based on inter PCR data."""
    pass

if __name__ == '__main__':
  pkt = None
  # Each pkt has the form {fdi_ptr : ..., pkt_num : ..., sync_byte : ..., 
  # tei : ..., pusi : ..., tp : ..., pid : ..., tsc : ..., afc : ..., cc : ...}
  pkt_list = []
  # Each pcr pkt has the form {pkt_num : ..., pcr : ..., disc : ...}
  pcr_list = []
  fdo_pcr = open(WR_FILE_PCR, "w")
  fdo_pcr.write("PCR_NUMBER,PACKET_NUMBER,PCR_FIELD_H,PCR_FIELD_L,PCR[27M_ticks],dPCR[27M_ticks],dPCR[s],PCR_BITRATE\n")
  
  # Check sync bytes.
  with open(RD_FILE, 'rb') as fdi:
    # Init.
    total_n_pkt = 0
    total_n_sync_err = 0
    total_n_pids = 0
    total_n_scr = 0
    total_n_scr_even = 0
    total_n_scr_odd = 0
    total_n_cc_err = 0
    total_n_af = 0
    total_n_pcr = 0
    
    known_pids = set()
    counts = {
      "n_pkt" : {},
      "n_sync_err" : {},
      "n_scr" : {},
      "n_scr_even" : {},
      "n_scr_odd" : {},
      "cc_prev" : {},
      "n_cc_err" : {},
      "n_af" : {},
      "n_pcr" : {}
    }
    
    # PCR analysis.
    pcr = 0
    delta_pcr = 0
    pcr_h, pcr_l = 0, 0
    total_n_pkt_old_rc = 0
    
    # Start analysis.
    pkt = fdi.read(MPEG2TS_PKT_SIZE)
    while len(pkt) == MPEG2TS_PKT_SIZE:
      # Extract flags and fields from TS packet.
      sync_byte = pkt[0]
      # pid = struct.unpack("!H",pkt[1:2+1])[0] & 0x1FFF
      tei = (pkt[1] & 0x80) >> 7
      pusi = (pkt[1] & 0x40) >> 6
      tp = (pkt[1] & 0x20) >> 5
      pid = int.from_bytes(pkt[1:3], 'big') & 0x1FFF
      tsc = (pkt[3] & 0xC0) >> 6
      afc = (pkt[3] & 0x30) >> 4
      cc = (pkt[3] & 0x0F) >> 0
      af_len = pkt[4] >> 0
      pcr_flag = ((pkt[5] & 0x10) >> 4) & (afc >> 1) & af_len > 0
      
      if pid not in known_pids:
        known_pids.add(pid)
        for k in counts.keys():
          counts.get(k)[pid] = 0
        counts.get("cc_prev")[pid] = cc - 1
      
      # Count packet.
      total_n_pkt += 1
      counts.get("n_pkt")[pid] += 1
      
      # Store TS packet information in list, timestamp is calculated later.
      # pkt_list.append({
        # "fdi_ptr"   : fdi.tell(),
        # "pkt_num"   : total_n_pkt,
        # "timestamp" : None,
        # "sync_byte" : sync_byte,
        # "tei"       : tei,
        # "pusi"      : pusi,
        # "tp"        : tp,
        # "pid"       : pid,
        # "tsc"       : tsc,
        # "afc"       : afc,
        # "cc"        : cc,
        # "pcr"       : pcr_flag
      # })
      
      # Check sync byte.
      if sync_byte != MPEG2TS_SYNC_BYTE:
        total_n_sync_err += 1
        counts.get("n_sync_err")[pid] += 1
      
      # Check for CC error.
      if cc != (counts.get("cc_prev").get(pid) + 1) % 16 and \
        cc != counts.get("cc_prev").get(pid):
          total_n_cc_err += 1
          counts.get("n_cc_err")[pid] += 1
      counts.get("cc_prev")[pid] = cc
      
      # Check scrambling status.
      if tsc == 0:
        pass
      elif tsc == 2:
        total_n_scr += 1
        total_n_scr_even += 1
        counts.get("n_scr")[pid] += 1
        counts.get("n_scr_even")[pid] += 1
      elif tsc == 3:
        total_n_scr += 1
        total_n_scr_odd += 1
        counts.get("n_scr")[pid] += 1
        counts.get("n_scr_odd")[pid] += 1
      else:
        pass
      
      # Check adaptation field and PCR flag.
      if afc >= 2:
        total_n_af += 1
        if pcr_flag == 1:
          total_n_pcr += 1
          counts.get("n_pcr")[pid] += 1
          if (pid == monitored_pcr_pid or not monitored_pcr_pid):
            pcr_h_old, pcr_l_old = pcr_h, pcr_l
            
            # Extract PCR value and compute delta to previous PCR value.
            pcr_h, pcr_l = struct.unpack("!LL", b''.join([b'\x00\x00', pkt[6:11+1]]))
            pcr_old = pcr
            pcr = pcr_h * 2**32 + pcr_l
            pcr_base = (pcr >> 15)
            pcr_ext = pcr & 0x1FF
            pcr = pcr_base * 300 + pcr_ext
            if pcr > pcr_old:
              delta_pcr = pcr - pcr_old
            else:
              delta_pcr = pcr - pcr_old # TODO: Handle PCR wrap around.
            delta_pkt = total_n_pkt - total_n_pkt_old_rc
            if delta_pkt != 0:
              pcr_bitrate = (delta_pkt*188*8)/(delta_pcr*(27e6)**-1)
            total_n_pkt_old_rc = total_n_pkt
            fdo_pcr.write("{0},{1},{2:.0f},{3:.0f},{4:.0f},{5:.0f},{6:.6f},{7:.0f}\n".format(counts.get("n_pcr")[pid], total_n_pkt, pcr_h, pcr_l, pcr, delta_pcr, delta_pcr*(27e6)**-1, pcr_bitrate))
            
            # Calculate arrival timestamps for TS packets.
            # Working with the lists here, so some things are done twice (see above).
            # pkt_list[-1]["timestamp"] = pcr*((27e6)**-1)
            # if len(pcr_list) > 0 and pcr_list[-1] is not None:
              # pcr_pkt_num_delta = total_n_pkt - pcr_list[-1]["pkt_num"]
              # pcr_delta = (pcr - pcr_list[-1]["pcr"])
              # pcr_bitrate = pcr_pkt_num_delta*188*8 / (pcr_delta*((27e6)**-1))
              # for i in range(pcr_list[-1]["pkt_num"], total_n_pkt):
                # pkt_list[i]["timestamp"] = pkt_list[i-1]["timestamp"] + 188*8/pcr_bitrate
                
            pcr_list.append({
              "pkt_num" : total_n_pkt,
              "pcr"     : pcr,
              "disc"    : 0
            })
        
      pkt = fdi.read(MPEG2TS_PKT_SIZE)
  
  if not fdi.closed:
    fdi.close()
  
  if not fdo_pcr.closed:
    fdo_pcr.close()
  
  # Print TS packet list.
  fdo_ts = open(WR_FILE_TS, "w")
  fdo_ts.write("PACKET_NUMBER, SYNC_BYTE_ERROR, TEI, PUSI, TP, PID, TSC, AFC, CC, ARRIVAL_TIME\n")
  fdo_pcr_pid = open(WR_FILE_PCR_PID, "w")
  fdo_pcr_pid.write("PACKET_NUMBER, SYNC_BYTE_ERROR, TEI, PUSI, TP, PID, TSC, AFC, CC, ARRIVAL_TIME\n")
  
  # for pkt in pkt_list:
    # fdo_ts.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}\n".format(
      # pkt["pkt_num"], pkt["sync_byte"], pkt["tei"], pkt["pusi"], pkt["tp"],
      # pkt["pid"], pkt["tsc"], pkt["afc"], pkt["cc"], pkt["timestamp"]
    # ))
    # if pkt["pid"] == monitored_pcr_pid:
      # fdo_pcr_pid.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}\n".format(
        # pkt["pkt_num"], pkt["sync_byte"], pkt["tei"], pkt["pusi"], pkt["tp"],
        # pkt["pid"], pkt["tsc"], pkt["afc"], pkt["cc"], pkt["timestamp"]
      # ))
  
  if not fdo_ts.closed:
    fdo_ts.close()
  
  if not fdo_pcr_pid.closed:
    fdo_pcr_pid.close()
  
  # Print per PID statistics.
  fdo_pid = open(WR_FILE_PID, 'w')
  fdo_pid.write("PID, N_PACKETS, N_SYNC_ERR, N_SCR, N_SCR_EVEN, N_SCR_ODD,\
    N_CC_ERR, N_PCR, N_AF\n")
  known_pids_list = list(known_pids)
  known_pids_list.sort()
  for pid in known_pids_list:
    fdo_pid.write(str(pid)+", ")
    fdo_pid.write(str(counts.get("n_pkt")[pid])+", ")
    fdo_pid.write(str(counts.get("n_sync_err")[pid])+", ")
    fdo_pid.write(str(counts.get("n_scr")[pid])+", ")
    fdo_pid.write(str(counts.get("n_scr_even")[pid])+", ")
    fdo_pid.write(str(counts.get("n_scr_odd")[pid])+", ")
    fdo_pid.write(str(counts.get("n_cc_err")[pid])+", ")
    fdo_pid.write(str(counts.get("n_pcr")[pid])+", ")
    fdo_pid.write(str(counts.get("n_af")[pid])+", ")
    fdo_pid.write("\n")
  
  if not fdo_pid.closed:
    fdo_pid.close()
  
  # Print some statistics to stdout.
  print("total_n_pkt: {0}".format(total_n_pkt))
  print("total_n_sync_err: {0}".format(total_n_sync_err))
  print("total_n_af: {0}".format(total_n_af))
  print("total_n_scr: {0}".format(total_n_scr))
  print("total_n_scr_even: {0}".format(total_n_scr_even))
  print("total_n_scr_odd: {0}".format(total_n_scr_odd))
  print("total_n_cc_err: {0}".format(total_n_cc_err)) 
  print("total_n_pcr: {0}".format(total_n_pcr))
  print("Monitored PCR PID: {0}".format(monitored_pcr_pid))
  