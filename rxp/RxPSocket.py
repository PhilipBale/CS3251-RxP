import socket
import RxPPacket

class SocketState:
	NONE = "none",
	BOUND = "bound",
	CONNECTED = "connected"

class RxPSocket:

	CONNECTION_TIMEOUT_LIMIT = 30 # seconds
	
	def __init__(self):
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		self.state = SocketState.NONE 
		self.send_window = 1
		self.receive_window_size = RxPPacket.MAX_WINDOW_SIZE

		self.source_address = None
		self.destination_address = None 

		self.seq_number = 0
		self.ack_number = 0


	def setTimeout(self, value):
		self._socket.settimeout(value)

	def bind(self, source_address):
		self.source_address = self.source_address or source_address
		self._socket.bind(self.source_address)
		self.state = SocketState.BOUND

	def connect(self, destination_address):
		if not self.state == SocketState.BOUND:
			raise RxPException("Socket not bound yet")
		elif self.state = SocketState.CONNECTED:
			raise RxPException("Socket already connected")

		self.destination_address = destination_address
		self.state = SocketState.CONNECTED

		self.seq_number = 0
		self.ack_number = 0

		


