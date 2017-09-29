import socket
import os

def Main():
    port = 7005

    clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    clientSocket.connect((socket.gethostname(),port))

    filename = raw_input("Filename ->")
    if filename != 'q':
        clientSocket.send(filename)
        data = clientSocket.recv(1024)
        if data[:6] == 'Geting':
            filesize = long(data[6:])
            message = raw_input("File Exists, " + str(filesize) +\
            "Bytes, download? (Y/N)?")
            if message == 'Y':
                clientSocket.send('OK')
                f = open('new_'+filename,'wb')
                data.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = clientSocket.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print "{0:.2f}".format((totalRecv/float(filesize))*100) + "% DONE"

                print "Download Complete!"
        else:
            print "File 404"
    clientSocket.close()

if __name__ == '__main__':
    Main()