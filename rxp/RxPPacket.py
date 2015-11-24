import RxPPacketHeader

class RxPPacket:

	def __init__(self, header=None, data=None):
		self.header = header or RxPPacketHeader()

	def checksum(self):


	# compute checksum & compare it against embedded checksum
	def verify_packet(self):


	# fancy formatting
	def __str__(self):

