class RxPPacketHeader:
	
	def __init__(self):	
		self.src_port = 0
		self.dest_port = 0

		self.seq_number = 0
		self.ack_number = 0
		
		self.syn_flag = 0
		self.ack_flag = 0
		self.fin_flag = 0
		self.lst_flag = 0
		self.rst_flag = 0

		self.rcv_window = 0

		self.checksum = 0
		self.payload_length = 0

	def toString(self):
		return "" + str(self.src_port) + str(self.dest_port) + str(self.seq_number) \
		+ str(self.ack_number) + str(self.syn_flag ) + str(self.ack_flag ) \
		+ str(self.fin_flag ) + str(self.lst_flag ) + str(self.rst_flag) \
		+ str(self.payload_length ) + str(self.rcv_window)

		# todo do we include rcv_window?



	