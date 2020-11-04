import random
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np

from joblib import Parallel, delayed

from src.geometry import Box
from src.environment.agent import Agent
from src.environment.status import Status
from src.environment.mobility import MobilityType
from src.configuration import MobilityParams


class Society:

    def __init__(self, population, initial_condition):

        self.population = int(population)
        self.agents = self._create_agents(initial_condition)

    def _create_agents(self, initial_condition) -> List[Agent]:

        agents = []
        healthy = min(self.population - 1, round(initial_condition[Status.Healthy.name]*self.population))
        infected = max(1, round(initial_condition[Status.Infected.name]*self.population))
        immune = self.population - healthy - infected

        mobility_type = MobilityType[MobilityParams.MOBILITY_TYPE]

        [agents.append(
            Agent(x=random.uniform(0, Box.Lx),
                  y=random.uniform(0, Box.Ly),
                  status=Status.Healthy,
                  mobility_value=MobilityParams.DEFAULT_MOBILITY,
                  mobility_type=mobility_type))
            for _ in range(healthy)
        ], [agents.append(
            Agent(x=random.uniform(0, Box.Lx),
                  y=random.uniform(0, Box.Ly),
                  status=Status.Infected,
                  mobility_value=MobilityParams.DEFAULT_MOBILITY,
                  mobility_type=mobility_type))
            for _ in range(infected)
        ], [agents.append(
            Agent(x=random.uniform(0, Box.Lx),
                  y=random.uniform(0, Box.Ly),
                  status=Status.Immune,
                  mobility_value=MobilityParams.DEFAULT_MOBILITY,
                  mobility_type=mobility_type))
            for _ in range(immune)
        ]

        return agents

    def count_statuses(self, status: Status) -> int:
        return len([1 for agent in self.agents if (agent.status == status)])

    @property
    def num_infected(self) -> int:
        return self.count_statuses(status=Status.Infected)

    @property
    def num_healthy(self) -> int:
        return self.count_statuses(status=Status.Healthy)

    @property
    def num_immune(self) -> int:
        return self.count_statuses(status=Status.Immune)

    @property
    def num_confined(self) -> int:
        return self.count_statuses(status=Status.Confined)

    def get_status(self) -> Dict:
        status_dict = {st.name: self.count_statuses(st) for st in Status}
        status_dict["Total"] = self.population
        return status_dict

    def get_stacked_status(self) -> Dict:

        status_dict = {}
        previous_status = None
        for st in Status:
            status_dict[st.name] = self.count_statuses(status=st) / self.population
            if previous_status:
                status_dict[st.name] += status_dict[previous_status.name]

            previous_status = st

        return status_dict

    def make_step(self):

        Parallel(n_jobs=-10, prefer="threads")(
            delayed(agent.step)(self.force_field(agent.position)) for agent in self.agents
        )

    def force_field(self, position: np.array) -> np.array:

        return np.sum([agent.viral_force(position) for agent in self.agents])

    def compute_field(self, mesh: Box) -> np.array:

        aux_f = [
            self.force_field(position=np.array([x, y]))
            for j, y in enumerate(mesh.y_range())
            for i, x in enumerate(mesh.x_range())
        ]

        return np.array(aux_f).reshape(mesh.x_range().size, mesh.y_range().size)

    def plot_field(self, ax, mesh):

        f = self.compute_field(mesh)

        ax.clear()
        x, y = mesh.x_y()
        ax.contour(x, y, f)
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

        ax.set_xlim(0, Box.Lx)
        ax.set_ylim(0, Box.Ly)
        ax.set_aspect('equal')
