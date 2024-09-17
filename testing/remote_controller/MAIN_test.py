from bluetooth import *

# Define the port
port = 1

# Create a Bluetooth socket
server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", port))
server_sock.listen(1)

print("Waiting for a connection on RFCOMM channel %d" % port)

# Accept a connection
client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)

try:
    # Receive the message
    data = client_sock.recv(1024)
    print("Received message:", data.decode("utf-8"))

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the sockets
    client_sock.close()
    server_sock.close()
