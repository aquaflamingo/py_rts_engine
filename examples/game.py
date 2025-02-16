from rts_engine.engine.game import RTSGame
from rts_engine.entities.unit import Unit

def main():
    # Create game instance
    game = RTSGame(
        window_size=(800, 600),
        tile_size=32,
        colors={
            'player_1': (0, 100, 255),  # Custom blue
            'player_2': (255, 50, 50),  # Custom red
        }
    )
    
    # Add some initial units in a formation
    positions = [
        (100, 100), (150, 100), (200, 100),
        (100, 150), (150, 150), (200, 150)
    ]
    
    for pos in positions:
        unit = Unit(
            position=pos,
            size=32,
            player_id=1,
            max_speed=3.0,
            separation_radius=40.0
        )
        game.add_unit(unit)
    
    # Run the game
    game.run()

if __name__ == "__main__":
    main()
