

class Graph:

    @staticmethod
    def plot_table_params(axis, params_dict):

        cells = [[i] for i in params_dict.values()]

        axis.axis('off')
        table = axis.table(cellText=cells,
                           cellLoc='center',
                           rowLabels=list(params_dict.keys()),
                           rowLoc='center',
                           colWidths=[0.1],
                           loc='center')

        table.auto_set_font_size(False)
        table.set_fontsize(10)
