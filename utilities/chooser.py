import questionary
from itertools import zip_longest
from operations import utility_functions
import zmq
from pynput import keyboard

# this function allow the user to select one value using shortcuts


def selector(message, choices):
    choices.append("Retour")
    answer = questionary.rawselect(message=message, choices=choices).ask()
    return answer


def simple_selector(message, socket):
    print(message, end=": ")
    answer = get_answer(socket)
    return answer


def tuple_selector(message, list, socket):
    list_of_tuples = utility_functions.split_list(list)

    # Create a dictionary to map numbers to elements
    element_dict = {}

    fixed_width = 50  # Set the fixed width for each column

    counter = 1
    column1 = []
    column2 = []
    column3 = []
    for items in zip_longest(*list_of_tuples, fillvalue=None):
        item_strs = []
        for item in items:
            if item is not None:
                # Store only the first element of the tuple
                element_dict[counter] = item[0]
                # Display only the second and third elements of the tuple
                display_item = item[1:]
                if counter <= 10:
                    column1.append(
                        f"{counter}. {str(display_item)[:fixed_width]:<{fixed_width}}")
                elif counter <= 20:
                    column2.append(
                        f"{counter}. {str(display_item)[:fixed_width]:<{fixed_width}}")
                else:
                    column3.append(
                        f"{counter}. {str(display_item)[:fixed_width]:<{fixed_width}}")
                counter += 1

    # Print the columns
    for c1, c2, c3 in zip_longest(column1, column2, column3, fillvalue=""):
        print(f"{c1}\t{c2}\t{c3}")

    # Add the additional choice with number 999
    print(f"999. Retour")

    # Ask for user input
    # choice = int(input(message))
    print(message, end="")
    choice = int(get_answer(socket))

    # Return corresponding element
    if choice in element_dict:
        return element_dict[choice]
    elif choice == 999:
        return "Retour"
    else:
        return None


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


def get_answer(socket):
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
