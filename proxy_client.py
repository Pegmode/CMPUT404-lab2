#cmput404W22 dchu lab 2
#https://uofa-cmput404.github.io/lab-2-tcp-proxy.html
import socket as soc
import pdb


PORT = 8001
BUFFER = 4096
REMOTEHOSTNAME = "localhost"#127.0.0.1
PAYLOAD = "GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n"


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
        s.connect((hostAddr, PORT))
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
    print("closing socket")
    return msg

def sendPayload(s):
    payloadBytes = str.encode(PAYLOAD)
    s.sendall(payloadBytes)#Send whole payload at once
    s.shutdown(soc.SHUT_WR)#stop all writes

def main():
    s = createTCPSocket()
    connectToHost(s)
    sendPayload(s)
    msg = getReply(s)
    print("\n\nRequest reply from {}:\n{}".format(REMOTEHOSTNAME, msg))
    s.close()

if __name__ == "__main__":
    main()