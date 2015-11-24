import socket
import RxPPacket

class SocketState:
	NONE = "none"

class RxPSocket:
	def __init__(self):
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		self.state = SocketState.NONE
		self.send_window = 1
		self.receive_window = RxPPacket.MAX_WINDOW_SIZE

		self.source_address = None
		self.destination_address = None 

		self.seq_number = 0
		self.ack_number = 0