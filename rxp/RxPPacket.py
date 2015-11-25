import RxPPacketHeader
import math
import md5

class RxPPacket:
	MAX_WINDOW_SIZE = math.pow(2, 16)
	MAX_SEQ_NUM = math.pos(2, 32)

	def __init__(self, header=None, payload=None):
		self.header = header or RxPPacketHeader()
		self.payload = payload
		self.header.checksum = checksum(payload)
		self.header.payload_length = len(payload)

	# https://docs.python.org/2/library/md5.html
	def checksum(self, payload):
		md5_checksum = md5.new(payload).digest()
		md5_adjusted_checksum = md5_checksum[:2] + md5_checksum[14:16]
		return md5_adjusted_checksum

	# compute checksum & compare it against embedded checksum
	def verify_packet(self):
		return checksum() == self.header.checksum

	# fancy formatting
	def __str__(self):
		print("Packet verified: ", verify_packet())
		print("Packet payload: ", self.payload)

