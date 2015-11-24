import RxPPacketHeader

class RxPPacket:
	MAX_WINDOW_SIZE = 1024

	def __init__(self, header=None, data=None):
		self.header = header or RxPPacketHeader()

	def checksum(self):


	# compute checksum & compare it against embedded checksum
	def verify_packet(self):


	# fancy formatting
	def __str__(self):

