from dataclasses import dataclass
from types import FunctionType
from typing import List, Self, Final
from Utils import angle_between, angular_a_to_b, components_of_angle, distance_from_a_to_b, Coord, flat_distance_from_a_to_b, wrap_coord
from matplotlib import pyplot as plt, patches


class Agent:
    def __init__(self, idx:int, start_pos:Coord, world_size:int, color:str="b",step_noise_function:FunctionType=None):
        # Identifying Information
        self.idx:Final[int] = idx
        # Fixed Values about the enviornment:
        self.world_size:Final[int] =  world_size
        # Fixed Values about the agent
        self.max_distance:Final[float] = 100.0
        self.min_distance:Final[float] = 90.0
        self.acceleration_limit:Final[float] = 5.0
        self.step_noise_function: Final[FunctionType] = step_noise_function
        self.max_speed: Final[float] = 10
        
        # Changing Values
        self._pos:Coord = start_pos
        self._body = plt.Circle(self.pos.as_coords(), radius=3, color=color)
        self._acceleration:float = 0.0
        self._speed:float = 0.0
        self._angle:float = 0.0
        self.going_straight:bool = True
        
    def __str__(self):
        return "\n".join([
            f"--- id: {self.idx} ---",
            f"    {self.pos=:}",
            f"    {self.speed=:}",
            f"    {self.acceleration=:}",
            f"    {self.angle=:}",
            f""
        ])
        
    def move(self, target: Coord):
        if target is None:
            self._move_straight()
        else:
            self._move_toward_target(target)
    
    def _move_toward_target(self, target: Coord):
        distance: float = max(flat_distance_from_a_to_b(self.pos, target),0)
        if distance < self.min_distance:
            self.acceleration -= self.max_speed / 10
            self.body.set_color("Orange")
        elif distance > self.max_distance:
            self.acceleration += self.max_speed / 20
            self.body.set_color("Orange")
        else:
            self.body.set_color("Green")
        self.speed += self.acceleration 
        self.pos = Coord(self.pos.x + self.speed, self.pos.y)
        self.going_straight = False
          
    def _move_straight(self):
        # print(" >>> Move Straight <<<")
        if self.acceleration == 0:
            self.acceleration = self.acceleration_limit/2
        self.body.set_color("Blue")
        self.speed = self.speed + self.acceleration
        self.pos = Coord(self.pos.x + self.speed, self.pos.y)
        self.going_straight = True
    
    @property
    def angle(self)->float:
        return self._angle
    
    @angle.setter
    def angle(self,value:float):
        while value < 0:
            value += 360
        if value > 360:
            value %= 360
    
    @property
    def acceleration(self)->float:
        return self._acceleration
    
    @acceleration.setter
    def acceleration(self,value:float):
        if value >=0:
            self._acceleration = min(value, self.acceleration_limit)
        else:
            self._acceleration = max(value, self.acceleration_limit)

    @property
    def speed(self)->float:
        return self._speed
    
    @speed.setter
    def speed(self,value:float):
        max_speed = self.max_speed
        if self.going_straight:
            max_speed *= 0.5
        self._speed = min( max( self.step_noise_function(value),0), max_speed)
        if self._speed == 0:
            self._body.set_color("Red")
    
    @property
    def pos(self)->Coord:
        return self._pos
    
    @pos.setter
    def pos(self,new_position:Coord):
        new_position.wrap_values(self.world_size/2)
        self._pos = new_position
        self._body.center = new_position.as_coords()
        
    @property
    def body(self)->"plt.Circle":
        return self._body
    
    @body.setter
    def body(self,value:"plt.Circle"):
        self._body = value