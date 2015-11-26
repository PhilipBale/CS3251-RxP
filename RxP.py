from RxPSocket import RxPSocket, SocketState
from RxPPacket import RxPPacket
from RxPPacketHeader import RxPPacketHeader
from RxPException import RxPException

from collections import deque

class RxP:

	@staticmethod
	def createRxPSocket(ip_address, port_number):
		socket = RxPSocket()
		source_address = (ip_address, port_number)
		socket.bind(source_address)
		return socket

	@staticmethod
	def closeRxPSocket(rxp_socket):
		rxp_socket.close()
		# todo send closing stuff

	@staticmethod
	def listenForRxPConnections(rxp_socket):
		if rxp_socket.state == SocketState.NONE:
			raise RxPException("listenForRxPConnections: Socket not yet bound!")

		timeout_limit = rxp_socket.LISTEN_TIMEOUT_LIMIT
		while timeout_limit > 0:
			incoming_packet = None
			try:
				packet_address, incoming_packet = rxp_socket.receivePacket(RxPPacket.MAX_PACKET_SIZE)
			except RxPException as e:
				if e.type == RxPException.TIMEOUT or e.type == RxPException.INVALID_CHECKSUM:
					timeout_limit -= 1
			except Exception as e:
				if str(e) == "timed out":
					print "Incoming connection timed out, trying again."
					timeout_limit -= 1

			if not incoming_packet is None:
				if incoming_packet.header.syn_flag == 1: # TODO determine if needs to be unique
					return packet_address

		if timeout_limit <= 0:
			raise RxPException(RxPException.CONNECTION_TIMEOUT)

		return None

	# sends ack to a potential connection
	# incoming connection is a (src, packet) tuple
	@staticmethod
	def acceptRxPSocketConnection(rxp_socket, incoming_address):
		if rxp_socket.state == SocketState.NONE:
			raise RxPException("acceptRxPSocketConnection: Socket not yet bound!")
		elif rxp_socket.state != SocketState.BOUND:
			raise RxPException("acceptRxPSocketConnection: Socket needs to be bound!")


		rxp_socket.seq_number = 0
		rxp_socket.ack_number = 1000

		rxp_socket.destination_address = incoming_address

		response = RxP.sendSYNACK(rxp_socket)

		rxp_socket.state = SocketState.CONNECTED
		print("Succesfully accepted an RxP connection!")

	@staticmethod
	def connectToRxP(rxp_socket, ip_address, port_number):
		destination_address = (ip_address, port_number)
		rxp_socket.connect(destination_address)

		syn_ack = RxP.sendSYN(rxp_socket) # TODO implement
		rxp_socket.seq_number = 1000
		rxp_socket.ack_number = 0

		RxP.sendACK(rxp_socket)

		print("Succesfully connected to RxP!")

	@staticmethod
	def setWindowSize(rxp_socket, window_length):
		rxp_socket.receive_window_size = window_length

	@staticmethod
	def sendSYN(rxp_socket):
		print "Sending SYN! from socket", rxp_socket

		header = RxPPacketHeader()
		header.src_port = rxp_socket.source_address[1]
		header.dst_port = rxp_socket.destination_address[1]
		header.syn_flag = 1

		packet = RxPPacket(header)

		number_of_resends = RxPPacket.MAX_RESEND_LIMIT

		while number_of_resends > 0:
			print "Attempt #", (RxPPacket.MAX_RESEND_LIMIT - number_of_resends) + 1
			rxp_socket.sendPacket(packet)
			try:
				address, packet = rxp_socket.receivePacket(RxPPacket.MAX_PACKET_SIZE)

				print "Verifying packet"

				if not packet.verifyPacket(): #invalid checksum
					print("Incorrect checksum for sent data ack. Discarding packet")
					number_of_resends -= 1
				elif packet.header.syn_flag == 0 or packet.header.ack_flag == 0:
					print("Not a SYN ACK! Discarding")
					number_of_resends -= 1
				else:
					print("Received succesful SYN ACK")
					return packet
			except Exception as e:
				if str(e) == "timed out": 
					print("Sending SYN timed out. " + str(number_of_resends - 1) + " attempts remaining")
					number_of_resends -= 1
				elif str(e).find("EOFError"):
					print("Packet was mangled! resending!")
					number_of_resends -= 1
				else:
					print "Grr"
					print str(e)
					raise e
		raise RxPException("Sending SYN failed!")

		return None

	@staticmethod
	def sendACK(rxp_socket): 
		print "Sending ACK!"

		header = RxPPacketHeader()
		header.src_port = rxp_socket.source_address[1]
		header.dst_port = rxp_socket.destination_address[1]
		header.ack_flag = 1
		header.ack_number = rxp_socket.ack_number

		packet = RxPPacket(header)

		rxp_socket.sendPacket(packet)

	@staticmethod
	def sendSYNACK(rxp_socket): 
		print "Sending SYNACK!"

		header = RxPPacketHeader()
		header.src_port = rxp_socket.source_address[1]
		header.dst_port = rxp_socket.destination_address[1]
		header.syn_flag = 1
		header.ack_flag = 1

		packet = RxPPacket(header)

		number_of_resends = RxPPacket.MAX_RESEND_LIMIT

		while number_of_resends > 0:

			rxp_socket.sendPacket(packet)

			try:
				address, packet = rxp_socket.receivePacket(RxPPacket.MAX_PACKET_SIZE)

				if not packet.verifyPacket(): #invalid checksum
					print("Incorrect checksum for sent data ack. Discarding packet")
					number_of_resends -= 1
				elif packet.header.syn_flag == 1 or packet.header.ack_flag == 0:
					print("Not a ACK! Discarding")
					number_of_resends -= 1
				else:
					print("Received succesful ACK to our SYNACK")
					return packet
			except Exception as e:
				if str(e) == "timed out": 
					print("Sending SYN timed out. " + str(number_of_resends) + " resends remaining")
					number_of_resends -= 1
				else: 
					raise e
				

		return None

	@staticmethod
	def sendData(rxp_socket, data):
		if not rxp_socket.state == SocketState.CONNECTED:
			raise RxPException("sendData: Socket not connected!")
		
		# break data into chunks
		data_chunks = deque()

		packet_payload_length = RxPPacket.MAX_PAYLOAD_LENGTH
		numberOfPackets = int(len(data) / packet_payload_length)
		if len(data) % packet_payload_length > 0:
			numberOfPackets += 1

		print("Preparing " + str(numberOfPackets) + " packets to send")
		for i in range(numberOfPackets):
			start_index = int(packet_payload_length * i)
			end_index = int(start_index + packet_payload_length)

			if i + 1 == numberOfPackets:
				data_chunks.append(data[start_index:])
			else:
				data_chunks.append(data[start_index:end_index])


		# these are the acual packets that we need to send
		packets_to_send = deque()

		for data_item in data_chunks:
			is_last_packet = (data_item == data_chunks[-1])

			header = RxPPacketHeader()
			header.src_port = rxp_socket.source_address[1]
			header.dst_port = rxp_socket.destination_address[1]
			header.rcv_window = rxp_socket.receive_window_size

			if is_last_packet:
				header.lst_flag = 1

			header.seq_number = rxp_socket.seq_number
			rxp_socket.seq_number += 1 # todo wrap sequence number if needed

			packet = RxPPacket(header, data_item)
			packets_to_send.append(packet)

		# these are the packets that we know are sent but haven't been acked yet
		packets_to_be_acked = deque()

		window_size = rxp_socket.receive_window_size
		cur_seq_number = packets_to_send[0].header.seq_number

		print ("Sending packets for data: ", data)
		while len(packets_to_send) > 0:


			while window_size > 0 and len(packets_to_send) > 0:
				packet = packets_to_send.popleft()

				rxp_socket.sendPacket(packet)
				window_size -= 1
				packets_to_be_acked.append(packet)

			# collect acks
			try:
				address, packet = rxp_socket.receivePacket(RxPPacket.MAX_PACKET_SIZE)

				if not packet.verifyPacket: #invalid checksum
					print("Incorrect checksum for sent data ack. Discarding packet")
					window_size += 1
				else:
					# valid packet
					print("Validating packet!")
					if packet.header.ack_number == cur_seq_number and packet.header.ack_flag > 0:
						print("Received desired ack: ", cur_seq_number)
						packets_to_be_acked.popleft()
						cur_seq_number += 1
						window_size += 1
						window_size *= 2
					else:
						print("Received sent packet ack but not one we were looking for")
						print(str(packet.header.ack_number) + " vs " + str(cur_seq_number))
						if packet.header.seq_number > cur_seq_number:
							print("Sequence number is greater than looking for")
							window_size += 1
						else:
							packets_to_send.extendleft(packets_to_be_acked)
							packets_to_be_acked.clear()
							print ("Receive duplicate packet. Discarding")
				

			except Exception as e:
				if str(e) == "timed out": 
					print("Socket timeout for sent ack receive--resending")
					# need to send packet
					window_size = 3
					
				else: 
					raise e

	@staticmethod
	def receiveData(rxp_socket, max_length=99999999999999999):
		if not rxp_socket.state == SocketState.CONNECTED:
			raise RxPException("sendData: Socket not connected!")

		timeout_limit = RxPSocket.RECEIVE_TIMEOUT_LIMIT

		data_buffer = ""

		while timeout_limit > 0:
			incoming_packet = None
			try:
				packet_address, incoming_packet = rxp_socket.receivePacket(RxPPacket.MAX_PACKET_SIZE)
			except RxPException as e:
				if e.type == RxPException.TIMEOUT or e.type == RxPException.INVALID_CHECKSUM:
					timeout_limit -= 1
			except Exception as e:
				if str(e) == "timed out":
					print "Timed out, trying again."
					timeout_limit -= 1

			if not incoming_packet is None and incoming_packet.verifyPacket():
				# let's do some work on this packet
				print "Incoming/Outcoing: " + str(incoming_packet.header.seq_number) + ":" + str(rxp_socket.ack_number)
				if incoming_packet.header.seq_number < rxp_socket.ack_number:
					print "Resending ack!"
					print "Incoming seq number: ", incoming_packet.header.seq_number
					RxP.sendACK(rxp_socket) # resend
				elif incoming_packet.header.seq_number == rxp_socket.ack_number:
					RxP.sendACK(rxp_socket)

					rxp_socket.ack_number += 1
					data_buffer += incoming_packet.payload
					rxp_socket.receive_window_size = incoming_packet.header.rcv_window

					if incoming_packet.header.lst_flag == 1:
						return data_buffer
					elif incoming_packet.header.fin_flag == 1:
						RxP.sendACK(rxp_socket)
						RxP.closeRxPSocket(rxp_socket)

		if timeout_limit <= 0:
			raise RxPException(RxPException.CONNECTION_TIMEOUT)

		return None

	@staticmethod
	def isConnected(rxp_socket):
		return rxp_socket.state == SocketState.CONNECTED
