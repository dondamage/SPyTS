import AdaptationFieldError

class AdaptationField():
  """A class representing the adaptation field of an MPEG2 transport stream packet."""
  def __init__(self, af):
    """Initialize AdaptationField."""
    if isinstance(af, bytes):
      if 0 < len(af) and len(af) < 183:
        pos = 0 # Keep track of the position within the adaptation field.
        self._content = af
        self.adaptation_field_length = self._content[0]
        if self.adaptation_field_length != len(af):
          raise AdaptationFieldError("Mismatch in adaptation field length.")
        self.discontinuity_indicator(self._content[1] & 0x80 >> 7)
        self.random_access_indicator = self._content[1] & 0x40 >> 6
        self.elementary_stream_priority_indicator = self._content[1] & 0x20 >> 5
        self.pcr_flag = self._content[1] & 0x10 >> 4
        self.opcr_flag = self._content[1] & 0x08 >> 3
        self.splicing_point_flag = self._content[1] & 0x04 >> 2
        self.transport_private_data_flag = self._content[1] & 0x02 >> 1
        self.adaptation_field_extension_flag = self._content[1] & 0x1 >> 0
        
        if self.pcr_flag == 1:
          self.program_clock_reference_base = int.from_bytes((self._content[1:6] & 0xFFFFFFFF80) >> 7, "big")
          self.program_clock_reference_reserved = int.from_bytes((self._content[5:6] & 0x7E) >> 1, "big")
          self.program_clock_reference_extension = int.from_bytes((self._content[5:7] & 0x1FF), "big")
        if self.opcr_flag == 1:
          self.original_program_clock_reference_base = int.from_bytes((self._content[8:13] & 0xFFFFFFFF80) >> 7, "big")
          self.original_program_clock_reference_reserved = int.from_bytes((self._content[13:14] & 0x7E) >> 1, "big")
          self.original_program_clock_reference_extension = int.from_bytes((self._content[13:15] & 0x1FF), "big")
        if self.splicing_point_flag == 1:
          self.splice_countdown = int.from_bytes(self._content[15:16], "big")
        if self.transport_private_data_flag == 1:
          self.transport_private_data_length = int.from_bytes(self._content[16:17], "big")
          # TODO: Extract private data.
        if self.adaptation_field_extension_flag == 1:
          self.adaptation_field_extension_length = int.from_bytes(self._content[16:17], "big")
          # TODO: Extract flags fields.
      else:
        raise AdaptationFieldError("Invalid adaptation field length.")
  
  def adaptation_field_length(self):
    return
  
  def discontinuity_indicator(self):
    return
  
  def random_access_indicator(self):
    return
  
  def elementary_stream_priority_indicator(self):
    return
  
  def pcr_flag(self):
    return
  
  def opcr_flag(self):
    return
  
  def splicing_point_flag(self):
    return
  
  def splice_countdown(self):
    return
  
  def transport_private_data_length(self):
    return
  
  def transport_private_data(self):
    return
  
  def adaptation_field_extension_length(self):
    return
  
  def ltw_flag(self):
    return
  
  def piecewise_rate_flag(self):
    return
  
  def seamless_splice_flag(self):
    return
    
  def ltw_valid_flag(self):
    return
    
  def ltw_offset(self):
    return
    
  def piecewise_rate(self):
    return
    
  def splice_type(self):
    return
  