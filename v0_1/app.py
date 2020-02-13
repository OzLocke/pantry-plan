## Pantry Plan V0.1 App ##
## Takes user input and logs to CSV, tracks contents of pantry ##

import csv, os

# set up directory
dirname = os.path.dirname(__file__)
data_file = os.path.join(dirname, 'pantryplan.csv')

# set up variables
pantry = []
headers = ["item", "unit", "quantity"]

# Load in existing pantry data
with open(data_file) as pantry_csv:
    print("SYSTEM: Reading file pantryplan.csv")
    reader = csv.DictReader(pantry_csv)
    for row in reader:
        # Bring in row as a dict
        pantry_item = {}
        pantry_item.update(row)
        # And then append the dict to the pantry list
        pantry.append(pantry_item)
    print("Finished reading file\n---------------------")

# Set up functions
def user_input():
    user_choice = int(input("What would you like to do?\n1 - Review Pantry Contents\n2 - Update Pantry\n3 - Quit\n\n"))

    if user_choice == 1:
        display_pantry()
        user_input()
    if user_choice == 2:
        update_pantry()
        user_input()
    if user_choice == 3:
        print("\nGoodbye!")

def display_pantry():
    global pantry
    print("\nOK, here' the current pantry list:\n\nItem | Unit | Quantity")
    for item in pantry:
        print("{item} | {unit} | {quantity}".format(item=item["item"], unit=item["unit"], quantity=item["quantity"]))
    print("---------------------\n")

def update_pantry():
    more = "y"
    while more == "y":
        # Take input for each dictionary value
        item = input("\nWhat is the item called?\n\n")
        unit = input("\nWhat unit should I store the item as?\n\n")
        quantity = input("\nWhat quantity of this item should I store?\n\n")

        if any(entry["item"] == item for entry in pantry):
            item_index = next((index for (index, entry) in enumerate(pantry) if entry["item"] == item), None)
            if pantry[item_index]["unit"] == unit:
                pantry_quantity = int(pantry[item_index]["quantity"])
                pantry_quantity += int(quantity)
                pantry[item_index]["quantity"] = str(pantry_quantity)
            else:
                # Build dictionary and add to pantry list
                new_entry = {"item": item, "unit": unit, "quantity": quantity}
                pantry.append(new_entry)
        else:
            # Build dictionary and add to pantry list
            new_entry = {"item": item, "unit": unit, "quantity": quantity}
            pantry.append(new_entry)

        # Check for continue
        more = input("\nWould you like to add another item? (y or n)\n\n")
    
    # Overwrite CSV
    with open(data_file, "w", newline="") as pantry_csv:
        print("SYSTEM: Writing to file pantryplan.csv")
        writer = csv.DictWriter(pantry_csv, fieldnames=headers)
        writer.writeheader()
        for item in pantry:
            writer.writerow(item)
        print("Finished writing to file\n---------------------")





# Begin interaction
print("Welcome to Pantry Plan 0.1")
user_input()

