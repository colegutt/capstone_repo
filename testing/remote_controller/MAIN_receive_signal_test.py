from bluetooth import *

# Create a Bluetooth socket
server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

print(f"Waiting for connection on RFCOMM channel {port}")

advertise_service(server_sock, "SampleServer",

                  service_id=uuid.uuid4(),

                  service_classes=[uuid.uuid4(), SERIAL_PORT_CLASS],

                  profiles=[SERIAL_PORT_PROFILE])

client_sock, client_info = server_sock.accept()

print(f"Accepted connection from {client_info}")

try:
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        print(f"Received: {data}")

except IOError:
    pass

print("Disconnected")
client_sock.close()
server_sock.close()