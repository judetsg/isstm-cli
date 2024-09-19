import questionary
from itertools import zip_longest
from operations import utility_functions
import zmq
from pynput import keyboard
import re
import time


def natural_sort_key(string):
    return [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', string)]


def selector(message, choices):
    choices.append("Retour")
    answer = questionary.rawselect(message=message, choices=choices).ask()
    return answer


def simple_selector(message, socket):
    print(message)
    time.sleep(1)
    answer = get_answer(socket)
    return answer


def displayer(list):
    sorted_list = sorted(list, key=lambda x: natural_sort_key(x[1]))
    # Calculate the length of each column
    [l1, l2, l3] = divide_by_three(len(sorted_list))

    # Create a dictionary to map numbers to elements
    element_dict = {}

    fixed_width = 50  # Set the fixed width for each column

    column1 = [f"{i+1}. {str(item[1:])[0:fixed_width]:<{fixed_width}}" for i,
               item in enumerate(sorted_list[:l1])]
    column2 = [f"{i+1+l1}. {str(item[1:])[0:fixed_width]:<{fixed_width}}" for i,
               item in enumerate(sorted_list[l1:l1+l2])]
    column3 = [f"{i+1+l1+l2}. {str(item[1:])[0:fixed_width]:<{fixed_width}}" for i,
               item in enumerate(sorted_list[l1+l2:])]

    # Store the mapping between counter and tuple element
    for i, item in enumerate(sorted_list):
        element_dict[i+1] = [item[0], item[1]]

    # Print the columns
    for c1, c2, c3 in zip_longest(column1, column2, column3, fillvalue=""):
        print(f"{c1}\t{c2}\t{c3}")

    # Add the additional choice with number 999
    print(f"999. Retour")


def tuple_selector(message, list, socket, type):
    # Sort the list of tuples based on the natural order of the second element of each tuple
    sorted_list = sorted(list, key=lambda x: natural_sort_key(x[1]))
    # print(sorted_list)

    # Calculate the length of each column
    # [l1, l2, l3] = divide_by_three(len(sorted_list))

    # Create a dictionary to map numbers to elements
    element_dict = {}

    # fixed_width = 50  # Set the fixed width for each column

    # column1 = [f"{i+1}. {str(item[1:])[0:fixed_width]:<{fixed_width}}" for i,
    #            item in enumerate(sorted_list[:l1])]
    # column2 = [f"{i+1+l1}. {str(item[1:])[0:fixed_width]:<{fixed_width}}" for i,
    #            item in enumerate(sorted_list[l1:l1+l2])]
    # column3 = [f"{i+1+l1+l2}. {str(item[1:])[0:fixed_width]:<{fixed_width}}" for i,
    #            item in enumerate(sorted_list[l1+l2:])]

    # Store the mapping between counter and tuple element
    for i, item in enumerate(sorted_list):
        element_dict[i+1] = [item[0], item[1]]

    # Print the columns
    # for c1, c2, c3 in zip_longest(column1, column2, column3, fillvalue=""):
    #     print(f"{c1}\t{c2}\t{c3}")

    # Add the additional choice with number 999
    # print(f"999. Retour")
    print(message)

    # If order is False, I want the counter to be automatically entered
    # in the case of a grade entry for example, the 'anonymat'is supposed to be ordered already so
    # we just enter the grade
    if type == "note":
        for anonymat_index in range(len(sorted_list)):
            print("Anonymat: ", sorted_list[anonymat_index][1])
            return sorted_list[anonymat_index][0]
    if type == "anonymat":
        # Ask for user input
        # choice = int(input(message))
        choice = int(get_answer(socket))
        if choice == 999:
            return "Retour"
        elif choice in element_dict:
            print(element_dict[choice][1])
            time.sleep(1)
            return element_dict[choice][0]
    if type == "cc":
        # choose student
        choice = int(get_answer(socket))
        if choice == 999:
            return "Retour"
        elif choice in element_dict:
            print(element_dict[choice][1])
            time.sleep(1)
            return element_dict[choice][0]


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
    # listener = keyboard.Listener(on_press=on_press)
    # listener.start()
    # print(message, end=": ")
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
    # listener.stop()

    return answer if user_input is None else user_input

# Just a utility function to diplay a list by 3 columns


def divide_by_three(n):
    quotient = n // 3
    remainder = n % 3

    if remainder == 0:
        return [quotient, quotient, quotient]
    else:
        return [quotient + 1, quotient + 1, n - (2 * (quotient + 1))]
