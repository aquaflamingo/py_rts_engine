import pygame
from typing import List, Optional, Tuple, Dict
from ..entities.unit import Unit
from ..core.vector import Vector2

class RTSGame:
    """Base game engine class for RTS games."""
    
    def __init__(self, 
                 window_size: Tuple[int, int] = (800, 600),
                 tile_size: int = 32,
                 colors: Optional[Dict[str, Tuple[int, int, int]]] = None):
        """
        Initialize the RTS game engine.
        
        Args:
            window_size: Tuple of (width, height) for the game window
            tile_size: Size of grid tiles
            colors: Dictionary of color definitions
        """
        pygame.init()
        
        self.window_size = window_size
        self.tile_size = tile_size
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        
        # Game state
        self.units: List[Unit] = []
        self.selected_units: List[Unit] = []
        
        # Selection state
        self.selection_start: Optional[Tuple[int, int]] = None
        self.selecting = False
        self.selection_surface = pygame.Surface(window_size, pygame.SRCALPHA)
        
        # Default colors
        self.colors = {
            'background': (0, 0, 0),
            'grid': (50, 50, 50),
            'player_1': (0, 0, 255),
            'player_2': (255, 0, 0),
            'selection': (255, 255, 255),
            'selection_box': (0, 255, 0, 50),
            'selection_border': (0, 255, 0)
        }
        if colors:
            self.colors.update(colors)
    
    def add_unit(self, unit: Unit):
        """Add a unit to the game."""
        self.units.append(unit)
    
    def get_selection_box(self) -> Optional[pygame.Rect]:
        """Get the current selection box rectangle."""
        if not self.selection_start:
            return None
        
        mouse_pos = pygame.mouse.get_pos()
        x1, y1 = self.selection_start
        x2, y2 = mouse_pos
        
        return pygame.Rect(
            min(x1, x2),
            min(y1, y2),
            abs(x2 - x1),
            abs(y2 - y1)
        )
    
    def handle_selection(self):
        """Handle unit selection logic."""
        selection_box = self.get_selection_box()
        if not selection_box:
            return
            
        if not pygame.key.get_pressed()[pygame.K_LSHIFT]:
            self.selected_units.clear()
            for unit in self.units:
                unit.selected = False
        
        for unit in self.units:
            if selection_box.colliderect(unit.get_rect()):
                unit.selected = True
                if unit not in self.selected_units:
                    self.selected_units.append(unit)
    
    def handle_movement(self, target_pos: Tuple[int, int]):
        """Handle unit movement commands."""
        if not self.selected_units:
            return

        # Move units in a grid formation
        for i, unit in enumerate(self.selected_units):
            row = i // 3
            col = i % 3
            offset_x = col * unit.separation_radius
            offset_y = row * unit.separation_radius
            
            target_x = target_pos[0] - (unit.separation_radius * 1.5) + offset_x
            target_y = target_pos[1] - (unit.separation_radius * 1.5) + offset_y
            
            unit.move_to((target_x, target_y))
    
    def handle_input(self) -> bool:
        """Handle game input events. Returns False if game should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.selection_start = pygame.mouse.get_pos()
                    self.selecting = True
                elif event.button == 3:  # Right click
                    self.handle_movement(pygame.mouse.get_pos())
                    
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.handle_selection()
                    self.selecting = False
                    self.selection_start = None
        
        return True
    
    def update(self):
        """Update game state."""
        for unit in self.units:
            unit.apply_physics(self.units)
    
    def draw(self):
        """Draw the game state."""
        self.screen.fill(self.colors['background'])
        
        # Draw grid
        for x in range(0, self.window_size[0], self.tile_size):
            pygame.draw.line(self.screen, self.colors['grid'],
                           (x, 0), (x, self.window_size[1]))
        for y in range(0, self.window_size[1], self.tile_size):
            pygame.draw.line(self.screen, self.colors['grid'],
                           (0, y), (self.window_size[0], y))
        
        # Draw units
        for unit in self.units:
            unit.draw(self.screen, self.colors)
        
        # Draw selection box
        if self.selecting:
            selection_box = self.get_selection_box()
            if selection_box:
                self.selection_surface.fill((0, 0, 0, 0))
                pygame.draw.rect(self.selection_surface,
                               self.colors['selection_box'],
                               selection_box)
                pygame.draw.rect(self.selection_surface,
                               self.colors['selection_border'],
                               selection_box, 1)
                self.screen.blit(self.selection_surface, (0, 0))
        
        pygame.display.flip()
    
    def run(self, target_fps: int = 60):
        """Run the game loop."""
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(target_fps)
