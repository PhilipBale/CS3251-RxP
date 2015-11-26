from RxP import RxP
import sys
import time


#run this like 'python RxPTester.py 2'
def main():
    print "Starting RxPTester" 
    test_to_run = int(sys.argv[1])
    is_client = int(sys.argv[2]) == 1
    print "Running command: ", test_to_run

    if test_to_run == 1:
        test_create_socket()
    elif test_to_run ==2:
        test_basic_connection(is_client)
    elif test_to_run == 3:
        test_basic_sending(is_client)
    else:
        print "No commands run!"


def test_create_socket():
    socket = RxP.createRxPSocket("localhost", 9998)

    RxP.closeRxPSocket(socket)

#basic client server
def test_basic_connection(is_client):
    if is_client:
        print "Testing basic connection as a client"
        client = RxP.createRxPSocket("localhost", 5000)
        RxP.connectToRxP(client, "localhost", 5001)
        time.sleep(3)
        RxP.closeRxPSocket(client)
    else:
        print "Testing basic connection as a server"
        server = RxP.createRxPSocket("localhost", 5001)
        connection_attempt_address = RxP.listenForRxPConnections(server)
        print("Receieved connection attempt from: ", connection_attempt_address)
        RxP.acceptRxPSocketConnection(server, connection_attempt_address)
        time.sleep(3)
        RxP.closeRxPSocket(server)
    

#basic send. Should fail cause sockets are not connected
def test_basic_sending(is_client):
    if is_client:
        print "Testing basic connection as a client"
        client = RxP.createRxPSocket("localhost", 5000)
        RxP.connectToRxP(client, "localhost", 5001)
        RxP.sendData(client, "Hello, World!  This is a big test.  Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test")

        RxP.closeRxPSocket(client)
    else:
        print "Testing basic connection as a server"
        server = RxP.createRxPSocket("localhost", 5001)
        connection_attempt_address = RxP.listenForRxPConnections(server)
        print("Receieved connection attempt from: ", connection_attempt_address)
        RxP.acceptRxPSocketConnection(server, connection_attempt_address)

        response = RxP.receiveData(server, 999999)
        print "Received data: ", response
 
        RxP.closeRxPSocket(server)


#basic connect and send. Should pass
def test_4():
    client = RxP.createRxPSocket("localhost", 5000)
    server = RxP.createRxPSocket("localhost", 5001)
    RxP.listenForRxPConnections(server)
    RxP.connectToRxP(client, "localhost", 5001)
    RxP.sendData(client, "Hello")
    RxP.close(client)

if __name__ == "__main__":
    main()