import os
from utilities import chooser
from data import choices
from operations import operations

# loop until it's done
def run_app():
    # display a list of menu from an array
    user_choice = chooser.selector("Menu Principal", choices)

    # execute a function based on the choice made by the end user
    execute(user_choice)

def execute(choice):
    operations[choice]()
    # os.system('clear')