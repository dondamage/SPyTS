import TsPacket as _TsPkt

class TsDemux(object):
  def __init__(self, tsfr=None):
    """Initialize."""
    # callbacks is a dictionary linking PIDs to functions to be called when
    # a TS packet with a certain PID arrives.
    # e.g. self.callbacks = {0 : [process_pat, count_packet], 101 : [monitor_pcr]}
    self.callbacks = {}
    self.tsfr = tsfr
  
  def __repr__(self):
    """Stringify."""
    return "{0} not implemented.".format(self.__repr__.__name__)
    
  def __str__(self):
    """Stringify."""
    return "{0} not implemented.".format(self.__str__.__name__)
    
  def subscribe(self, pids, fun):
    """
    Subscribe to get TS packets with selected PIDs passed to a function.
    pids: list of PIDs to subscribe for.
    fun: callback function to be called for packets with PID in pids.
    """
    if callable(fun):
      for p in pids:
        demux_entry = self.callbacks.get(p)
        if demux_entry is not None:
          demux_entry.append(fun)
        else:
          self.callbacks[p] = [fun]
    else:
      # TODO: Raise an apropriate exception here.
      print("Trying to add a non-callable object in {0}".format(self.__name__))
    
  def unsubscribe(self, pids, fun):
    """
    Unsubscribe to stop getting TS packets with selected PIDs passed to a function.
    At the moment it is not possible to unsubscribe a sepcific callback
    function from a specific PID event.
    """
    for p in pids:
      demux_entry = self.callbacks.get(p)
      if fun in demux_entry:
        demux_entry.remove(fun)
      else:
        # TODO: Raise an apropriate exception here.
        print("Trying to remove non-existent callback in {0}".format(self.__name__))
    
  def demux(self, pkt=None):
    """
    Demux the given TS packet to all subscribers.
    """
    if pkt is None and self.tsfr is not None:
      pkt = self.tsfr.read(1)
    callbacks = self.callbacks.get(pkt.get_pid())
    if callbacks is not None:
      for f in callbacks:
        f(pkt)
    