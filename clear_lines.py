import time
def clear_lines(num_lines):
    """
    Clears the specified number of lines in the console.

    Args:
        num_lines (int): The number of lines to clear.
    """
    # Move the cursor up by the specified number of lines
    print("\033[F" * num_lines, end="")
    # Clear the lines
    print("\033[K" * num_lines, end="")


print("lines")
print("lines")
print("lines")
print("lines")
time.sleep(4)
clear_lines(4)
print("lines cleared")
