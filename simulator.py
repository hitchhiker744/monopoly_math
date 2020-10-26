import pandas as pd
import matplotlib.pyplot as plt
from game_setup import Game, Player



class Simulation(object):
    def __init__(self, players, cards_files_list, squares_file_name):
        self.game = self.setup_simulation(players, cards_files_list, squares_file_name)

    def setup_simulation(self, players, cards_files_list, squares_file_name):
        game = Game(players, cards_files_list, squares_file_name)
        return game


    def make_plot(self):
        return self.final_results['share_of_visits'].plot(kind='bar')


    def extract_results(self):
        results = []
        for square in self.game.board.squares:
            result = [square.purchasable, square.type, square.sequence, square.name, square.visits_count]
            results.append(result)

        df = pd.DataFrame(results, columns=['purchasable', 'type','sequence', 'name', 'visits_count'])
        df['share_of_visits'] = df['visits_count'] / df['visits_count'].sum()
        self.results = df
        self.grouped = df.groupby(['purchasable','type','sequence']).sum()
        self.final_results = self.grouped.loc['purchasable' != True].sort_values(by='share_of_visits', ascending=False)


    def run_simulation(self, rounds):
        while self.game.round_number <= rounds:
            self.game.play_round()
