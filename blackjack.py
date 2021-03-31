from player import Player
from variables import Variables
from DQNLearner import DQNLearner
from QLearner import Qlearning
import numpy as np


class BlackJack:
    def __init__(self, learning_rounds, Qlearning= None, report_every=100):
        self.p = Qlearning
        self.win = 0
        self.loss = 0
        self.game = 1
        self.learning_rounds = learning_rounds
        self.reportEvery = report_every
    
    def run(self):
        deck, player, dealer, winner = self.reset_round()

        state = self.startingState(player, dealer)
        while True:
            dealer_action = player.getAction(state)
            player_action = dealer.getAction(state)

            if dealer_action == Variables.hit:
                player.hit(deck)
            
            if player_action == Variables.hit:
                dealer.hit(deck)

            if self.ifBust(dealer):
                winner = Variables.player
                break

            if self.ifBust(player):
                winner = Variables.dealer
                break

            if dealer_action == player_action and dealer_action == Variables.stay:
                break

            state = self.getState(player, dealer_action, dealer)
            player.update(state,0)

        if winner is None:
            winner = self.scoreWinner(player, dealer)
            player.update(state,0)

        if winner is None:
            winner = self.scoreWinner(player, dealer)
        
        if winner == Variables.player:
            self.win += 1
            player.update(self.getLastState(player,player_action, dealer),1)

        else:
            self.loss += 1
            player.update(self.getLastState(player,player_action,dealer),-1)
        
        self.game += 1

        self.report()

        if self.game == self.learning_rounds:
            print('Learning Complete')
            self.p.learning
            self.win = 0
            self.loss = 0

    def report(self):
        if self.game % self.learning_rounds == 0:
            if self.win <= 0:
                pass
            else:
                print(str(self.game)+':'+str(self.win/(self.win+self.loss)))

        elif self.game % self.reportEvery == 0:
            print(str(self.win/(self.win+self.loss)))
    
    def getState(self, player, player_action, dealer):
        return (player.hand_value(), dealer.get_og_show_value())
    
    def startingState(self, player, dealer):
        return (player.hand_value(), dealer.visibile_card())
    
    def getLastState(self, player, player_action, dealer):
        return (player.hand_value(), dealer.hand_value())
    
    def scoreWinner(self,player,dealer):
        if player.hand_value() ==21 or (player.hand_value() > dealer.hand_value() and player.hand_value() <=21):
            return Variables.player
        else:
            return Variables.dealer
    
    def ifBust(self,player):
        if player.hand_value() >21:
            return True
        else:
            return False
    
    def reset_round(self):
        deck = Deck()
        if self.p is None:
            self.p = Qlearning()
        else:
            self.p.resetHand()
        
        player = self.p
        dealer = Player()

        winner = None
        player.hit(deck)
        dealer.hit(deck)
        player.hit(deck)
        dealer.hit(deck)

        return deck, player, dealer, winner
    

            

class Deck:
    def __init__(self):

        self.shuffle()

    def shuffle(self):
        cards = (np.arange(0,10) + 1)
        #6 decks of cards
        cards = np.repeat(cards,4*6) 
        np.random.shuffle(cards)
        self._cards = cards.tolist()

    def draw(self):
        return self._cards.pop()