# Chore Randomizer Program (History Tracking Version)
# Adam Flick
# December 2024

import random
import json
import os

# Empty list of chores and family members
chores = []
family_members = []
chore_history = []

# Function to get the directory for storage
def get_storage_directory():
    # For local testing, we can use the "user files" folder
    # For web apps or mobile apps, we will adapt the logic here later
    current_directory = os.getcwd()
    user_files_directory = os.path.join(current_directory, 'user files')
    
    # Ensure the "user files" directory exists, create it if not
    if not os.path.exists(user_files_directory):
        os.makedirs(user_files_directory)

    return user_files_directory

# Function to save data to a file
def save_data(filename="chore_data.json"):
    # Get the storage directory (local for now)
    storage_directory = get_storage_directory()
    filepath = os.path.join(storage_directory, filename)
    
    data = {
        "chores": chores,
        "family_members": family_members,
        "chore_history": chore_history  # Include chore history in the saved data
    }
    
    try:
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {filepath}.")
    except Exception as e:
        print(f"Error saving data: {e}")

# Function to load data from a file
def load_data(filename="chore_data.json"):
    global chores, family_members, chore_history
    # Get the storage directory (local for now)
    storage_directory = get_storage_directory()
    filepath = os.path.join(storage_directory, filename)

    try:
        with open(filepath, "r") as file:
            data = json.load(file)
            chores = data.get("chores", [])
            family_members = data.get("family_members", [])
            chore_history = data.get("chore_history", [])  # Load chore history
            print(f"Data loaded from {filepath}.")
    except FileNotFoundError:
        print(f"No saved data found. Starting with empty lists.")
    except Exception as e:
        print(f"Error loading data: {e}")

# Function to edit an item in a list
def edit_item(item_list, list_name):
    if not item_list:
        print(f"No {list_name} to edit.")
        return
    print(f"Current {list_name}:")
    for index, item in enumerate(item_list, start=1):
        print(f"{index}. {item}")
    try:
        choice = int(input(f"Select a {list_name[:-1]} to edit (1-{len(item_list)}): ")) - 1
        if 0 <= choice < len(item_list):
            new_item = input(f"Enter the new value for {item_list[choice]}: ").strip()
            if new_item:
                item_list[choice] = new_item
                print(f"{list_name[:-1].capitalize()} updated successfully.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Function to delete an item from a list
def delete_item(item_list, list_name):
    if not item_list:
        print(f"No {list_name} to delete.")
        return
    print(f"Current {list_name}:")
    for index, item in enumerate(item_list, start=1):
        print(f"{index}. {item}")
    try:
        choice = int(input(f"Select a {list_name[:-1]} to delete (1-{len(item_list)}): ")) - 1
        if 0 <= choice < len(item_list):
            removed_item = item_list.pop(choice)
            print(f"{removed_item} removed from {list_name}.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Function to add user-defined chores
def add_custom_chores():
  print("Enter your chores one at a time. Type 'done' when finished:")
  while True:
    custom_chore = input("Add a chore: ").strip()
    if custom_chore.lower() == "done":
      break
    elif custom_chore:
      chores.append(custom_chore)
      print(f"Added chore: {custom_chore}")

# Function to add family members
def add_family_members():
  print("Enter family member names one at a time. Type 'done' when finished:")
  while True:
    name = input("Add a name: ").strip()
    if name.lower() == "done":
      break
    elif name:
      family_members.append(name)
      print(f"Added family member: {name}")

# Function to randomly assign chores without repeating recent ones
def assign_chores():
    global chore_history  # Reference the global chore_history variable
    if chores and family_members:
        random.shuffle(chores)  # Shuffle chores for randomness
        for member in family_members:
            if chores:
                # Find a chore that hasn't been assigned recently
                assigned_chore = None
                for chore in chores:
                    if not any(member in history and chore == history[1] for history in chore_history):
                        assigned_chore = chore
                        break
                if assigned_chore:
                    chores.remove(assigned_chore)  # Remove the assigned chore from the list
                    chore_history.append((member, assigned_chore))  # Record the assignment
                    print(f"{member}'s chore is: {assigned_chore}")
                else:
                    print(f"No unique chore available for {member}, assigning randomly!")
                    assigned_chore = chores.pop(0)
                    chore_history.append((member, assigned_chore))
                    print(f"{member}'s chore is: {assigned_chore}")
            else:
                print(f"No more chores left for {member}!")  # Runs once chore list is empty
    elif chores and not family_members:
        print("No family members were added. Here's a random chore you can do yourself:")
        print(f"Random chore: {random.choice(chores)}")
    else:
        print("Either no chores or no family members were added. Please try again.")

# Load data on startup
load_data()

# Main program
while True:
    print("\nChoose an option:")
    print("1. Add chores")
    print("2. Add family members")
    print("3. View chores and family members")
    print("4. Edit chores")
    print("5. Edit family members")
    print("6. Delete chores")
    print("7. Delete family members")
    print("8. Randomly assign chores")
    print("9. Save and exit")
    choice = input("Enter your choice #: ").strip()

    if choice == "1":
        add_custom_chores()
    elif choice == "2":
        add_family_members()
    elif choice == "3":
        print(f"Chores: {chores}")
        print(f"Family Members: {family_members}")
    elif choice == "4":
        edit_item(chores, "chores")
    elif choice == "5":
        edit_item(family_members, "family members")
    elif choice == "6":
        delete_item(chores, "chores")
    elif choice == "7":
        delete_item(family_members, "family members")
    elif choice == "8":
        # Randomly assign chores to family members, making sure the same chore isn't repeated
        if chores and family_members:
            assign_chores()  # Call the new function that handles chore assignment with history
        elif chores and not family_members:
            print("No family members were added. Here's a random chore you can do yourself:")
            print(f"Random chore: {random.choice(chores)}")
        else:
            print("Either no chores or no family members were added. Please try again.")
            
    elif choice == "9":
        save_data()
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")



