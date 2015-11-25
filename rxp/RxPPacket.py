import RxPPacketHeader
import math
import md5

MAX_WINDOW_SIZE = math.pow(2, 16)
MAX_SEQ_NUM = math.pow(2, 32) 
MAX_PAYLOAD_LENGTH = math.pow(2,9) # in bytes

class RxPPacket:
	

	def __init__(self, header=None, payload=None):
		self.header = header or RxPPacketHeader()
		self.payload = payload
		self.header.checksum = checksum(payload)
		self.header.payload_length = len(payload)

	# https://docs.python.org/2/library/md5.html
	def checksum(self, payload):
		total_payload = self.header.toString() + payload
		md5_checksum = md5.new(total_payload).digest()
		md5_adjusted_checksum = md5_checksum[:2] + md5_checksum[14:16]
		return md5_adjusted_checksum

	# compute checksum & compare it against embedded checksum
	def verifyPacket(self):
		return checksum() == self.header.checksum

	# gets byte version of packets
	def byteVersion(self):
		print "Not yet implemented"

	# fancy formatting
	def __str__(self):
		print("Packet verified: ", verifyPacket())
		print("Packet payload: ", self.payload)

