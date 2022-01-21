#cmput404W22 dchu lab 2
#https://uofa-cmput404.github.io/lab-2-tcp-proxy.html
import socket as soc

HOSTPORT = 80
CLIENTPORT = 8001
BUFFER = 4096
REMOTEHOSTNAME = "www.google.com"

def createTCPSocket():
    print("creating socket")
    try:
        s  = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        return s
    except:
        print("ERROR: Could not create socket")
        exit()

def connectToHost(s):
    try:
        hostAddr = soc.gethostbyname(REMOTEHOSTNAME)
    except:
        print("ERROR: Could not resolve hostname")
        exit()
    try:
        s.connect((hostAddr, HOSTPORT))
    except:
        print("ERROR: Could not connect to host")
        exit()
    print("Socket connected to {}({})".format(REMOTEHOSTNAME, hostAddr))

def getReply(s):
    isRecv = True
    msg = b''
    while isRecv:
        buffer = s.recv(BUFFER)
        if buffer != b'':
            msg += buffer
        else:
            isRecv = False
    return msg

def bindSocket(s):
    try:
        s.bind(('', CLIENTPORT))
    except Exception as e:
        print("ERROR: Could not bind socket\n exception{}".format(e))
        exit()

def sendMsg(msg):
    #host setup
    s = createTCPSocket()
    s.setsockopt(soc.SOL_SOCKET, soc.SO_REUSEADDR, 1)
    connectToHost(s)
    #send msg
    s.sendall(msg)
    s.shutdown(soc.SHUT_WR)
    reply = getReply(s)
    s.close()
    return reply


def main():
    #client setup
    clientSoc = createTCPSocket()
    clientSoc.setsockopt(soc.SOL_SOCKET, soc.SO_REUSEADDR, 1)

    bindSocket(clientSoc)
    clientSoc.listen(5)
    print("listening on client socket")


    isRecv = True
    while isRecv:
        connection, address = clientSoc.accept()
        print("Connection accepted from {}".format(address))
        print("Getting msg from client...")
        msg = getReply(connection)
        print("recieved message from {}".format(address))
        reply = sendMsg(msg)
        print("reply received, sending reply to client")
        connection.sendall(reply)
        connection.close()

if __name__ == "__main__":
    main()