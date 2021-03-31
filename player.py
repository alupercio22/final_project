from variables import Variables

class Player:
    def __init__(self):
        self.cards =[]
        self.og_show_value = 0

    #show hidden cards
    def show_hand(self):
        return self.cards
    
    #decision to hit/stay(HIT17)
    def getAction(self, state = None):
        if self.hand_value() <= 17:
            return Variables.hit
        else:
            return Variables.stay
        
    def hand_value(self):
        return sum(self.cards)
        
    def visibile_card(self):
        visibleCard = sum(self.cards[1:])
        self.og_show_value = visibleCard
        return visibleCard
    
    def get_og_show_value(self):
        return self.og_show_value
    
    def hit(self, deck):
        Value = deck.draw()
        self.cards.append(Value)
    
    def stay(self):
        return True
    
    def resetHand(self):
        self.cards = []
    
    def update(self, new_state, reward):
        pass