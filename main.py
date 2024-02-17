import signal
from contextlib import contextmanager
import sys

# A context manager to handle the alarm signal for a timeout
@contextmanager
def timeout(time):
    # Signal handler for the alarm
    def raise_timeout(signum, frame):
        raise TimeoutError

    signal.signal(signal.SIGALRM, raise_timeout)  # Set the signal handler
    signal.alarm(time)  # Set the alarm for `time` seconds

    try:
        yield
    finally:
        signal.alarm(0)  # Cancel the alarm

# Updated make_choice function with a 60-second wait for valid input
def make_choice(prompt, choices):
    try:
        with timeout(60):  # Set the timeout context for 60 seconds
            while True:  # Keep asking until a valid response or timeout
                response = input(prompt).lower()
                if response in choices:
                    return response
                print(f"Invalid choice. The valid options are: {', '.join(choices)}. Please try again.")
    except TimeoutError:
        print("No valid response in 60 seconds. Goodbye.")
        sys.exit()  # Exit the program after timeout
    
def start_game():
    print("Welcome to Treasure Island.")
    print("Your mission is to find the treasure.")
    
    direction = make_choice("You're at a crossroad. Where do you want to go? Type 'left' or 'right'\n", ["right", "left"])
    
    if direction == "left":
        return "You fell into a hole. Game Over"

    action = make_choice("You come to a lake. There is an island in the middle of the lake. Type 'wait' to wait for a boat. Type 'swim' to swim across.\n", ["wait", "swim"])
    
    if action == "swim":
        return "You get attacked by an angry trout. Game Over."

    door_color = make_choice("You arrive at the island unharmed. There is a house with 3 doors. One red, one yellow and one blue. Which colour do you choose?\n", ["red", "yellow", "blue"])
    
    if door_color in ["red", "blue"]:
        return "It's a room full of fire. Game Over."
    elif door_color == "yellow":
        return "You found the treasure! You Win!"

if __name__ == "__main__":
    result = start_game()
    print(result)