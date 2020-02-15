## Pantry Plan V0.1 App ##
## Takes user input and logs to CSV, tracks contents of pantry ##

from script import Pantry, UserInput

# -- Set up instances
pantry = Pantry()
# User input contains pantry instance so that it call that instance's methods
user_input = UserInput(pantry)

# -- Begin interaction
print("Welcome to Pantry Plan 0.1")
user_input.user_input()
