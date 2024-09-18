import questionary
from itertools import zip_longest
from operations import utility_functions

# this function allow the user to select one value using shortcuts


def selector(message, choices):
    answer = questionary.rawselect(message=message, choices=choices).ask()
    return answer

# def tuple_selector(message, list):

#     list_of_tuples = utility_functions.split_list(list)

#     # Create a dictionary to map numbers to elements
#     element_dict = {}

#     fixed_width = 50  # Set the fixed width for each column

#     counter = 1
#     for items in zip_longest(*list_of_tuples, fillvalue=None):
#         item_strs = []
#         for item in items:
#             if item is not None:
#                 element_dict[counter] = item[0]  # Store only the first element of the tuple
#                 display_item = item[1:]  # Display only the second and third elements of the tuple
#                 item_strs.append(f"{counter}. {str(display_item)[:fixed_width]:<{fixed_width}}")
#                 counter += 1
#             else:
#                 item_strs.append(' ' * fixed_width)

#         print("\t".join(item_strs))

#     # Ask for user input
#     # import pdb; pdb.set_trace()
#     choice = int(input(message))

#     # Return corresponding element
#     if choice in element_dict:
#         # print(f"Your chosen element is: {element_dict[choice]}")
#         return element_dict[choice]
#     else:
#         # print("Invalid choice.")
#         return None


# def tuple_selector(message, list):
#     print(list)
#     list_of_tuples = utility_functions.split_list(list)

#     # Create a dictionary to map numbers to elements
#     element_dict = {}

#     fixed_width = 50  # Set the fixed width for each column

#     counter = 1
#     for items in zip_longest(*list_of_tuples, fillvalue=None):
#         item_strs = []
#         for item in items:
#             if item is not None:
#                 # Store only the first element of the tuple
#                 element_dict[counter] = item[0]
#                 # Display only the second and third elements of the tuple
#                 display_item = item[1:]
#                 item_strs.append(
#                     f"{counter}. {str(display_item)[:fixed_width]:<{fixed_width}}")
#                 counter += 1
#             else:
#                 item_strs.append(' ' * fixed_width)

#         print("\t".join(item_strs))

#     # Add the additional choice with number 999
#     print(f"999. Retour")

#     # Ask for user input
#     choice = int(input(message))

#     # Return corresponding element
#     if choice in element_dict:
#         return element_dict[choice]
#     elif choice == 999:
#         return "Retour"
#     else:
#         return None

def tuple_selector(message, list):
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
    choice = int(input(message))

    # Return corresponding element
    if choice in element_dict:
        return element_dict[choice]
    elif choice == 999:
        return "Retour"
    else:
        return None
