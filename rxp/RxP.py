from RxPSocket import RxPSocket
from RxPPacket import RxPPacket
from RxPException import RxPException

import Queue

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

	def listenForRxPConnections(rxp_socket):
		if rxp_socket.state == SocketState.NONE:
			raise RxPException("listenForRxPConnections: Socket not yet bound!")

		timeout_limit = rxp_socket.CONNECTION_TIMEOUT_LIMIT
		while timeout_limit > 0:
			try:
				packet_address, incoming_packet = receiveData(rxp_socket, rxp_socket.receive_window_size)
			except RxPException as e:
				if e.type == RxPException.TIMEOUT or e.type == RxPException.INVALID_CHECKSUM:
					timeout_limit -= 1

			if not incoming_packet is None:
				if packet.header.syn_flag == 1: # TODO determine if needs to be unique
					return (packet_address, incoming_packet)

		if timeout_limit <= 0:
			raise RxPException(RxPException.CONNECTION_TIMEOUT)

		return None

	# sends ack to a potential connection
	# incoming connection is a (src, packet) tuple
	def acceptRxPSocketConnection(rxp_socket, incoming_connection):
		if rxp_socket.state == SocketState.NONE:
			raise RxPException("acceptRxPSocketConnection: Socket not yet bound!")
		elif rxp_socket.state == SocketState.BOUND:
			raise RxPException("acceptRxPSocketConnection: No destination set!")

		incoming_address, incoming_packet = incoming_connection

		rxp_socket.seq_number = 0
		rxp_socket.ack_number = incoming_packet.header.seq_number + 1

		rxp_socket.destination_address = packet_address

		response = sendSYNACK(rxp_socket)

		rxp_socket.state = SocketState.CONNECTED


	def connectToRxP(rxp_socket, ip_address, port_number):
		destination_address = (ip_address, port_number)
		rxp_socket.connect(destination_address)

		syn_ack = sendSYN(rxp_socket) # TODO implement
		rxp_socket.ack_number = syn_ack.header.seq_number + 1

		sendACK(rxp_socket)

	def setWindowSize(rxp_socket, window_length):
		rxp_socket.receive_window_size = window_length

	def sendSYN(rxp_socket):
		print "Method not completed"
		# todo implement sending of syn

	def sendACK(rxp_socket):
		print "Method not completed"
		# todo implement sending of ack

	def sendSYNACK(rxp_socket):
		print "Method not completed"
		# todo implement sending of ack

	def sendData(rxp_socket, data):
		if not rxp_socket.state == SocketState.CONNECTED:
			raise RxPException("sendData: Socket not connected!")
		
		# break data into chunks
		data_chunks = Queue.Queue()

		packet_payload_length = RxPPacket.MAX_PAYLOAD_LENGTH
		numberOfPackets = len(data) / packet_payload_length
		if len(data) % packet_payload_length > 0:
			numberOfPackets += 1

		for i in range(numberOfPackets):
			start_index = packet_payload_length * i
			end_index = start_index + packet_payload_length

			if i + 1 == numberOfPackets :
				data_chunks.append(data[start_index:])
			else:
				data_chunks.append(data[start_index:end_index])

		# construct packet queue

	def receiveData(rxp_socket, max_length):
		# todo implement data receiving
		print "Method not completed"
