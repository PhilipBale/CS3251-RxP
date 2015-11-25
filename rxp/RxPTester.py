from RxP import RxP
import sys


#run this like 'python RxPTester.py 2'
def main():
    print "Starting RxPTester" 
    test_to_run = int(sys.argv[1])
    print "Running command: ", test_to_run

    if test_to_run == 1:
        test_create_socket()
    elif test_to_run ==2:
        test_2()
    elif test_to_run == 3:
        test_3()
    else:
    	print "No commands run!"


def test_create_socket():
    socket = RxP.createRxPSocket("localhost", 9998)

    RxP.closeRxPSocket(socket)

#basic client server
def test_2():
    client = RxP.createRxPSocket("127.0.0.1", 5000)
    server = RxP.createRxPSocket("127.0.0.1", 5001)
    RxP.listenForRxPConnections(server)
    RxP.connectToRxP(client, "127.0.0.1", 5001)

    #not sure the accept works after listening. Do we have to call it or should it do it automatically if it's listening?
    #server.acceptRxPSocketConnection(server, )

    server.close(server)

#basic send. Should fail cause sockets are not connected
def test_3():
    client = RxP.createRxPSocket("127.0.0.1", 5000)
    server = RxP.createRxPSocket("127.0.0.1", 5001)
    RxP.sendData(client, "Hello")

#basic connect and send. Should pass
def test_4():
    client = RxP.createRxPSocket("127.0.0.1", 5000)
    server = RxP.createRxPSocket("127.0.0.1", 5001)
    RxP.listenForRxPConnections(server)
    RxP.connectToRxP(client, "127.0.0.1", 5001)
    RxP.sendData(client, "Hello")
    RxP.close(client)

if __name__ == "__main__":
    main()