#cmput404W22 dchu lab 2
#https://uofa-cmput404.github.io/lab-2-tcp-proxy.html

import socket as soc


PORT = 80
BUFFER = 4096
REMOTEHOSTNAME = "www.google.com"
PAYLOAD = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(REMOTEHOSTNAME)

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


def sendPayload(s):
    payloadBytes = str.encode(PAYLOAD)
    s.sendall(payloadBytes)#Send whole payload at once
    s.shutdown(soc.SHUT_WR)#stop all writes

def getReply(s):
    isRecv = True
    msg = b''
    print("awaiting reply...")
    while isRecv:
        buffer = s.recv(BUFFER)
        if buffer != b'':
            msg += buffer
        else:
            isRecv = False
    print("closing socket")
    s.close()
    return msg

def main():
    s = createTCPSocket()
    connectToHost(s)
    sendPayload(s)
    msg = getReply(s)
    print("\n\nRequest reply from {}:\n{}".format(REMOTEHOSTNAME, msg))
    s.close()

if __name__ == "__main__":
    main()