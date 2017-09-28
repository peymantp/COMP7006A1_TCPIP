//This is the server side
/*
Objective: Starts the server, allows in max of 5 connections. Client makes the request to connect to server. Once validated, client makes a request
to retrieve a file. Server acknowledges that request and then submits the file to client.

Server Purpose:
	=> Create a socket with the socket()
	=> Bind the socket to an address using the bind()
	=> Listen for connections with the Listener()
	=> Accept a connection with the accept()
	=> Send and receive data, using the read() and write() system calls
*/

#include <stdio.h>
#include <sys/types.h>	
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <strings.h>
#include <arpa/inet.h>
#include <unistd.h>

#define SERVER_TCP_PORT 7005 //default port
#define BUFLEN 80 //defining the buffer length to be a max of 80bits per reading
#define TRUE 1


//AF_NET defines what it'll be listenting to which are IPv4 addresses and only follows this kind of protocols
//sock_stream defines which transport protocol we'll be following which in this case will be TCP
//while (true) is an infinite loop that keeps the server running with minimal delays

int main(int argc, char **argv){

	int	n, bytes_to_read;
	int	sd, new_sd, client_len, port;
	struct	sockaddr_in server, client;
	char	*bp, *filePath, buf[BUFLEN];

	switch(argc)
	{
		case 1:
			port = SERVER_TCP_PORT;	// Use the default port
		break;
		case 2:
			port = atoi(argv[1]);	// Get user specified port
		break;
		default:
			fprintf(stderr, "Usage: %s [port]\n", argv[0]);
			exit(1);
	}

	//this creates a socket stream and then from there we bind it
	//socket() takes in 3 arguments: a) defines the internet protocol of IPv4, b)specifies the transport layer we want to follow TCP,
	//c) is generally left at 0 for the kernal to use the defaulted connection which is alway TCP since it's most reliable
	if ((sd = socket(AF_NET, SOCK_STREAM, 0)) == 1)
	{
		perror("Can't create socket"); //will terminate if socket can't get a proper connection
		exit(1);
	}

	//Now we have to bind the address with the port
	bzero((char *)&server, sizeof(struct sockaddr_in)); //this sets all values in the buffer to zero  sockaddr_in is a socket structure we must follow
	server.sin_family = AF_NET;
	server.sin_port = htons(port);
	server.sin_addr.s_addr = htonl(INADDR_ANY); // Accept connections from any client

	if (bind(sd, (struct sockaddr *)&server, sizeof(server)) == -1)
	{
		perror("Can't bind name to socket");
		exit(1);
	}

	// Listen for connections
	// queue up to 5 connect requests
	listen(sd, 5);

	//this while loops is an infinite loop keeping the server running all the time with no delays
	while (TRUE)
	{
		client_len= sizeof(client);
		if ((new_sd = accept (sd, (struct sockaddr *)&client, &client_len)) == -1)
		{
			fprintf(stderr, "Can't accept client\n");
			exit(1);
		}

		printf(" Remote Address:  %s\n", inet_ntoa(client.sin_addr));
		bp = buf;
		bytes_to_read = BUFLEN;
		while ((n = recv (new_sd, bp, bytes_to_read, 0)) < BUFLEN)
		{
			bp += n;
			bytes_to_read -= n;
		}

		/*
		new_sd => specifies socket file descriptor/the connected socket
		bd => points to a buffer where the message should be stored
		bytes_to_read =>specifies the length in bytes if the buffer pointed to by the buffer argument
		converts the Internet host address cp from the IPv4 numbers-and-dots notation into binary form (in network byte order)
		*/

		printf(" Remote Address:  %s\n", inet_ntoa(client.sin_addr));
		bp = buf;
		bytes_to_read = BUFLEN;
		while ((n = recv (new_sd, bp, bytes_to_read, 0)) < BUFLEN) //reads the message
		{
			bp += n;
			bytes_to_read -= n;
		}
		printf ("sending:%s\n", buf);

		/*	use strcmp to compare first 3 characters of message. Should be "get" once it matches, then you open the file
			Read Command Given
			Return Command Request
			Close the connection

			Use FILE *fp; => this
			fp = fopen("C:\\dasdsad.txt", "w"); => sets it in write mode
			read the file
		*/

		char *msgIwant = "get";
		if (strcmp(msgIwant,buf,3)=1){
			//get the file and prepare to send
			FILE *fp;
			filePath = "/root/Documents/testFile.txt";
			fp = fopen(filePath,"rw");
			if(fp == NULL){
				printf("Error: Failed to send: ");
			}

			//if (send(new_sd,))
			//fscanf(fp,"%s",buf);
			//write(new_sd,buffer,100);
			//printf("the file was sent successfully");
			//send(new_sd,);
		}

		//send(new_sd, buf, BUFLEN, 0);
		close(new_sd); //closes the connection
	}
	close(sd);
	return(0);
}
