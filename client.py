import socket
import os
from os import path

def Main():
    address = '127.0.1.1'
    msgPort = 7005
    msgSocket = socket.socket()
    msgSocket.connect((address,msgPort))

    dataPort = 7005
    dataSocket = socket.socket()
    dataSocket.connect((address,dataPort))

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
                    data = dataSocket.recv(1024)
                    totalRecv = len(data)
                    f.write(data)
                    while totalRecv < filesize:
                        data = dataSocket.recv(1024)
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
                        dataSocket.send(bytesToSend)
                        if bytesToSend == "":
                            break
                print "Upload Complete"
            else:
                print "No such file found"
        else:
            print "not valid command try again"


if __name__ == '__main__':
    Main()