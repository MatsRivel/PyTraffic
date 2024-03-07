import random
from typing import Final
from AnimationManager import AnimationManager
from MovingDot import Agent, Coord


def noise(speed:float)->float:
    if speed >= 10:
        if random.random() > 0.8:
            return speed * 0.8
    return speed

def noise_and_speed(speed:float)->float:
    if speed == 0:
        speed = 1
        if random.random() > 0.5:
            return speed * 0.8
    return noise(speed)

def main():
    WORLD_SIZE:Final[int] = 1000
    N_ACTORS: Final[int] = 2
    agents = []
    for i in range(0,N_ACTORS):
        if i == 0:
            agent = Agent( i ,Coord(-i*10,0),world_size=WORLD_SIZE, step_noise_function=noise_and_speed)
        else:
            agent = Agent(i,Coord(-i*10,0),world_size=WORLD_SIZE,step_noise_function=noise)
        agents.append(agent)
        
    # agents.append(Agent(i,Coord(N_ACTORS*10,0),world_size=WORLD_SIZE,step_noise_function=noise))
    AM = AnimationManager(WORLD_SIZE,agents)
    AM.runAnimation()
# 
if __name__ == '__main__':
    main()