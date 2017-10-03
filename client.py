import socket
import os
from os import path

def Main():
    address = socket.gethostbyname(socket.getfqdn()) #selects first non localhost in etc/hosts
    serverAddress = raw_input("Enter server IP>")
    msgPort = 7005
    msgSocket = socket.socket()
    msgSocket.connect((serverAddress,msgPort))

    dataPort = 7006
    dataSocket = socket.socket()
    #dataSocket.connect((address,dataPort))
    try:
        dataSocket.bind((address,dataPort))
    except socket.error as e:
        print(str(e))
    dataSocket.listen(1)
    msgSocket.send(address)
    dataConnection, dataaddr = dataSocket.accept()
    print "server connected ip:<" + str(dataaddr) + ">"

    while True:
        command = raw_input("(GET/SEND)?")
        if command == "GET":
            msgSocket.send("GET")

            listOfFiles = msgSocket.recv(1024)
            print str(listOfFiles)

            filename = raw_input("Filename ->")
            msgSocket.send(filename)

            data = msgSocket.recv(1024)
            if data[:6] == 'Geting':
                filesize = long(data[6:])
                message = raw_input("File Exists, " + str(filesize) +\
                "Bytes, download? (Y/N)?")
                if message == 'Y':
                    msgSocket.send('OK')
                    f = open('client_'+filename,'w')
                    data = dataConnection.recv(1024)
                    totalRecv = len(data)
                    f.write(data)
                    while totalRecv < filesize:
                        data = dataConnection.recv(1024)
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
                msgSocket.send("SEND"+filename)

                response = msgSocket.recv(1024)
                if response == "READY":
                    msgSocket.send( str(os.path.getsize(filename)))
                    print "READY"
                with open(filename,'rb') as f:
                    while True:
                        bytesToSend = f.read(1024)
                        dataConnection.send(bytesToSend)
                        if bytesToSend == "":
                            break
                print "Upload Complete"
            else:
                print "No such file found"
        else:
            print "not valid command try again"


if __name__ == '__main__':
    Main()