from RxP import RxP

def main():
	print "Starting RxPTester" 
	test_create_socket()

def test_create_socket():
	socket = RxP.createRxPSocket("localhost", 9998)

	RxP.closeRxPSocket(socket)


if __name__ == "__main__":
    main()