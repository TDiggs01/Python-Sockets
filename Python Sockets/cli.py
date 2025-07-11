# Client code
# Connecting to the local host server as a client
import socket
import os
import sys

# Command line checks
if len(sys.argv) < 2:
    print("USAGE python " + sys.argv[0] + " <FILE NAME>")
    sys.exit(1)

# Name and port number of the server to want to connect.
serverName = sys.argv[1]
serverPort = int(sys.argv[2])


# Create a socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the server
clientSocket.connect((serverName, serverPort))
print(clientSocket.recv(17).decode())

def sendAll(clientSocket, encoded_data_):
    # bytes sent
    bytesSent = 0
    # Keep sending bytes until all bytes are sent
    while bytesSent < len(encoded_data_):
        bytesSent += clientSocket.send(encoded_data_[bytesSent:])

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

def sendFile(objFile):
    while True:
        # Read 65536 bytes of data
        fileData = objFile.read(65536)

        # Make sure we did not hit EOF
        if not fileData:
            break

        # The file has been read. We are done
        sendAll(fileData.encode())
    print("Sent file.")

def sendCommand(sock, command):
    encoded = command.encode()
    header = f"{len(encoded):010}".encode()
    sendAll(sock, header)
    sendAll(sock, encoded)

def uploadFile(sock, filename):
    if not os.path.exists(filename):
        print(f"File '{filename}' does not exist.")
        return

    sendCommand(sock, f"put {filename}")
    encodedName = filename.encode()
    sock.send(f"{len(encodedName):010}".encode())
    sock.send(encodedName)

    with open(filename, "rb") as f:
        fileData = f.read()

    print(f"Uploading '{filename}' ({len(fileData)} bytes)...")
    sock.send(f"{len(fileData):010}".encode())
    sendAll(sock, fileData)
    print(f"Uploaded '{filename}'")

def downloadFile(sock, filename):
    sendCommand(sock, f"get {filename}")
    status = sock.recv(2).decode()
    if status == "OK":
        fileSize = int(recvAll(sock, 10).decode())
        fileData = recvAll(sock, fileSize)
        with open(filename, "wb") as f:
            f.write(fileData)
        print(f"Downloaded '{filename}' ({fileSize} bytes)")
    else:
        print(f"File '{filename}' not found on server.")

def listFiles(sock):
    sendCommand(sock, "ls")
    fileListSize = int(recvAll(sock, 10).decode())
    fileList = recvAll(sock, fileListSize).decode()
    print(fileList)



try:
    while True:
        command = input("ftp> ").strip()
        if not command:
            continue

        parts = command.split(maxsplit=1)
        action = parts[0]
        argument = parts[1] if len(parts) > 1 else ""

        match action:
            case "put":
                uploadFile(clientSocket, argument)
            case "get":
                downloadFile(clientSocket, argument)
            case "ls":
                listFiles(clientSocket)
            case "quit":
                sendCommand(clientSocket, "quit")
                break
            case _:
                print("Invalid command. Try: get, put, ls, quit.")
except Exception as e:
    print("Error:", e)

clientSocket.close()
