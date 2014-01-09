# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ["",""]
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
    def draw_back(self, canvas, pos):
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        string = ""
        for card in self.cards:
            string += card.suit + card.rank + " "
        return "Hand contains " + string

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        has_ace = False
        for card in self.cards:
            value += VALUES[card.rank]
            if VALUES[card.rank] == 1:
                has_ace = True
                
        if has_ace:
            if value + 10 > 21:
                return value
            else:
                return value + 10
        else:
            return value
        
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        current = list(pos)
        for card in self.cards:
            card.draw(canvas, current)
            current[0] += CARD_SIZE[0] * 1.2

    def draw_dealer_blackjack(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        current = list(pos)
        down_card_drawn = False
        for card in self.cards:
            if not down_card_drawn:
                card.draw_back(canvas, current)
                current[0] += CARD_SIZE[0] * 1.2
                down_card_drawn = True
            else:
                card.draw(canvas, current)
                current[0] += CARD_SIZE[0] * 1.2
            
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []
        for i in range(4):
            for j in range(13):
                self.cards.append(Card(SUITS[i], RANKS[j]))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop()
    
    def __str__(self):
        # return a string representing the deck
        string = ""
        for card in self.cards:
            string += card.suit + card.rank + " "
        return "Deck contains " + string


#define event handlers for buttons
def deal():
    global outcome, in_play, score
    global card_deck, dealer_hand, player_hand
    
    outcome = ["",""]
    if in_play:
        in_play = False
        button.set_text("Deal")
        outcome = ["(Dealer wins: %d)" % dealer_hand.get_value(), "(You conceded: %d)" % player_hand.get_value()]
        score -= 1

    else: 
        in_play = True
        button.set_text("Concede")
        
        # your code goes here
        card_deck = Deck()
        dealer_hand = Hand()
        player_hand = Hand()
    
        card_deck.shuffle()
        player_hand.add_card(card_deck.deal_card())
        dealer_hand.add_card(card_deck.deal_card())
        player_hand.add_card(card_deck.deal_card())
        dealer_hand.add_card(card_deck.deal_card())
    
    
def hit():
    # replace with your code below
    global score, outcome, in_play
    
    # if the hand is in play, hit the player
    if in_play:
        if player_hand.get_value() < 21:
            player_hand.add_card(card_deck.deal_card())
   
    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() > 21:
        in_play = False
        button.set_text("Deal")
        outcome = ["(Dealer wins: %d)" % dealer_hand.get_value(), "(You busted: %d)" % player_hand.get_value()]
        score -= 1

    
def stand():
    # replace with your code below
    global score, outcome, in_play
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(card_deck.deal_card())
            
        # assign a message to outcome, update in_play and score
        if dealer_hand.get_value() > 21:
            score += 1
            outcome = ["(Dealer busted: %d)" % dealer_hand.get_value(), "(You win: %d)" % player_hand.get_value()]
        elif player_hand.get_value() > dealer_hand.get_value():
            score += 1
            if player_hand.get_value() == 21:
                outcome = ["(Dealer loses: %d)" % dealer_hand.get_value(), "(Blackjack: %d)" % player_hand.get_value()]
            else:
                outcome = ["(Dealer loses: %d)" % dealer_hand.get_value(), "(You win: %d)" % player_hand.get_value()]
        else:
            score -= 1
            if dealer_hand.get_value() == 21:
                outcome = ["(Blackjack: %d)" % dealer_hand.get_value(), "(You lose: %d)" % player_hand.get_value()]
            else:
                outcome = ["(Dealer wins: %d)" % dealer_hand.get_value(), "(You lose: %d)" % player_hand.get_value()]
                
        in_play = False
        button.set_text("Deal")
    
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    #card = Card("S", "A")
    #card.draw(canvas, [300, 300])

    canvas.draw_text("Blackjack", (50,100), 64, "White")
    canvas.draw_text("Score: %d" % score, (500,100), 64, "Yellow")
    canvas.draw_text("Dealer Hand %s" % outcome[0], (50, 220), 50, "Black")
    canvas.draw_text("Player Hand %s" % outcome[1], (50, 420), 50, "Black")
    
    if in_play:
        dealer_hand.draw_dealer_blackjack(canvas, (50,250))
        prompt.set_text("Hit, stand or concede?")
    else:
        dealer_hand.draw(canvas, (50,250))
        prompt.set_text("New deal?")
    player_hand.draw(canvas, (50,450))
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 800, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
button = frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

dummy = frame.add_label("")
prompt = frame.add_label("")

# get things rolling
deal()
frame.start()


# remember to review the gradic rubric