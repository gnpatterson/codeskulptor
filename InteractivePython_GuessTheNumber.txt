# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import random
import simplegui

# initialize global variables used in your code
low = 0
high = 100
secret = 0
tries = 0
allowed = 7

# helper function to start and restart the game
def new_game():
    global secret, tries
    tries = 0
    # we are using randrange which returns [low, high) which means
    # the high number will never be chosen by the computer and the
    # player will waste any guess that consists of the high number.
    # our messages should reflect this but the project requirements
    # say otherwise. the requirements are inconsistent. they say to
    # change the range to range [0,100) in function range100() but
    # then put the text "Range: 0 - 100" on the button. these two
    # things are in contradiction. you can't include and exclude
    # the high value. you need to make up your mind.
    secret = random.randrange(low, high)
    print ""
    print "New Game!"
    print "Guess a number between", low, "and", high, "-", "You have", allowed, "guesses."

# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global low, high, allowed
    low = 0
    high = 100
    allowed = 7
    new_game()

def range1000():
    # button that changes range to range [0,1000) and restarts
    global low, high, allowed
    low = 0
    high = 1000
    allowed = 10
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    global tries
    guess = int(guess)
    tries = tries + 1
    print "Guess", tries, "is", guess, "-",
    
    if guess == secret:
        print "Correct!"
        print "It only took you", tries, "guesses!"
        new_game()
    else:
        if guess < low:
            print "Guess a higher number.",
        elif guess < secret:
            print "Guess a higher number.",
        elif guess > high:
            print "Guess a lower number.",
        else:
            print "Guess a lower number.",
        print allowed - tries, "guesses remaining."

    if tries >= allowed:
        print "You have exhausted your allotted guesses."
        new_game()

# create frame
frame = simplegui.create_frame("Guess the Number", 200, 200)

# register event handlers for control elements
frame.add_button("Range: 0 - 100", range100, 200)
frame.add_button("Range: 0 - 1000", range1000, 200)
frame.add_input("Enter Guess", input_guess, 200)

# call new_game and start frame
new_game()
frame.start()

# always remember to check your completed program against the grading rubric
