import random
from config import WINDOW_SIZE, POWERUP_SIZE

class PowerUp:
    def __init__(self):
        self.x = random.randint(0, WINDOW_SIZE[0] - POWERUP_SIZE)
        self.y = -POWERUP_SIZE
        self.active = True
        self.speed = 3
        self.type = random.choice(['shield', 'slow', 'score_boost'])
        self.duration = 5000  # Duration in milliseconds (5 seconds)
        
    def update(self):
        self.y += self.speed
        if self.y > WINDOW_SIZE[1]:  # Passed bottom of screen
            self.active = False
            return True
        return False

# Add to config.py
POWERUP_SIZE = 20
POWERUP_SPAWN_RATE = 10000  # Spawn every 10 seconds
POWERUP_COLORS = {
    'shield': (0, 255, 255),     # Cyan
    'slow': (255, 255, 0),       # Yellow
    'score_boost': (255, 165, 0)  # Orange
}