Python File Transfer System (Client–Server)
This project implements a simple file transfer system using Python sockets. It allows a client to connect to a server, upload and download files, list available files, and gracefully disconnect. The system mimics basic FTP (File Transfer Protocol) functionality using TCP connections.

How to Execute the Program
1. Clone the repository
git clone https://github.com/<your-username>/python-file-transfer.git
cd python-file-transfer

2. Run the Server
Start the server on a host machine (or localhost):
python server.py

By default, the server listens on port 12000 and accepts multiple client connections sequentially.
You should see:
The server is ready to receive
Waiting for connections...

3. Run the Client
On another terminal (or another machine on the same network):
python client.py <SERVER_IP> 12000

Example:
python client.py 127.0.0.1 12000

You should see:
Hello from server
ftp>

Use the following FTP-like commands at the prompt:
    ftp> put <filename>
      - Uploads a file to the server using a separate data connection.

   ftp> get <filename>
      - Downloads a file from the server using a separate data connection.

   ftp> ls
      - Lists files in the server's directory via a data connection.

   ftp> quit
      - Disconnects from the server.
