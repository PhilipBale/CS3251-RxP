import socket
import RxPPacket

class SocketState:
	NONE = "created",
	BOUND = "bound",
	CONNECTED = "connected",
	CLOSED = "closed",

class RxPSocket:

	CONNECTION_TIMEOUT_LIMIT = 30 # seconds

	def __init__(self):
		print("Initializing new RxPSocket")
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		self.state = SocketState.NONE 
		self.send_window = 1
		self.receive_window_size = RxPPacket.MAX_WINDOW_SIZE

		self.source_address = None
		self.destination_address = None 

		self.seq_number = 0
		self.ack_number = 0

		print("Socket initialized!", str(self))

	def bind(self, source_address):
		self.source_address = self.source_address or source_address
		self._socket.bind(self.source_address)
		self.state = SocketState.BOUND
		print("Socket has been bound! ", str(self))

	def close(self):
		print("Closing RxPSocket: ", str(self))
		self._socket.close()
		self.state = SocketState.CLOSED
		print("Closed RxPSocket: ", str(self))

	def setTimeout(self, value):
		self._socket.settimeout(value)



	def connect(self, destination_address):
		if not self.state == SocketState.BOUND:
			raise RxPException("Socket not bound yet")
		elif self.state == SocketState.CONNECTED:
			raise RxPException("Socket already connected")

		self.destination_address = destination_address
		self.state = SocketState.CONNECTED

		self.seq_number = 0
		self.ack_number = 0

	def sendPacket(self, rxp_packet):
		self._socket.sentdto(rxp_packet.byteVersion(), self.source_address)

	def receivePacket(self, receive_window_size):
		while True:
			try:
				packet, address = self._socket.recvfrom(receive_window_size)
				break
			except socket.error as e:
				if e.error != -1:
					raise e # todo fix

		return (address, packet)

		
	def __str__(self):
		return "State: " + str(self.state[0]) + ", Source: " + str(self.source_address) \
			+ ", Destination: " + str(self.destination_address)

