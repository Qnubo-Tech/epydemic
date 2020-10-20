from typing import Dict, List

import matplotlib.pyplot as plt

from src.environment.status import Status


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

    @staticmethod
    def plot_lines_society_progress(ax: plt.axis,
                           time_array: List,
                           society_snapshot: Dict,
                           society_progress: Dict):

        for st in Status:
            society_progress[st.name].append(society_snapshot[st.name] / society_snapshot["Total"])
            ax.plot(
                time_array, society_progress[st.name],
                c=st.value, ls='-', label=st.name, alpha=0.5
            )
            ax.text(
                x=time_array[-1], y=society_progress[st.name][-1],
                s=r"{0:.2f}".format(society_progress[st.name][-1]),
                size=10,
                color=st.value
            )

    @staticmethod
    def plot_areas_society_progress(ax: plt.axis,
                                   time_array: List,
                                   society_snapshot: Dict,
                                   society_progress: Dict):

        previous_status = None
        for st in Status:
            society_progress[st.name].append(society_snapshot[st.name])

            if previous_status:
                lower_limit = society_progress[previous_status.name]
            else :
                lower_limit = [0]

            ax.fill_between(
                x=time_array, y1=lower_limit, y2=society_progress[st.name],
                color=st.value, label=st.name, alpha=0.25
            )

            ax.text(
                x=time_array[-1], y=1 / 2 * (lower_limit[-1] + society_snapshot[st.name]),
                s=r"{0:.2f}".format(society_snapshot[st.name] - lower_limit[-1]),
                size=10,
                color=st.value
            )

            previous_status = st
