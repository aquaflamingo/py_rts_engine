import math

class Vector2:
    """2D vector class for handling positions and movements."""
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def normalize(self):
        length = self.length()
        if length != 0:
            return Vector2(self.x / length, self.y / length)
        return Vector2()
    
    def to_tuple(self):
        return (self.x, self.y)
    
    @staticmethod
    def from_tuple(tuple_value):
        return Vector2(tuple_value[0], tuple_value[1])
