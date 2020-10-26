from csv import reader


class Square(object):
    def __init__(self, position, purchasable, square_type, sequence, name, action_type, action_value):
        self.position = position
        self.purchasable = purchasable
        self.type = square_type
        self.sequence = sequence
        self.name = name
        self.action_type = action_type
        self.action_value = action_value
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


class Board(object):
    def __init__(self, squares_file_name):
        self.file_name = squares_file_name
        self.squares = []
        self.jail = []
        self.read_squares()

    def read_squares(self):
        with open(self.file_name, encoding='utf-8-sig') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                position = int(row[0])
                purchasable = bool(int(row[1]))
                square = Square(position, purchasable, row[2], row[3], row[4], row[5], row[6])
                self.squares.append(square)

    def move(self):
        pass

    def give_cash(self, player, amount):
        pass

    
    def send_player_to_jail(self, player, game):
        release_date = self.round_number + 3
        player_index = self.players.index(player)

        cell = Jail_Cell(player, release_date, player_index)
        game.players.remove(player)
        self.jail.append(cell)
        game.log.append(player.name + " was jailed until round " + str(release_date))


    def release_player_from_jail(self, player, game):
        for cell in self.jail:
            if cell.prisoner.name == player.name:
                game.players.insert(cell.index, player)
                self.jail.remove(cell)
                game.log.append(player.name + " was released from jail")
