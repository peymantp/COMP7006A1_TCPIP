import os
import socket
import threading


def Get(name,sock):
    filename = sock.recv(1024)
    if os.path.isfile(filename):
        sock.send("Geting: " + str(os.path.getsize(filename)))
        userResponse = sock.recv(1024)
        if userResponse[:2] == 'OK':
            with open(filename,'rb') as f:
                while True:
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
                    if bytesToSend == "":
                        break
    else:
        sock.send("No such file found")

    sock.close()

def Main():
    mySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    port = 7005

    print str(socket.gethostname())
    mySocket.bind((socket.gethostname(),port))
    mySocket.listen(5)

    print "Server Started"
    while True:
        connection, addr = mySocket.accept()
        print "client connected ip:<" + str(addr) + ">"
        readThread = threading.Thread(target=Get, args=("retrThread",connection))
        readThread.start()

    mySocket.close()

if __name__ == '__main__':
    Main()