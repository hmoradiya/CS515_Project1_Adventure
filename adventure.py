import json
import time


# Define the player's starting location and inventory
player_location = 0
player_inventory = []

# Load the map data from the JSON string in the file
# Opening JSON file
with open('loop.map') as f:
    # Load the JSON data as a string
    json_str = f.read()

# Parse the JSON data as an array
map_data = json.loads(json_str)

# Helper function to look up a room by ID


def get_room(room_id):
    return map_data[str(room_id)]

# Helper function to print the current room's description and exits


def print_room(room):
    print("> " + room["name"])
    print(room["desc"])
    if room.get("exits") and len(room["exits"]) > 0:
        print("Exits: " + ", ".join(room["exits"].keys()))
    if room.get("items") and len(room["items"]) > 0:
        print("Items: " + ", ".join(room["items"]))


# Print the starting room's description
current_room = get_room(player_location)
print_room(current_room)

# Define a function to print the list of valid verbs


def print_valid_verbs():
    valid_verbs = ["go", "get", "drop", "drop_all",
                   "look", "inventory", "quit", "help"]
    print("You can run the following commands:")
    for verb in valid_verbs:
        if verb == "get":
            print("  get <item>")
        elif verb == "drop":
            print("  drop <item>")
        elif verb == "go":
            print("  go <direction>")
        else:
            print("  " + verb)


# Game loop
while True:
    # Read player input and split it into words
    command = input("What would you like to do? ").strip().lower().split()

    # Handle empty input
    if not command:
        continue

    # Parse the verb and any additional arguments
    verb = command[0]
    args = command[1:]

    # Define a variable to keep track of the start time
    start_time = time.time()

    weapon_used = False

    # Handle the "go" verb
    if verb == "go":
        direction = " ".join(args)

        if verb == "go" and direction == "school_exit":
            if "key" not in player_inventory:
                print("You need the key to unlock School exit gate.")
            else:
                print("You use the key to unlock School exit gate.")
                player_location = current_room["exits"][direction]
                current_room = get_room(player_location)

                if "student_5" in player_inventory:
                    print("Congratulations! you saved students!")
                    print("Thanks for playing!")
                    break
                else:
                    print("You have failed to save students. You lose!")
                    print("Try Again!")
                    break

        else:
            if direction in current_room["exits"]:
                player_location = current_room["exits"][direction]
                current_room = get_room(player_location)
                print_room(current_room)

            else:
                print("There's no way to go " + direction + ".")

    # Handle the "look" verb
    elif verb == "look":
        print_room(current_room)

    # Handle the "get" verb
    elif verb == "get":
        item_name = " ".join(args)
        if item_name in current_room.get("items", []):
            player_inventory.append(item_name)
            current_room["items"].remove(item_name)
            print("You get the " + item_name + ".")
        else:
            print("There's no " + item_name + " here.")

    # Handle the "drop" verb
    elif verb == "drop":
        if player_inventory != 0:
            player_inventory.remove(item_name)
            current_room["items"].append(item_name)
            print("You drop the " + item_name + ".")
        else:
            print("There's no " + item_name + " here.")

    # Handle the "drop all" verb
    elif verb == "drop_all":
        if len(player_inventory) == 0:
            print("You're not carrying anything to drop.")
        else:
            for item_name in player_inventory:
                current_room["items"].append(item_name)
            player_inventory = []
            print("You drop all of your items.")

    # Handle the "inventory" verb
    elif verb == "inventory":
        if not player_inventory:
            print("You're not carrying anything.")
        else:
            print("You're carrying: " + ", ".join(player_inventory))

    elif verb == "help":
        print_valid_verbs()

    # Handle the "quit" verb
    elif verb == "quit":
        print("Thanks for playing!")
        break

    # Handle unknown verbs
    else:
        print("I don't know how to " + verb + ".")
