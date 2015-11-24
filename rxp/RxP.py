import RxPSocket
import RxPPacket

class RxP:

	def createRxPSocket():

	def bindRxPSocket(rxp_socket, ip_address, port_number):

	def closeRxPSocket(rxp_socket):

	def listenForRxPConnections(rxp_socket):

	def acceptRxPSocketConnection(rxp_socket):

	def connectToRxP(rxp_socket, ip_address, port_number):

	def setWindowSize(rxp_socket, window_length):

	def sendData(rxp_socket, data):

	def receiveData(rxp_socket, max_length):