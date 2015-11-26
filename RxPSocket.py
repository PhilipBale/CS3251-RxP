import socket

import RxPPacket
import pickle

class SocketState:
	NONE = "created",
	BOUND = "bound",
	CONNECTED = "connected",
	CLOSED = "closed",


CONNECTION_TIMEOUT_LIMIT = 5
LISTEN_TIMEOUT_LIMIT = 10
RECEIVE_TIMEOUT_LIMIT = 20

class RxPSocket:
	CONNECTION_TIMEOUT_LIMIT = CONNECTION_TIMEOUT_LIMIT
	LISTEN_TIMEOUT_LIMIT = LISTEN_TIMEOUT_LIMIT
	RECEIVE_TIMEOUT_LIMIT = RECEIVE_TIMEOUT_LIMIT

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

		self._socket.settimeout(CONNECTION_TIMEOUT_LIMIT * 5) # tiemout larger for connection

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

	def sendPacket(self, rxp_packet):
		self._socket.sendto(rxp_packet.byteVersion(), self.destination_address)

	def receivePacket(self, receive_window_size):
		self._socket.settimeout(CONNECTION_TIMEOUT_LIMIT)
		while True:
			try:
				packet, address = self._socket.recvfrom(int(receive_window_size))
				print "packet received"
				packet = self.unpicklePacket(packet)
				print "unpickled"

				break
			except Exception as e:
				print("Received error", e)
				raise e

		print "Returning packet"
		return (address, packet)

	@property
	def timeout(self):
		return self._socket.gettimeout()
	@timeout.setter
	def timeout(self, time):
		self._socket.settimeout(time)

	def unpicklePacket(self, packet):
		return pickle.loads(packet)

		
	def __str__(self):
		return "State: " + str(self.state[0]) + ", Source: " + str(self.source_address) \
			+ ", Destination: " + str(self.destination_address)

