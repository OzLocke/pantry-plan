## Pantry Plan V0.1 Script ##

import csv, os

class UserInput:
    def __init__(self, verbose = False):
        self.pantry_instance = Pantry()
        self.verbose = verbose
        self.type_lookup = {"unit": self.pantry_instance.unit_types, "area": self.pantry_instance.area_types}
        self.menu = {1: "Review Pantry Contents", 2: "View available units", 3: "View available areas", 4: "Update Pantry", 5: "Quit"}
    
    def __repr__(self):
        return "an instance of the UserInput functional class"

    def display_types(self, d_type):
        d_type_selection = self.type_lookup[d_type]
        # Create nicely written list
        types = ', '.join(d_type_selection)
        print(f"\nThe available {d_type}s are: {types}.\n---------------------\n")
        
    def input_pantry_entries(self):
        # Create instance of error checker that can be used by the function
        self.error_checker = ErrorChecker()
        # Run input with a loop so user can add more than one item
        more = "y"
        while more == "y":
            # Take input for each dictionary value
            item = input("\nWhat is the item called?\n\n").lower()
            
            error = True
            while error:
                unit = input("\nWhat unit should I store the item as?\n\n").lower()
                error = self.error_checker.type_error_check(unit, "unit")
            
            error = True
            while error:
                try:
                    quantity = int(input("\nWhat quantity of this item should I store?\n\n"))
                    error = False
                except:
                    print(f"\nSorry, that's not a valid input.")

            error = True
            while error:
                area = input("\nWhat area should I store the item in?\n\n").lower()
                error = self.error_checker.type_error_check(area, "area")

            #Confirm user input
            print(f"\nYou are adding {item} ({quantity} {unit}s) to {area}, is this correct?\n")
            error = True
            while error:
                confirm = input("y or n\n\n").lower()
                error = self.error_checker.confirm_error_check(confirm)
            #If input was incorect go back to start of loop
            if confirm.lower() == "n":
                continue
            elif confirm.lower() == "y":
                # Add to pantry list
                self.pantry_instance.update_pantry(item, unit, quantity, area, self.verbose)
                # Check for continue
                error = True
                while error:
                    more = input("\nWould you like to add another item? (y or n)\n\n").lower()
                    error = self.error_checker.confirm_error_check(more)
        # Write to database
        self.pantry_instance.write_pantry(self.verbose)

    def user_input(self):
        # Print menu
        for key, value in self.menu.items():
            print(f"{str(key)} - {value}")
        
        # Take user input, with error handling
        error = True
        while error:
            try:
                user_choice = int(input("\nWhat would you like to do?\n\n"))

                # Call methods from linked pantry instance based on user input
                if self.menu[user_choice] == "Review Pantry Contents":
                    print("\nOK, here' the current pantry list:\n\nItem | Unit | Quantity | Area")
                    self.pantry_instance.display_pantry()
                    print("---------------------\n")
                    self.user_input()
                elif self.menu[user_choice] == "View available units":
                    self.display_types("unit")
                    self.user_input()
                elif self.menu[user_choice] == "View available areas":
                    self.display_types("area")
                    self.user_input()
                elif self.menu[user_choice] == "Update Pantry":
                    self.input_pantry_entries()
                    self.user_input()
                elif self.menu[user_choice] == "Quit":
                    print("\nGoodbye!")
                else:
                    raise ValueError

                error = False
            except:
                print(f"\nSorry, that's not a valid input.\n")

class ErrorChecker(UserInput):
    def __init__(self):
        # Link to UserInput class to be able to access it's attributes
        UserInput.__init__(self, verbose = False)

    def type_error_check(self, u_input, i_type):
        if not u_input in self.type_lookup[i_type]:
            print(f"\nSorry, that's not a valid input.")
            self.display_types(i_type)
            return True 
        else:
            return False

    def confirm_error_check(self, u_input):
        if u_input in ["n", "y"]:
            return False
        else:
            return True        
class Pantry:
    def __init__(self):
        # set up directory
        self.file_name = "pantryplan.csv"
        self.dirname = os.path.dirname(__file__)
        self.data_file = os.path.join(self.dirname, self.file_name)

        # set up variables
        self.pantry = []
        self.unit_types = ["bag", "box", "bottle", "carton", "tin", "case", "pack", "kg", "l"]
        self.area_types = ["fridge", "freezer", "cupboard"]

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
        return f"\nAn instance of the Pantry functional class"

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
            if verbose: print(f"SYSTEM: Creating new entry for {item} with unit of {unit} and quantity of {quantity} in the {area}")
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







