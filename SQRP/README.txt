
#This README file provides clear instructions for users on how to run both the server and client, including any dependencies required.



#SQRP (Simple Query-Response Protocol) Client-Server Example

#This example includes server and client code for a simple query-response protocol (SQRP).

# Dependencies
Python 3.x is required to run the code. It may not work with lower versions.

# Running the Server
#To run the server, execute the `server.py` file in your terminal or command prompt. The server listens on localhost at port 31369 by default.

```bash
python server.py

# When the server is started, it will begin listening for incoming connections.

#Running the Client
#To run the client, execute the client.py file in your terminal or command prompt.

python client.py


#When prompted, enter a query type (0, 1, 2, or 3). Then, provide the appropriate arguments for the query (e.g.,file name, directory path).

#Sample Query Types
#0: Query for the existence of a directory
#1: Query for the existence of a file in the specified directory
#2: Query whether a file in the specified directory has changed
#3: Query for the existence of a directory and return the name and creation time of a file
#Note: If the server and client are running on the same machine, you need to run the server and client in different terminals or command prompts.


