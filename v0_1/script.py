## Pantry Plan V0.1 Script ##

import csv, os

class UserInput:
    def __init__(self, pantry, verbose = False):
        self.pantry_instance = pantry
        self.verbose = verbose
    
    def __repr__(self):
        return "an instance of the UserInput functional class"

    def display_types(self, d_type):
        d_type_lookup = {"unit": self.pantry_instance.unit_types, "area": self.pantry_instance.area_types}
        d_type = d_type_lookup[d_type]
        # Create nicely written list
        types = ', '.join(d_type)
        print(f"\nThe available units are: {types}.\n---------------------\n")
        

    def input_pantry_entries(self):
        more = "y"
        while more == "y":
            # Take input for each dictionary value
            item = input("\nWhat is the item called?\n\n")
            # Ensure unit input is valid
            unit_error = True
            while unit_error:
                unit = input("\nWhat unit should I store the item as?\n\n")
                if not unit in self.pantry_instance.unit_types:
                    print(f"Sorry, {unit} is not a valid unit.")
                    self.display_types("unit")
                else:
                    unit_error = False
            quantity = input("\nWhat quantity of this item should I store?\n\n")
            # Ensure unit input is valid
            area_error = True
            while area_error:
                area = input("\nAnd where will you be storing it?\n\n")
                if not area in self.pantry_instance.area_types:
                    print(f"Sorry, {area} is not a valid area.")
                    self.display_types("area")
                else:
                    area_error = False

            # Add to pantry list
            self.pantry_instance.update_pantry(item, unit, quantity, area, self.verbose)
            # Check for continue
            more = input("\nWould you like to add another item? (y or n)\n\n")
        # Write to database
        self.pantry_instance.write_pantry(self.verbose)

    def user_input(self):
        user_choice = int(input("What would you like to do?\n1 - Review Pantry Contents\n2 - View available units\n3 - Update Pantry\n4 - Quit\n\n"))

        # Call methods from linked pantry instance based on user input
        if user_choice == 1:
            print("\nOK, here' the current pantry list:\n\nItem | Unit | Quantity | Area")
            self.pantry_instance.display_pantry()
            print("---------------------\n")
            self.user_input()
        if user_choice == 2:
            self.display_types("unit")
            self.user_input()
        if user_choice == 3:
            self.input_pantry_entries()
            self.user_input()
        if user_choice == 4:
            print("\nGoodbye!")

class Pantry:
    def __init__(self, p_name):
        # set up directory
        self.file_name = "pantryplan.csv"
        self.dirname = os.path.dirname(__file__)
        self.data_file = os.path.join(self.dirname, self.file_name)

        # set up variables
        self.pantry = []
        self.unit_types = ["bag", "box", "bottle", "carton", "tin", "case", "pack", "kg", "l"]
        self.area_types = ["fridge", "freezer", "cupboard"]
        self.pantry_name = p_name

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
            print("SYSTEM: Finished reading file\n---------------------")

    def __repr__(self):
        return f"\nAn instance of the Pantry functional class called {self.pantry_name}"

    def display_pantry(self):       
        for item in self.pantry:
            print("{item} | {unit} | {quantity} | {area}".format(item=item["item"], unit=item["unit"], quantity=item["quantity"], area=item["area"]))

    def update_pantry(self, item, unit, quantity, area, verbose):
        if verbose: print("SYSTEM: Checking item against pantry")
        if any(entry["item"] == item for entry in self.pantry):
            # Get the index of the item so we can access the dictionary within the pantry list by index
            item_index = next((index for (index, entry) in enumerate(self.pantry) if entry["item"] == item), None)
            if self.pantry[item_index]["unit"] == unit:
                if verbose: print(f"SYSTEM: Adding {quantity} of {item} to existing item")
                pantry_quantity = int(self.pantry[item_index]["quantity"])
                pantry_quantity += int(quantity)
                self.pantry[item_index]["quantity"] = str(pantry_quantity)
            else:
                # Build dictionary and add to pantry list
                if verbose: print(f"SYSTEM: Creating new entry for duplicate {item} with new unit of {unit} and quantity of {quantity} in the {area}")
                new_entry = {"item": item, "unit": unit, "quantity": quantity, "area": area}
                self.pantry.append(new_entry)
        else:
            # Build dictionary and add to pantry list
            if verbose: print(f"SYSTEM: Creating new entry for {item} with uinit of {unit} and quantity of {quantity} in the {area}")
            new_entry = {"item": item, "unit": unit, "quantity": quantity, "area": area}
            self.pantry.append(new_entry)
        if verbose: print("SYSTEM: Finished updating pantry\n---------------------")
    
    def write_pantry(self, verbose):
        # Overwrite CSV
        with open(self.data_file, "w", newline="") as pantry_csv:
            if verbose: print(f"SYSTEM: Writing to file {self.file_name}")
            headers = ["item", "unit", "quantity", "area"]
            writer = csv.DictWriter(pantry_csv, fieldnames=headers)
            writer.writeheader()
            for item in self.pantry:
                writer.writerow(item)
        if verbose: print("SYSTEM: Finished writing to file\n---------------------")







