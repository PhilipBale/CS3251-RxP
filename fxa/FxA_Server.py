#FxA Server
#for command line arguments
import sys

# for ip address validation
from socket import inet_aton

# check for number of correct command line arguments
if len(sys.argv) != 4:
    print ('Please enter arguments in the correct format: X A P' + 
        '\nX: The port number this server should bind to'+
        '\nA: The IP address of NetEmu' + 

        '\nP: The UDP port number of NetEmu ')
    sys.exit()

# port number at which the FxA-Server's UDP socket should bind to
try:
    portnumber = int(sys.argv[1])
except:
    print 'Please enter a valid port number for Server (1025-65536)'
    sys.exit()

ipaddress = sys.argv[2]

try:
    emuportnumber = int(sys.argv[3])
except:
    print 'Please enter a valid port number for NetEmu (1025-65536)'
    sys.exit()

size = 1

# check for valid client port numbers
if portnumber < 1025 or portnumber > 65536: 
    print 'Please enter a valid port number for client (1025-65536)'
    sys.exit()

# Port number for client must be even
if portnumber % 2 != 1:
    print 'Port number for client must be odd'
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

#updates server's maximum window-size
def window(newsize):
    print "updated window size to " + str(newsize)
    size = newsize

#Shutdown the server
def terminate():
    print "Shutting down server"
    #TODO
    return

#TODO creating and binding rxp socket

#the command loop
while True:

    # have the user input a command and parse it
    command = raw_input('\nCommand: ').split(" ")
    # check for invalid command
    if len(command) > 2:
        print "Enter a valid command"
        continue

    #check for terminate
    if len(command) == 1:
        # terminate the server
        if command[0] == "terminate":
            terminate()
            continue
        else:
            print "Please enter a valid command"
            continue
    #check for window
    elif len(command) == 2:
        #window
        if command[0] == "window":
            window(command[1])
            continue
        else:
            print "Please enter a valid command"
            continue