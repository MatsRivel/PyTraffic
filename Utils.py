from ast import Tuple
from dataclasses import dataclass
import math
from typing import List
import numpy as np

@dataclass
class Coord:
    def __init__(self,x:float,y:float):
        self.x = x
        self.y = y
        
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def add(self,step:"Coord"):
        self.x += step.x
        self.y += step.y

    def mult(self,multiplicator:float):
        self.x *= multiplicator
        self.y *= multiplicator
        
    def as_coords(self)->Tuple:
        return (self.x,self.y)
    
    def wrap_values(self,limit:float):
        if self.x > limit:
            self.x -= 2*limit
        if self.y > limit:
            self.y -= 2*limit
        if self.x < -limit:
            self.x += 2*limit
        if self.y < -limit:
            self.y += 2*limit

def distance_from_a_to_b(a:Coord,b:Coord)->float:
    return math.sqrt(math.pow(b.x-a.x,2) + math.pow(b.y-a.y,2))

def flat_distance_from_a_to_b(a:Coord,b:Coord)->float:
    return a.x - b.x

def angle_between(a:Coord,b:Coord)->float:
    
    return math.atan2(b.y - a.y,b.x - a.x)

def angular_a_to_b(a:Coord,b:Coord)->Coord:
    angle = angle_between(a,b)
    return components_of_angle(angle)

def closest_other_coord(a:Coord,B:List[Coord])->Coord:
    if len(B) == 0:
        return None
    raw_distances = np.array([(distance_from_a_to_b(a,b), angle_between(a,b)) for b in B],dtype=Coord)
    distances = np.array( [dist for (dist,angle) in raw_distances if (abs(angle) < 1 ) ])
    if len(distances) == 0:
        return None
    else:
        smallest_distance = np.min(distances)
        idx_of_closest = np.where(distances == smallest_distance)[0][0]
        return B[idx_of_closest]
    
def wrapping_distance_a_to_b(size:float, a:Coord, b:Coord):
    wrapped_points = (a.x,a.y)
    for i in range(len(wrapped_points)):
        if wrapped_points[i] > size/2:
            wrapped_points[i] /=2
    wrapped_a = Coord(*wrapped_points)
    return distance_from_a_to_b(wrapped_a,b)

def wrap_coord(size:int,c:Coord)->Coord:
    return Coord(c.x+size,c.y)
    
def components_of_angle(angle:float)->Coord:
    return Coord(math.cos(angle),math.sin(angle))