from csv import reader
from cards_setup import Card, Deck
import pandas as pd

class Square(object):
    def __init__(self, position, purchasable, square_type, sequence, name, action_type, action_value, plot_color):
        self.position = position
        self.purchasable = purchasable
        self.owner = None
        self.type = square_type
        self.sequence = sequence
        self.name = name
        self.action_type = action_type
        self.action_value = action_value
        self.plot_color = plot_color
        self.visits_count = 0
        self.visits = []
        self.deck = []

    def play(self, game, player, turn):
        game.log.append(player.name + " arrived at " + self.name + " at " + str(self.position))
        if self.action_type == 'move_to':
            player.current_position = self.action_value
            game.log.append(player.name + " moved to " + str(self.action_value))
        elif self.action_type == 'draw_card':
            game.log.append(player.name + " is drawing a card from " + self.deck.file_name)
            player.draw_card(game, self.deck)
        self.visits_count += 1
        self.visits.append(Visit(player, turn))
        game.positions_visited.append(self.position)


class Visit(object):
    def __init__(self, player, turn):
        self.turn = turn
        self.player = player



class Jail_Cell(object):
    def __init__(self, player, release_date, index, reason):
        self.prisoner = player
        self.release_date = release_date
        self.index = index
        self.reason = reason



class Board(object):
    def __init__(self, cards_files_list, squares_file_name):
        self.file_name = squares_file_name
        self.cards_files_list = cards_files_list
        self.squares = []
        self.jail = []
        self.cards_decks = []
        self.setup_board()

#    def load_squares(self):
#        with open(self.file_name, encoding='utf-8-sig') as read_obj:
#            csv_reader = reader(read_obj)
#            for row in csv_reader:
#                position = int(row[0])
#                purchasable = bool(int(row[1]))
#                square = Square(position, purchasable, row[2], row[3], row[4], row[5], row[6], row[7])
#                self.squares.append(square)

    def load_squares(self):
        #names=['index','purchasable','type','sequence','name','action_type','action_value','color','cost','house_cost','rent','rent_1h','rent_2h','rent_3h','rent_4h','rent_hotel','mortgage']
        df = pd.read_csv(self.file_name, index_col=0)

        for index, row in df.iterrows():
            position = int(index)
            purchasable = bool(int(row['purchasable']))
            square = Square(position, purchasable, row['type'], row['sequence'], row['name'], row['action_type'], row['action_value'], row['color'])
            self.squares.append(square)

    def prepare_cards_decks(self):
        for cards_file in self.cards_files_list:
            deck = Deck(cards_file)
            deck.load_cards()
            self.cards_decks.append(deck)


    def setup_board(self):
        self.load_squares()
        self.prepare_cards_decks()


    def move(self):
        pass

    def give_cash(self, player, amount):
        pass


    def send_player_to_jail(self, player, game, reason):
        release_date = game.round_number + 3
        player_index = game.players.index(player)

        cell = Jail_Cell(player, release_date, player_index, reason)
        self.squares[10].play(game, player, game.turn_number)
        game.players.remove(player)
        self.jail.append(cell)
        game.log.append(player.name + " was jailed until round " + str(release_date))


    def release_player_from_jail(self, player, game):
        for cell in self.jail:
            if cell.prisoner.name == player.name:
                game.players.insert(cell.index, player)
                self.jail.remove(cell)
                game.log.append(player.name + " was released from jail")
