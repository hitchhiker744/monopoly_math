import numpy as np
import random

#from cards_setup import Card, Deck
from board_setup import Square, Board

class Player(object):
    def __init__(self, name):
        self.name = name
        self.current_position = 0
        self.squares_visited = []
        #self.move_order = 0
        self.cash = 0

    def move(self, steps):
        self.current_position += steps
        if self.current_position >= 40:
            self.current_position -= 40

    def roll_dice(self, n):
        rolls = []
        for i in range(n):
            roll = np.random.randint(1,7)
            rolls.append(roll)
        return rolls

    def draw_card(self, game, deck):
        card = deck.draw(self, game)
        card.play(self, game)


    def pay_cash(self, to, amount):
        pass



class Game(object):
    def __init__(self, players, cards_files_list, squares_file_name):
        self.board = []
        self.log = []
        self.players = players
        self.turn_number = 0
        self.round_number = 0
        self.doubles_counter = 0
        self.positions_visited = []
        self.setup_game(cards_files_list, squares_file_name)



    def setup_game(self, cards_files_list, squares_file_name):


        self.board = Board(cards_files_list, squares_file_name)
        self.reset()

    def set_order_of_play(self):
        self.players.sort(key=lambda x: x.roll_dice(1), reverse=True)
        self.log.append("Order of play was determined:")
        [self.log.append(p.name) for p in self.players]


    def reset(self):
        self.log.clear()
        self.positions_visited.clear()
        self.log.append("New game starting")
        self.turn_number = 0
        self.round_number = 0
        for player in self.players:
            player.current_position = 0
            player.cash = 2500
            self.log.append(player.name + " joined and is at " + str(player.current_position))

        self.set_order_of_play()

        for deck in self.board.cards_decks:
            deck.shuffle()
            self.log.append(deck.file_name + " shuffled ")

        'set decks at positions'
        for i in (2,17,33):
            'community chest'
            self.board.squares[i].deck = self.board.cards_decks[0]

        for i in (7,22,36):
            'chance'
            self.board.squares[i].deck = self.board.cards_decks[1]


    def check_prisoners_time_left(self):
        for cell in self.board.jail:
            if cell.release_date == self.round_number:
                self.board.release_player_from_jail(cell.prisoner, self)



    def play_turn(self, player):
        self.turn_number += 1
        self.log.append("Now turn: " + str(self.turn_number) + ". " + player.name + " is playing")

        rolls = player.roll_dice(2)
        result = np.sum(rolls)

        self.log.append(player.name + " rolled " + str(result))
        if rolls[0] == rolls[1]:
            self.log.append(player.name + " rolled a double!")
            self.doubles_counter += 1
            if self.doubles_counter == 3:
                self.board.send_player_to_jail(player, self)
                self.log.append(player.name + " rolled a 3rd double in a row and will be jailed!")
                #Need to stope the loop here. Break doesnt work!


        player.move(result)
        square = self.board.squares[player.current_position]
        square.play(self, player, self.turn_number)

        if rolls[0] == rolls[1]:
            self.log.append(player.name + " had a double and will roll again")
            self.play_turn(player)
        else:
            self.doubles_counter = 0


    def play_round(self):
        self.round_number += 1
        self.log.append("Starting round " + str(self.round_number))
        self.check_prisoners_time_left()

        for player in self.players:
            self.play_turn(player)
