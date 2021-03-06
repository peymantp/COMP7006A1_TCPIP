import os
import socket
import threading
from os import path

def client(name, sock):
    dataport = 7006
    dataConnection = socket.socket()
    command = sock.recv(1024)
    print "Server connecting to " + str(command)
    dataConnection.connect((command,dataport))

    command = sock.recv(1024)
    if command[:3] == "GET":
        files = filter(path.isfile, os.listdir("./"))
        sock.send(str(files))

        filename = sock.recv(1024)
        if os.path.isfile(filename):
            sock.send("Geting " + str(os.path.getsize(filename)))
            userResponse = sock.recv(1024)
            if userResponse[:2] == 'OK':
                with open(filename,'rb') as f:
                    while True:
                        bytesToSend = f.read(1024)
                        dataConnection.send(bytesToSend)
                        if bytesToSend == "":
                            break
        else:
            sock.send("No such file found")
    elif command[:4] == "SEND":
        filename = "s_"+command[4:]

        sock.send("READY")
        filesize = sock.recv(1024)
        totalRecv = 0
        with open(filename, "wb") as f:
            while totalRecv < int(filesize):
                data = dataConnection.recv(1024)
                totalRecv += len(data)
                print str(totalRecv) + "<" + str(filesize) + " " + str(len(data))
                f.write(data)
                status = "{0:.2f}".format((totalRecv/float(filesize))*100) + "% DONE"
                print status
def Main():
    port = 7005
    mySocket = socket.socket()
    address = socket.gethostbyname(socket.getfqdn()) #selects first non localhost in etc/hosts
    print str(address)

    try:
        mySocket.bind((address,port))
    except socket.error as e:
        print(str(e))

    mySocket.listen(5)

    print " Server Started"
    while True:
        connection, addr = mySocket.accept()
        print "client connected ip:<" + str(addr) + ">"
        
        cThread = threading.Thread(target=client, args=("Thread",connection))
        cThread.start()

    mySocket.close()

if __name__ == '__main__':
    Main()