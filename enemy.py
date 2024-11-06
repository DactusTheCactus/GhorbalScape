# enemy.py

import random
from config import WINDOW_SIZE, ENEMY_SIZE, ENEMY_SPEED

class Enemy:
    def __init__(self):
        self.x = random.randint(0, WINDOW_SIZE[0] - ENEMY_SIZE)
        self.y = -ENEMY_SIZE
        self.active = True
        self.speed = random.uniform(ENEMY_SPEED - 1, ENEMY_SPEED + 2)

    def update(self):
        self.y += self.speed
        if self.y > WINDOW_SIZE[1]:  # Passed bottom of screen
            self.active = False
            return True
        return False
