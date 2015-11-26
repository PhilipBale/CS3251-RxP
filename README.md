# CS3251-RxP
Reliable transport protocol assignment for CS 3251.  Phillip Bale &amp; Allen Chen

Section B.  Due 11/25/15.

RxP - Reliable Transfer Protocol


DO NOT USE CYGWIN, THERE ARE KNOWN ISSUES WITH CYGWIN AND PYTHON 2.7's RAW_INPUT

Testing things for now:


FxA CLIENT:
- Command-line: FxA-client X A P 

The command-line arguments are: 

X: the port number at which the FxA-client’s UDP socket should bind to (even number). Please remember that this port number should be equal to the server’s port number minus 1. 
A: the IP address of NetEmu
P: the UDP port number of NetEmu 

*******************************************
eg 'python FxA_Client.py 3002 127.0.0.1 5000'

then run 'connect'

then run 'get obama.txt'
*******************************************

- Command: connect - The FxA-client connects to the FxA-server (running at the same IP host). 

- Command: get F - The FxA-client downloads file F from the server (if F exists in the same directory with the FxA-server program).

-the only file that exists on the server is obama.txt (Obama's inaugaral address)


- Command: post F - The FxA-client uploads file F to the server (if F exists in the same directory with the FxA-client program). This feature will be treated as extra credit for up to 20 project points.

- Command: window W (only for projects that support configurable flow window) W: the maximum receiver’s window-size at the FxA-Client (in segments). 

- Command: disconnect - The FxA-client terminates gracefully from the FxA-server. 


FxA Server:
- Command-line: FxA-server X A P 

The command-line arguments are:
X: the port number at which the FxA-server’s UDP socket should bind to (odd number) 
A: the IP address of NetEmu
P: the UDP port number of NetEmu 

*******************************************
eg 'python FxA_Server.py 3003 127.0.0.1 5000'
*******************************************

- Command: window W (only for projects that support pipelined and bi- directional transfers) 

W: the maximum receiver’s window-size at the FxA-Server (in segments). 

- Command: terminate Shut-down FxA-Server gracefully. 