from RxP import RxP
import sys


#run this like 'python RxPTester.py 2'
def main():
	print "Starting RxPTester" 
    if sys.argv[1] == 1:
	   test_create_socket()
    elif sys.argv[1] ==2:
        test_2()
    elif sys.argv[1] == 3:
        test_3()


def test_create_socket():
	socket = RxP.createRxPSocket("localhost", 9998)

	RxP.closeRxPSocket(socket)

#basic client server
def test_2():
    client = RxP.createRxPSocket(127.0.0.1, 5000)
    server = RxP.createRxPSocket(127.0.0.1, 5001)
    server.listenForRxPConnections(server)
    client.connectToRxP(127.0.0.1, 5001)

    #not sure the accept works after listening. Do we have to call it or should it do it automatically if it's listening?
    #server.acceptRxPSocketConnection(server, )

    server.close(server)

#basic send. Should fail cause sockets are not connected
def test_3():
    client = RxP.createRxPSocket(127.0.0.1, 5000)
    server = RxP.createRxPSocket(127.0.0.1, 5001)
    client.sendData("Hello")

#basic connect and send. Should pass
def test_4():
    client = RxP.createRxPSocket(127.0.0.1, 5000)
    server = RxP.createRxPSocket(127.0.0.1, 5001)
    server.listenForRxPConnections(server)
    client.connectToRxP(127.0.0.1, 5001)
    client.sendData("Hello")
    client.close(client)

if __name__ == "__main__":
    main()