# implementation of card game - Memory
# 131115. gnpatterson. coursera project.

import simplegui
import random

UNIQUE_CARDS = 8
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 100

CARD_COUNT = UNIQUE_CARDS * 2
CARD_WIDTH = CANVAS_WIDTH // CARD_COUNT
CARD_HEIGHT = CANVAS_HEIGHT
CARD_CHOICES = list(range(UNIQUE_CARDS))

TEXT_SIZE = CARD_WIDTH
TEXT_HORZ_OFFSET = TEXT_SIZE // 4
TEXT_VERT_OFFSET = TEXT_SIZE // 4

# helper function to initialize globals
def new_game():
    global attempts, cards_info, index_pending
    attempts = 0
    cards_info = {}
    index_pending = []
    
    # cards_info: [number, exposed, topleft]
    cards = list(CARD_CHOICES)
    cards.extend(CARD_CHOICES)
    random.shuffle(cards)
    index = 0
    for card in cards:
        cards_info[index] = [card, False, CARD_WIDTH * index]
        index += 1

    
# define event handlers
def mouseclick(pos):
    global attempts
    
    # add game state logic here
    # what card did we click and what state was that card in?
    index_current = pos[0] // CARD_WIDTH
    if not cards_info[index_current][1]: # if not exposed
        cards_info[index_current][1] = True
        index_pending.append(index_current)
        if len(index_pending) == 2:
            attempts += 1
        elif len(index_pending) == 3:
            index1 = index_pending.pop(0)
            index2 = index_pending.pop(0)
            
            # compare the two cards.
            if cards_info[index1][0] != cards_info[index2][0]:
                cards_info[index1][1] = False
                cards_info[index2][1] = False
            
                        
# cards are logically 50x100 pixels in size
# but we are calculating the size dynamically
def draw(canvas):
    for index, card in cards_info.items():
        if card[1]: #exposed
            card_color = "Black"
            card_text = str(card[0])
        else:
            card_color = "Green"
            card_text = ""
        
        canvas.draw_polygon([[card[2], 0], 
                             [card[2] + CARD_WIDTH, 0], 
                             [card[2] + CARD_WIDTH, CARD_HEIGHT], 
                             [card[2], CARD_HEIGHT]],
                            2, "White", card_color)
        canvas.draw_text(card_text, 
                         [card[2] + CARD_WIDTH // 2 - TEXT_HORZ_OFFSET, 
                          CARD_HEIGHT // 2 + TEXT_VERT_OFFSET], 
                         TEXT_SIZE, "White")
    
    label.set_text("Turns = %d" % attempts)


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric