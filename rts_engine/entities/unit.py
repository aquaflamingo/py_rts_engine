from ..core.vector import Vector2
import pygame
from typing import List, Optional, Tuple

class Unit:
    """Base class for all game units."""
    
    def __init__(self, 
                 position: Tuple[float, float],
                 size: int,
                 player_id: int,
                 max_speed: float = 3.0,
                 separation_radius: float = 40.0,
                 arrival_radius: float = 5.0):
        self.position = Vector2.from_tuple(position)
        self.velocity = Vector2()
        self.target: Optional[Vector2] = None
        self.size = size
        self.player_id = player_id
        self.selected = False
        
        # Physics parameters
        self.max_speed = max_speed
        self.separation_radius = separation_radius
        self.arrival_radius = arrival_radius
    
    def move_to(self, target_pos: Tuple[float, float]):
        """Set unit's target position."""
        self.target = Vector2.from_tuple(target_pos)
    
    def apply_physics(self, nearby_units: List['Unit'], separation_force: float = 0.5):
        """Apply physics calculations for unit movement."""
        if self.target:
            # Move towards target
            direction = (self.target - self.position).normalize()
            desired_velocity = direction * self.max_speed
            
            # Check if near target
            if (self.target - self.position).length() < self.arrival_radius:
                self.target = None
                self.velocity = Vector2()
                return

            # Apply separation force
            separation = Vector2()
            for other in nearby_units:
                if other != self:
                    diff = self.position - other.position
                    distance = diff.length()
                    if distance < self.separation_radius:
                        separation = separation + (diff.normalize() * (self.separation_radius - distance))
            
            # Combine forces
            self.velocity = (desired_velocity + (separation * separation_force)).normalize() * self.max_speed
            
            # Update position
            self.position = self.position + self.velocity
    
    def get_rect(self) -> pygame.Rect:
        """Get the unit's collision rectangle."""
        return pygame.Rect(
            self.position.x - self.size/2,
            self.position.y - self.size/2,
            self.size,
            self.size
        )
    
    def draw(self, screen: pygame.Surface, colors: dict):
        """Draw the unit on the screen."""
        color = colors.get(f'player_{self.player_id}', (255, 255, 255))
        pygame.draw.rect(
            screen,
            color,
            (self.position.x - self.size/2,
             self.position.y - self.size/2,
             self.size,
             self.size)
        )
        if self.selected:
            pygame.draw.rect(
                screen,
                colors.get('selection', (255, 255, 255)),
                (self.position.x - self.size/2,
                 self.position.y - self.size/2,
                 self.size,
                 self.size),
                2
            )
