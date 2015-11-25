#FxA Client
#for command line arguments
import sys

# for ip address validation
from socket import inet_aton

#testing stuff, delete me
#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

if len(sys.argv) != 4:
    print ('Please enter arguments in the correct format: X A P' + 
        '\nX: The port number this client should bind to'+
        '\nA: The IP address of NetEmu' + 

        '\nP: The UDP port number of NetEmu ')
    sys.exit()

# port number at which the FxA-client's UDP socket should bind to. Should be equal to the server's port number minus 1
portnumber = int(sys.argv[1])
ipaddress = sys.argv[2]
emuportnumber = int(sys.argv[3])
file = ""
size = 1

# check for valid client port numbers
if portnumber < 1025 or portnumber > 65536: 
    print 'Please enter a valid port number for client (1025-65536)'
    sys.exit()

# Port number for client must be even
if portnumber % 2 != 0:
    print 'Port number for client must be even'
    sys.exit()

# check for valid IP addresses
try:
    inet_aton(ipaddress)
except:
    print("Not a valid IP address")
    sys.exit()

# check for valid NetEmu UDP port number
if emuportnumber < 1025 or emuportnumber > 65536: 
    print 'Please enter a valid port number for NetEmu (1025-65536)'
    sys.exit()

#Connect the client to the FxA-server
def connect(): 
    print "connecting to server"
    #TODO
    return

# Download the file specified if it exists on the server
def get(filename):
    print "getting file: " + str(filename)
    #TODO
    return

# Upload file to server
def post(filename):
    print "uploading file: " + str(filename)
    #TODO
    return

#updates client's maximum window-size
def window(newsize):
    print "updated window size to " + str(newsize)
    size = newsize

#disconnect from server
def disconnect():
    print "disconnecting"
    #TODO
    return

print "Welcome! Commands include: \n'connect' \n'get <file>' \n'post <file>' \n'window <size>' \n'disconnect'"


#the command loop
while True:

    # have the user input a command and parse it
    command = raw_input('\nCommand: ').split(" ")
    # check for invalid command
    if len(command) > 2:
        print "Enter a valid command"
        continue

    #check for connect and disconnect
    if len(command) == 1:

        if command[0] == "connect":
            connect()
            continue
        elif command[0] == "disconnect":
            disconnect()
            continue
        else:
            print "Please enter a valid command"
            continue
    #check for get, post, and window
    elif len(command) == 2:
        #get
        if command[0] == "get":
            file = str(command[1])
            get(file)
            continue
        #post
        if command[0] == "post":
            file = str(command[1])
            post(file)
            continue
        #window
        if command[0] == "window":
            #int type checking
            try:
                size = int(command[1])
            except:
                print "invalid window size"
                continue
            window(size)
            continue
        else:
            print "Please enter a valid command"
            continue