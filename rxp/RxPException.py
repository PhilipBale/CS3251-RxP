class RxPException():

	NONE = ""
	TIMEOUT = "operation timed out"
	CONNECTION_TIMEOUT = "connection timed out"
	INVALID_CHECKSUM = "invalid checksum"

	def __init__(self, exception_type = None, message = None):
		self.exception_type = exception_type
		self.message = message
		if self.message is None:
			self.message = exception_type

	def __str__(self):
		return self.message
