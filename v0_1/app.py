## Pantry Plan V0.1 App ##
## Takes user input and logs to CSV, tracks contents of pantry ##

from script import Pantry, UserInput
verbose = True

# -- Set up instances
user_input = UserInput(verbose)

# -- Begin interaction
print("Welcome to Pantry Plan 0.1")
user_input.user_input()
