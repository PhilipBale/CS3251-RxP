from RxPPacketHeader import RxPPacketHeader
import math
import pickle
import md5

MAX_WINDOW_SIZE = math.pow(2, 16)
MAX_SEQ_NUM = math.pow(2, 32) 
MAX_PAYLOAD_LENGTH = math.pow(2,9) # in bytes
MAX_RESEND_LIMIT = math.pow(2,5) #idk

class RxPPacket:
	MAX_WINDOW_SIZE = MAX_WINDOW_SIZE
	MAX_SEQ_NUM = MAX_SEQ_NUM
	MAX_PAYLOAD_LENGTH = MAX_PAYLOAD_LENGTH
	MAX_RESEND_LIMIT = MAX_RESEND_LIMIT
	

	def __init__(self, header=None, payload=None):
		self.header = header or RxPPacketHeader()
		self.payload = payload
		if self.payload is None or self.payload == None:
			self.payload = '_'

		self.header.payload_length = len(self.payload)
		self.header.checksum = self.checksum(self.payload)

	# https://docs.python.org/2/library/md5.html
	def checksum(self, payload):
		total_payload = self.header.toString() + payload
		md5_checksum = md5.new(total_payload).digest()
		md5_adjusted_checksum = md5_checksum[:2] + md5_checksum[14:16] 
		return md5_adjusted_checksum

	# compute checksum & compare it against embedded checksum
	def verifyPacket(self):
		return self.checksum(self.payload) == self.header.checksum

	def byteVersion(self):
		return pickle.dumps(self)

	# fancy formatting
	def __str__(self):
		print("Packet verified: ", verifyPacket())
		print("Packet payload: ", self.payload)


