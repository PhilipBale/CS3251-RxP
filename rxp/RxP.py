import RxPSocket
import RxPPacket
import RxPException

class RxP:

	def createRxPSocket(ip_address, port_number):
		socket = RxPSocket()
		source_address = (ip_address, port_number)
		socket.bind(source_address)

	def closeRxPSocket(rxp_socket):

	def listenForRxPConnections(rxp_socket):
		if rxp_socket.state == SocketState.NONE:
			raise RxPException("Socket not yet bound!")

		timeout_limit = rxp_socket.CONNECTION_TIMEOUT_LIMIT
		while timeout_limit > 0:
			try:
				incoming_packet, packet_address = receiveData(rxp_socket, rxp_socket.receive_window_size)
			except RxPException as e:
				if e.type == RxPException.TIMEOUT or e.type == RxPException.INVALID_CHECKSUM:
					timeout_limit--

			if not incoming_packet is None:
				if packet.header.syn_flag == 1: # TODO determine if needs to be unique
					rxp_socket.ack_number = incoming_packet.header.seq_number + 1 
					rxp_socket.destination_address = packet_address
					return True

		if timeout_limit <= 0:
			raise RxPException(RxPException.CONNECTION_TIMEOUT))

		return None

	# sends ack to a potential connection
	def acceptRxPSocketConnection(rxp_socket):
		if rxp_socket.state == SocketState.NONE:
			raise RxPException("Socket not yet bound!")
		elif rxp_socket.state == SocketState.BOUND:
			raise RxPException("No destination set!")




	def connectToRxP(rxp_socket, ip_address, port_number):
		destination_address = (ip_address, port_number)
		rxp_socket.connect(destination_address)

		syn_ack = sendSYN(rxp_socket) # TODO implement
		rxp_socket.ack_number = syn_ack.header.seq_number + 1

		sendACK(rxp_socket)

	def setWindowSize(rxp_socket, window_length):
		rxp_socket.receive_window_size = window_length

	def sendSYN(rxp_socket):

	def sendACK(rxp_socket):

	def sendData(rxp_socket, data):

	def receiveData(rxp_socket, max_length):

	