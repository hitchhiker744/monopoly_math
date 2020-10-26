from csv import reader
import random
import ast


class Card(object):
    def __init__(self, card_type, name, action_type, action_value):
        self.type = card_type
        self.name = name
        self.action_type = action_type
        self.action_value = action_value

    def play(self, player, game):
        game.log.append(player.name + " is playing card " + self.name)
        if self.action_type == 'move_to':
            if len(self.action_value) == 1:
                player.current_position = self.action_value[0]
                game.log.append(player.name + " moved to " + str(self.action_value[0]))

            elif len(self.action_value) > 1:
                min_steps = 41
                next_position = -1

                for destination in self.action_value:
                    #print(destination, type(destination))
                    steps = int(destination) - player.current_position
                    if steps > 0 and steps < min_steps:
                        min_steps = steps
                        next_position = destination
                player.current_position = next_position
                game.log.append(player.name + " moved to " + str(player.current_position))

        elif self.action_type == 'move_steps':
            player.move(self.action_value[0])
            game.log.append(player.name + " moved " + str(self.action_value[0]) + " steps")
        elif self.action_type == 'finance':
            player.cash += self.action_value[0]
            game.log.append(player.name + " cash changed by  " + str(self.action_value[0]))


class Deck(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.cards = []

    def draw(self, player, game):
        card = self.cards[0]
        game.log.append(player.name + " drew card " + card.name)

        self.cards.remove(card)
        self.cards.append(card)

        return card

    def shuffle(self):
        random.shuffle(self.cards)


    def load_cards(self):
        with open(self.file_name, encoding='utf-8-sig') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                value = ast.literal_eval(row[3])
                card = Card(row[0], row[1], row[2], value)
                self.cards.append(card)
