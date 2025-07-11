# Server code
import socket
import os

# The port on which to listen
serverPort = 12000

# Create a TCP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
serverSocket.bind(('0.0.0.0', serverPort))
# Start listening for incoming connections
serverSocket.listen(5)

# Receives all data sent by sender/client with n number of bytes
def recvAll(sock, numBytes):
    recvBuff = b''

    while len(recvBuff) < numBytes:
        # Receive whatever the newly connected client has to send
        tmpBuff = sock.recv(numBytes - len(recvBuff))

        # When the other side unexpectedly closed its socket.
        if not tmpBuff:
            break

        # Receive whatever the newly connected client has to send
        recvBuff += tmpBuff
    return recvBuff

def handleClient(connectionSocket):


    while True:
        header = recvAll(connectionSocket, 10)
        if not header:
            break
        commandLength = int(header.decode())
        command = recvAll(connectionSocket, commandLength).decode()
        print(f"Command received: {command}")

        parts = command.split(maxsplit=1)
        action = parts[0]
        arg = parts[1] if len(parts) > 1 else ""

        match action:
            case "put":
                filenameSizeBuffer = recvAll(connectionSocket, 10)
                filenameSize = int(filenameSizeBuffer.decode())
                filename = recvAll(connectionSocket, filenameSize).decode()
                fileSizeBuffer = recvAll(connectionSocket, 10)
                fileSize = int(fileSizeBuffer.decode())
                data = recvAll(connectionSocket, fileSize)
                with open("received_" + filename, "wb") as f:
                    f.write(data)
                print(f"Received file: {filename}")
                print(f"File size: {fileSize} bytes")
                print(filename, "data contents: \n", data.decode())

            case "get":
                if os.path.exists(arg):
                    connectionSocket.send("OK".encode())
                    fileSize = os.path.getsize(arg)
                    connectionSocket.send(f"{fileSize:010}".encode())
                    with open(arg, "rb") as f:
                        connectionSocket.sendall(f.read())
                else:
                    connectionSocket.send("NF".encode())  # Not Found

            case "ls":
                files = os.listdir()
                listing = "\n".join(files)
                listingBytes = listing.encode()
                connectionSocket.send(f"{len(listingBytes):010}".encode())
                connectionSocket.sendall(listingBytes)

            case "quit":
                print("Client requested disconnect.")
                break

            case _:
                print("Unknown command.")

    connectionSocket.close()


def getClientFile():
    # Receive the name of the sent file
    filenameSizeBuffer = recvAll(connectionSocket, 10)
    filenameSize = int(filenameSizeBuffer.decode())

    filename = recvAll(connectionSocket, filenameSize).decode()
    print(f"Receiving file: {filename}")

    # Receive the first 10 bytes from client stating number of bytes sending
    fileSizeBuffer = recvAll(connectionSocket, 10)
    fileSize = int(fileSizeBuffer.decode())
    print(f"File size: {fileSize} bytes")

    data = recvAll(connectionSocket, fileSize)
    with open("received_" + filename, "wb") as f:
        f.write(data)
    print(filename, "data contents: \n", data.decode())



print('The server is ready to receive')
try:
# Forever accept incoming connections
    while 1:
        print('Waiting for connections...')

        # Accept a connection ; get client’s socket
        connectionSocket, addr = serverSocket.accept()
        print("Accepted connection from client: ", addr)
        print("\n")

        connectionSocket.send('Hello from server'.encode())
        handleClient(connectionSocket)
        # getClientFile()
except KeyboardInterrupt:
    print("\nServer shutting down...")

# Close Socket
connectionSocket.close()
