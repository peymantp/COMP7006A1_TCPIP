import socket
import os
from os import path

def Main():
    port = 7005
    address = raw_input("enter IPv4 of server")
    clientSocket = socket.socket()
    clientSocket.connect((address,port))

    while True:
        command = raw_input("(GET/SEND)?")
        if command == "GET":
            clientSocket.send("GET")

            listOfFiles = clientSocket.recv(1024)
            print str(listOfFiles)

            filename = raw_input("Filename ->")
            clientSocket.send(filename)

            data = clientSocket.recv(1024)
            if data[:6] == 'Geting':
                filesize = long(data[6:])
                message = raw_input("File Exists, " + str(filesize) +\
                "Bytes, download? (Y/N)?")
                if message == 'Y':
                    clientSocket.send('OK')
                    f = open('client_'+filename,'w')
                    data = clientSocket.recv(1024)
                    totalRecv = len(data)
                    f.write(data)
                    while totalRecv < filesize:
                        data = clientSocket.recv(1024)
                        totalRecv += len(data)
                        f.write(data)
                        print "{0:.2f}".format((totalRecv/float(filesize))*100) + "% DONE"

                    print "Download Complete!"
                    f.close()
            else:
                print "File 404"
        elif command == "SEND":
            files = filter(path.isfile, os.listdir("./"))
            print str(files)
            filename = raw_input("Filename ->")
            if path.isfile(filename):
                clientSocket.send("SEND"+filename)

                response = clientSocket.recv(1024)
                if response == "READY":
                    clientSocket.send( str(os.path.getsize(filename)))
                    print "READY"
                with open(filename,'rb') as f:
                    while True:
                        bytesToSend = f.read(1024)
                        clientSocket.send(bytesToSend)
                        if bytesToSend == "":
                            clientSocket.send("OK")
                            break
            else:
                print "No such file found"
        else:
            print "not valid command try again"


if __name__ == '__main__':
    Main()