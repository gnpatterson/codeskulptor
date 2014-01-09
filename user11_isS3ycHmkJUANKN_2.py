# coursera.org
# april 22, 2013
# program template for mini-project 1

import random

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

def number_to_name(number):
    # fill in your code below
    
    # convert number to a name using if/elif/else
    # don't forget to return the result!
    # all valid return values are not an empty string.
    # empty string is returned on an error.
    
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        print "number_to_name(" + str(number) + ") undefined."
        return ""
    
    
def name_to_number(name):
    # fill in your code below

    # convert name to number using if/elif/else
    # don't forget to return the result!
    # all valid return values are > 0.
    # -1 is returned on an error.

    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        print "name_to_number(" + name + ") undefined."
        return -1

    
def rpsls(name): 
    # fill in your code below

    # convert name to player_number using name_to_number
    player_number = name_to_number(name)

    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(5)
    
    # compute difference of player_number and comp_number modulo five
    # modulo ensures all answers are positive and <= 4.
    results = player_number - comp_number
    if results < 0:
        results = results % 5

    # use if/elif/else to determine winner
    # results of 0 is a tie.
    # results of 1 or 2 is a winner.
    # results of 3 or 4 is a loser.
    if results == 0:
        winner = "Player and computer tie!"
    elif results < 3:
        winner = "Player wins!"
    else:
        winner = "Computer wins!"
    
    # convert comp_number to name using number_to_name
    comp_name = number_to_name(comp_number)
    
    # print results
    print ""
    print "Player chooses " + name
    print "Computer chooses " + comp_name
    print winner

    
# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric


