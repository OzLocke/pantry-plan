## Pantry Plan V0.1 Script ##

import csv, os

class UserInput:
    def __init__(self, pantry):
        self.pantry_instance = pantry
    
    def __repr__(self):
        return "an instance of the UserInput functional class"

    def user_input(self):
        user_choice = int(input("What would you like to do?\n1 - Review Pantry Contents\n2 - Update Pantry\n3 - Quit\n\n"))

        # Call methods from linked pantry instance based on user input
        if user_choice == 1:
            self.pantry_instance.display_pantry()
            self.user_input()
        if user_choice == 2:
            self.pantry_instance.update_pantry()
            self.user_input()
        if user_choice == 3:
            print("\nGoodbye!")

class Pantry:
    def __init__(self):
        # set up directory
        self.dirname = os.path.dirname(__file__)
        self.data_file = os.path.join(self.dirname, 'pantryplan.csv')

        # set up variables
        self.pantry = []

        # Load in existing pantry data
        with open(self.data_file) as pantry_csv:
            print("SYSTEM: Reading file pantryplan.csv")
            reader = csv.DictReader(pantry_csv)
            for row in reader:
                # Bring in row as a dict
                pantry_item = {}
                pantry_item.update(row)
                # And then append the dict to the pantry list
                self.pantry.append(pantry_item)
            print("Finished reading file\n---------------------")

    def __repr__(self):
        return "an instance of the Pantry functional class"

    def display_pantry(self):
        print("\nOK, here' the current pantry list:\n\nItem | Unit | Quantity")
        for item in self.pantry:
            print("{item} | {unit} | {quantity}".format(item=item["item"], unit=item["unit"], quantity=item["quantity"]))
        print("---------------------\n")

    def update_pantry(self):
        more = "y"
        while more == "y":
            # Take input for each dictionary value
            item = input("\nWhat is the item called?\n\n")
            unit = input("\nWhat unit should I store the item as?\n\n")
            quantity = input("\nWhat quantity of this item should I store?\n\n")

            if any(entry["item"] == item for entry in self.pantry):
                item_index = next((index for (index, entry) in enumerate(self.pantry) if entry["item"] == item), None)
                if self.pantry[item_index]["unit"] == unit:
                    pantry_quantity = int(self.pantry[item_index]["quantity"])
                    pantry_quantity += int(quantity)
                    self.pantry[item_index]["quantity"] = str(pantry_quantity)
                else:
                    # Build dictionary and add to pantry list
                    new_entry = {"item": item, "unit": unit, "quantity": quantity}
                    self.pantry.append(new_entry)
            else:
                # Build dictionary and add to pantry list
                new_entry = {"item": item, "unit": unit, "quantity": quantity}
                self.pantry.append(new_entry)

            # Check for continue
            more = input("\nWould you like to add another item? (y or n)\n\n")
        
        # Overwrite CSV
        with open(self.data_file, "w", newline="") as pantry_csv:
            print("SYSTEM: Writing to file pantryplan.csv")
            headers = ["item", "unit", "quantity"]
            writer = csv.DictWriter(pantry_csv, fieldnames=headers)
            writer.writeheader()
            for item in self.pantry:
                writer.writerow(item)
        print("Finished writing to file\n---------------------")







