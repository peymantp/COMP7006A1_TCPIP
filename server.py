import os
import socket
import threading
from os import path

address = socket.gethostbyname(socket.gethostname())

def client(name, sock, dataConnection):
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
                print str(totalRecv) + "<" + str(filesize) + " " + str(len(data)) + " " + str(totalRecv) 
                f.write(data)
                status = "{0:.2f}".format((totalRecv/float(filesize))*100) + "% DONE"
                print status
def Main():
    mySocket = socket.socket() 
    port = 7005

    print str(address)

    try:
        mySocket.bind((address,port))
    except socket.error as e:
        print(str(e))

    mySocket.listen(5)

    print " Server Started"
    while True:
        connection, addr = mySocket.accept()
        dataConnection, dataaddr = mySocket.accept()
        print "client connected ip:<" + str(addr) + ">"

        cThread = threading.Thread(target=client, args=("Thread",connection,dataConnection))
        cThread.start()

    mySocket.close()

if __name__ == '__main__':
    Main()