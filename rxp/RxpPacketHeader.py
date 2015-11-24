class RxPPacketHeader:
	
	src_port = 0
	dest_port = 0

	seq_number = 0
	ack_number = 0

	syn_flag = 0
	ack_flag = 0
	fin_flag = 0
	lst_flag = 0
	rst_flag = 0

	rcv_window = 0
	payload_length = 0

	checksum = 0

	payload = None