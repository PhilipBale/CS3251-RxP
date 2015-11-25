class RxPPacketHeader:
	
	def __init__(self):	
		self.src_port = 0
		self.dest_port = 0

		self.seq_number = 0
		self.ack_number = 0

		self.fst_flag = 0
		self.syn_flag = 0
		self.ack_flag = 0
		self.fin_flag = 0
		self.lst_flag = 0
		self.rst_flag = 0

		self.rcv_window = 0

		self.checksum = 0
		self.payload_length = 0

	def toString():
		return "" + self.src_port + self.dest_port + self.seq_number + self.ack_number 
		+ self.syn_flag + self.ack_flag + self.fin_flag + self.lst_flag + self.rst_flag 
		+ self.payload_length + self.rcv_window

		# todo do we include rcv_window?



	