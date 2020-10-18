from typing import Dict

import matplotlib.pyplot as plt


class Graph:

    @staticmethod
    def generate_fig_ax(show_params: bool):

        fig = plt.figure()
        if show_params:
            gs = fig.add_gridspec(3, 4)
            ax1 = fig.add_subplot(gs[:, :2])
            ax2 = fig.add_subplot(gs[1:,-2:])
            ax3 = fig.add_subplot(gs[0, -2:])

            return fig, (ax1, ax2, ax3)

        else:
            gs = fig.add_gridspec(4, 4)
            ax1 = fig.add_subplot(gs[:, :2])
            ax2 = fig.add_subplot(gs[:, -2:])

            return fig, (ax1, ax2)

    @staticmethod
    def plot_table_params(ax: plt.axis, params_dict: Dict):

        cells = [[i] for i in params_dict.values()]

        ax.axis('off')
        table = ax.table(cellText=cells,
                           cellLoc='center',
                           rowLabels=list(params_dict.keys()),
                           rowLoc='center',
                           colWidths=[0.1],
                           loc='center')

        table.auto_set_font_size(False)
        table.set_fontsize(10)
