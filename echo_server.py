#cmput404W22 dchu lab 2
#https://uofa-cmput404.github.io/lab-2-tcp-proxy.html
import socket as soc

PORT = 8001
BUFFER = 4096
ADDRESS = "localhost"#localhost

def createTCPSocket():
    print("creating socket")
    try:
        s  = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        return s
    except:
        print("ERROR: Could not create socket")
        exit()

def bindSocket(s):
    try:
        s.bind(('', PORT))
    except:
        print("ERROR: Could not bind socket")
        exit()

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
    bindSocket(s)
    s.listen(5)
    print("Socket set to listen...")

    while True:
        connection, address = s.accept()
        print("Connection reveived from {}".format(address))
        msg = getReply(connection)
        #print("\nMESSAGE FROM CLIENT:{}\n".format(msg))
        connection.sendall(msg)
        connection.close()

if __name__ == "__main__":
    main()