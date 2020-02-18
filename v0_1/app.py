## Pantry Plan V0.1 App ##
## Takes user input and logs to CSV, tracks contents of pantry ##

from script import Pantry, UserInput
pantry_name = "My Pantry"
verbose = True

# -- Set up instances
pantry = Pantry(pantry_name)
# User input contains pantry instance so that it call that instance's methods
user_input = UserInput(pantry, verbose)

# -- Begin interaction
print("Welcome to Pantry Plan 0.1")
user_input.user_input()
