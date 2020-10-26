import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from game_setup import Game, Player



class Simulation(object):
    def __init__(self, players, cards_files_list, squares_file_name):
        self.game = self.setup_simulation(players, cards_files_list, squares_file_name)

    def setup_simulation(self, players, cards_files_list, squares_file_name):
        game = Game(players, cards_files_list, squares_file_name)
        return game


    def make_plot(self):
        #return self.final_results['share_of_visits'].plot(kind='bar')
        labels = self.results['name']
        values = self.results['share_of_visits']
        colors = self.results['color']

        x = np.arange(len(labels))
        width = 0.8

        fig, ax = plt.subplots()
        rects1 = ax.bar(x, values, width, color=colors)


        ax.set_ylabel('% of all visits')
        ax.set_title('Monopoly board visits distribution')
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation='vertical')

        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{:.2%}'.format(height),
                           xy=(rect.get_x() + rect.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha = 'center', va='bottom')
        autolabel(rects1)
        fig.set_size_inches(18,10)
        fig.set_facecolor('white')
        fig.tight_layout()
        plt.show()

# colors: https://matplotlib.org/gallery/color/named_colors.html#sphx-glr-gallery-color-named-colors-py

    def extract_results(self):
        results = []
        for square in self.game.board.squares:
            result = [square.purchasable, square.type, square.sequence, square.name, square.visits_count, square.plot_color]
            results.append(result)

        df = pd.DataFrame(results, columns=['purchasable', 'type','sequence', 'name', 'visits_count', 'color'])
        df['share_of_visits'] = df['visits_count'] / df['visits_count'].sum()
        self.results = df
        self.grouped = df.groupby(['purchasable','type','sequence']).sum()
        self.final_results = self.grouped.loc['purchasable' != True].sort_values(by='share_of_visits', ascending=False)


    def run_simulation(self, rounds):
        while self.game.round_number <= rounds:
            self.game.play_round()
