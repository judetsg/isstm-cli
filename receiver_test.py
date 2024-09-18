import zmq

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.connect("tcp://localhost:5555")

while True:
    message = socket.recv_string()
    if not message:
        break
    print(f"Received: {message}")

socket.close()
