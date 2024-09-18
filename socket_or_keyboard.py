import zmq
from pynput import keyboard

# Set up the ZeroMQ socket for receiving messages
context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.connect("tcp://localhost:5555")

# Variable to store user input
user_input = None

# List to store the user input buffer
user_input_buffer = []


def on_press(key):
    global user_input_buffer
    try:
        user_input_buffer.append(key.char)
    except AttributeError:
        if key == keyboard.Key.enter:
            global user_input
            user_input = ''.join(user_input_buffer)
            user_input_buffer.clear()

# Function to get the answer from the socket or user input


def get_answer():
    global user_input

    # Create a poller for the socket
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    # Set up keyboard listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    while True:
        socks = dict(poller.poll(100))  # Poll the socket with a short timeout
        if socket in socks and socks[socket] == zmq.POLLIN:
            answer = socket.recv_string()
            print(f"Received answer via socket: {answer}")
            break
        elif user_input is not None:
            print(f"Answer provided via keyboard: {user_input}")
            break

    # Stop the keyboard listener
    listener.stop()

    return answer if user_input is None else user_input


# Example usage
answer = get_answer()
print(f"Selected answer: {answer}")

# Clean up
socket.close()
