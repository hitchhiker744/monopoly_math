import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt

from cards_setup import Card, Deck
from board_setup import Square, Board

class Player(object):
    def __init__(self, name):
        self.name = name
        self.current_position = 0
        self.squares_visited = []
        self.move_order = 0
        self.cash = 0

    def move(self, steps):
        self.current_position += steps
        if self.current_position >= 40:
            self.current_position -= 40

    def roll_dice(self, n):
        rolls = []
        for i in range(n):
            roll = np.random.randint(1,6)
            rolls.append(roll)
        return rolls

    def draw_card(self, game, deck):
        card = deck.draw(self, game)
        card.play(self, game)


class Jail_Cell(object):
    def __init__(self, player, release_date, index):
        self.prisoner = player
        self.release_date = release_date
        self.index = index


class Game(object):
    def __init__(self, players, cards_files_list, squares_file_name):
        self.board = []
        self.log = []
        self.players = players
        self.jail = []
        self.cards_decks = []
        self.turn_number = 0
        self.round_number = 0
        self.positions_visited = []
        self.setup_game(cards_files_list, squares_file_name)



    def setup_game(self, cards_files_list, squares_file_name):
        for cards_file in cards_files_list:
            deck = Deck(cards_file)
            deck.read_cards()
            self.cards_decks.append(deck)

        self.board = Board(squares_file_name)
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

        for deck in self.cards_decks:
            deck.shuffle()
            self.log.append(deck.file_name + " shuffled ")

        'set decks at positions'
        for i in (2,17,33):
            'community chest'
            self.board.squares[i].deck = self.cards_decks[0]

        for i in (7,22,36):
            'chance'
            self.board.squares[i].deck = self.cards_decks[1]



    def send_player_to_jail(self, player):
        release_date = self.round_number + 3
        player_index = self.players.index(player)

        cell = Jail_Cell(player, release_date, player_index)
        self.players.remove(player)
        self.jail.append(cell)
        self.log.append(player.name + " was jailed until round " + str(release_date))


    def release_player_from_jail(self, player):
        for cell in self.jail:
            if cell.prisoner.name == player.name:
                self.players.insert(cell.index, player)
                self.jail.remove(cell)
                self.log.append(player.name + " was released from jail")

    def check_prisoners_time_left(self):
        for cell in self.jail:
            if cell.release_date == self.round_number:
                self.release_player_from_jail(cell.prisoner)


    def play_round(self):
            pass


    def play_turn(self, player):
        doubles_count = 0
        rolls = player.roll_dice(2)
        result = np.sum(rolls)
        self.log.append(player.name + " rolled " + str(result))
        player.move(result)
        square = self.board.squares[player.current_position]
        square.play(self, player, self.turn_number)
        self.turn_number += 1
        self.log.append("Now turn: " + str(self.turn_number))

        if rolls[0] == rolls[1]:
            doubles_count += 1
            self.log.append(player.name + " plays again becaus he had a double")
            self.play_turn(player)

    def run_game(self, rounds):
        while self.turn_number <= rounds*len(self.players):
            for player in self.players:
                self.play_turn(player)


    def extract_results(self):
        results = []
        for square in self.board.squares:
            result = [square.purchasable, square.type, square.sequence, square.name, square.visits_count]
            results.append(result)

        df = pd.DataFrame(results, columns=['purchasable', 'type','sequence', 'name', 'visits_count'])
        df['share_of_visits'] = df['visits_count'] / df['visits_count'].sum()
        self.results = df
        self.grouped = df.groupby(['purchasable','type','sequence']).sum()
        #self.filtered_results = self.grouped.filter(lambda x: x['purchasable'] == 1)
        self.final_results = self.grouped.loc['purchasable' != True].sort_values(by='share_of_visits', ascending=False)
        self.results_plot = self.final_results['share_of_visits'].plot(kind='bar')
