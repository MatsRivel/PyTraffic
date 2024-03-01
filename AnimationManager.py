from typing import List
from matplotlib import animation, pyplot as plt
from functools import partial
from MovingDot import Agent
from Utils import Coord, closest_other_coord

class AnimationManager():
    def __init__(self,size:float,agents:list):
        self.size = size
        self.agents:List[Agent] = agents
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-size/2,size/2)
        self.ax.set_ylim(-size/2,size/2)
        
    def runAnimation(self):
        def update(num, dots, ax):
            for (idx,(current_agent,dot)) in enumerate(zip(self.agents,dots)):
                not_self_agents = self.agents[:idx] + self.agents[idx+1:]
                not_self_pos = [other_agent.pos for other_agent in not_self_agents]
                closest = closest_other_coord(current_agent.pos,not_self_pos)
                current_agent.move(closest)
            return dots

        dots = []
        for agent in self.agents:
            self.ax.add_patch(agent.body)
            dots.append(agent.body)
        
        ani = animation.FuncAnimation(self.fig,
                                      update,
                                      frames=range(1000),
                                      fargs=(dots, self.ax),
                                      interval=20)
        plt.show()