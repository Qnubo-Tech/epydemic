import random
from joblib import Parallel, delayed

import matplotlib.pyplot as plt
import numpy as np


from src.geometry import Geometry
from src.environment.agent import Agent
from src.environment.status import Status
from src.environment.mobility import MobilityType
from src.simulation import AVERAGE_MOBILITY, MOBILITY_TYPE


class Society:

    def __init__(self, population, initial_condition, volume=1.0):

        self.population = int(population)
        self.volume = volume
        self.agents = self._create_agents(initial_condition)

    def _create_agents(self, initial_condition):

        agents = []
        healthy = min(self.population - 1, round(initial_condition['healthy']*self.population))
        infected = max(1, round(initial_condition['infected']*self.population))
        immune = self.population - healthy - infected

        mobility_type = MobilityType[MOBILITY_TYPE]

        [agents.append(
            Agent(x=random.uniform(0, Geometry.Box.Lx),
                  y=random.uniform(0, Geometry.Box.Ly),
                  status=Status.Healthy,
                  mobility_value=AVERAGE_MOBILITY,
                  mobility_type=mobility_type))
            for i in range(healthy)
        ], [agents.append(
            Agent(x=random.uniform(0, Geometry.Box.Lx),
                  y=random.uniform(0, Geometry.Box.Ly),
                  status=Status.Infected,
                  mobility_value=AVERAGE_MOBILITY,
                  mobility_type=mobility_type))
            for i in range(infected)
        ], [agents.append(
            Agent(x=random.uniform(0, Geometry.Box.Lx),
                  y=random.uniform(0, Geometry.Box.Ly),
                  status=Status.Immune,
                  mobility_value=AVERAGE_MOBILITY,
                  mobility_type=mobility_type))
            for i in range(immune)
        ]

        return agents

    def make_step(self):

        Parallel(n_jobs=10, prefer="threads")(
            delayed(agent.step)(self.force_field(agent.position)) for agent in self.agents
        )

    def force_field(self, position):

        return np.sum([agent.viral_force(position) for agent in self.agents])

    def compute_field(self, mesh):

        aux_f = [
            self.force_field(position=np.array([x, y]))
            for j, y in enumerate(mesh.y_range)
            for i, x in enumerate(mesh.x_range)
        ]

        return np.array(aux_f).reshape(mesh.x_range.size, mesh.y_range.size)

    def plot_field(self, ax, mesh):

        f = self.compute_field(mesh)

        ax.clear()
        ax.contour(mesh.X, mesh.Y, f)
        ax.set_aspect('equal')

    def plot(self, ax):

        ax.clear()

        [(
            ax.scatter(agent.x, agent.y, s=5, color=agent.status.value),
            ax.add_artist(plt.Circle((agent.x, agent.y),
                                     radius=agent.disease.infection_radius,
                                     color=agent.status.value,
                                     alpha=0.5*agent.viral_load))
         ) for agent in self.agents]

        ax.set_xlim(0, Geometry.Box.Lx)
        ax.set_ylim(0, Geometry.Box.Ly)
        ax.set_aspect('equal')

    def count_statuses(self, status: Status):
        return len([1 for agent in self.agents if (agent.status == status)])

    def get_status(self):
        status_dict = {st.name: self.count_statuses(st) for st in Status}
        status_dict["Total"] = sum(status_dict.values())
        return status_dict

    def get_cumulative_status(self):

        status_dict = {}
        previous_status = None
        for st in Status:
            status_dict[st.name] = self.count_statuses(status=st) / len(self.agents)
            if previous_status:
                status_dict[st.name] += status_dict[previous_status.name]

            previous_status = st

        return status_dict
